/**
   The master/super controller of the Veracitor web site.
   @constructor
*/
function SuperController(vera) {

    // The current visible tab
    var active_tab;

    /** CSS classes. */
    var CLASSES = {
        'ACTIVE' : 'active'
    };
    /** CSS view positions. */
    var VIEW_POS = {
        'CENTER' : '0px',
        'LEFT' : '-100%',
        'RIGHT' : '100%'
    };
    /** Event key codes */
    var key = {
        'left': 37,
        'right': 39
    };

    // The time interval between callback checks
    var CALLBACK_CHECK_TIME = 100;
    // The time taken to switch from one tab to another in milliseconds
    var TAB_SWITCH_TIME = 300;

    // A pointer to this object
    var controller = this;

    /**
       Initializes this controller.
     */
    this.initialize = function () {
        // Setup controllers
        if (typeof vera.search !== 'undefined') {
            controller.search = new SearchController(this);
        }
        if (typeof vera.network !== 'undefined') {
            controller.network = new NetworkController(this);
        }
        if (typeof vera.ratings !== 'undefined') {
            controller.ratings = new RatingsController(this);
        }
        if (typeof vera.account !== 'undefined') {
            controller.account = new AccountController(this);
        }
        if (typeof vera.login !== 'undefined') {
            controller.login = new LoginController(this);
        }

        (function () {
            // Bind key combination shift + alt + left/right to switching
            // between the different tabs (for fast GUI testing)
            window.addEventListener('keydown', function (evt) {
                if (evt.altKey && evt.shiftKey) {
                    switch (evt.keyCode) {
                    case key.left:
                        controller.switch_to_tab_index(active_tab - 1);
                        break;
                    case key.right:
                        controller.switch_to_tab_index(active_tab + 1);
                        break;
                    }
                }
            });
        })();
    };

    /**
        Handles the event fired when a menu tab is clicked.
        If the current visible tab is to the left of the clicked
        tab it will be animated out from the screen to the left,
        otherwise to the right.
        The clicked tab will be animated in to the screen, following
        the motion of the previous visible tab.
        @name Vera#menu_click
        @function
        @param {Event} evt The fired event.
     */
    this.menu_click = function (evt) {
        /** A key in the vera.dom object of tab objects. */
        var tab;
        /** The index of the clicked tab. */
        var clicked_tab;
        /** The key of the clicked tab */
        var clicked_tab_key

        clicked_tab = 0;
        clicked_tab_key = null;

        // Retrieve the index of the clicked tab
        for(tab in vera.dom) {
            if(vera.dom[tab].menu[0] == evt.currentTarget) {
                clicked_tab = vera.dom[tab].index;
                clicked_tab_key = tab;
                break;
            }
        }

        for(tab in vera.dom) {

            if(vera.dom[tab].index == clicked_tab) {
                vera.dom[tab].menu.addClass(CLASSES.ACTIVE);

                // Animate the clicked tab to the center of the screen
                vera.dom[tab].view.animate({
                    'left' : VIEW_POS.CENTER
                }, TAB_SWITCH_TIME, null);

            } else if(vera.dom[tab].index == active_tab) {
                vera.dom[tab].menu.removeClass(CLASSES.ACTIVE);

                // Animate the previous visible tab out of the screen
                vera.dom[tab].view.animate({
                    'left' : (vera.dom[tab].index < clicked_tab) ?
                            VIEW_POS.LEFT : VIEW_POS.RIGHT
                }, TAB_SWITCH_TIME, null);

            } else {
                vera.dom[tab].menu.removeClass(CLASSES.ACTIVE);

                // Move the tab relative to the clicked tab
                vera.dom[tab].view.css({
                    'left' : (vera.dom[tab].index < clicked_tab) ?
                            VIEW_POS.LEFT : VIEW_POS.RIGHT
                });
            }
        }

        active_tab = clicked_tab;
        // Save active tab for further sessions
        vera.local_storage.set_active_tab(vera.user_name, active_tab);
        // Notify the tab that it has been activated
        controller[clicked_tab_key].on_tab_active();
    }

    /**
        Switches to the tab with the given index.
        @param tabIndex The index of the target tab.
     */
    this.switch_to_tab_index = function (tabIndex) {
        if(tabIndex >= 0 && tabIndex < vera.tabs.length) {
            vera.dom[vera.tabs[tabIndex].key].menu.click();
        }
    }

    /**
        Switches to the tab with the given name.
        @param tab The name of the target tab.
     */
    this.switch_to_tab = function (tab) {
        if(typeof(vera.dom[tab]) !== 'undefined') {
            vera.dom[tab].menu.click();
        }
    }

    /**

       @param f The function checking the callback.
       @param id An id related to the job started on the server.
     */
    this.set_job_callback = function (job_id, callback) {
        watch_job(job_id, callback);
    }

    /**
       Check the status of a started job on the server.
       @param callback The callback function.
       @param job_id An id related to the job started on the server.
     */
    var watch_job = function (job_id, callback) {
        $.post('/jobs/job_result', {
            'job_id' : job_id
        }, function (data, status, jqXHR) {
            if(jqXHR.status == 200) {
                callback(data);
            } else {
                setTimeout(function () {
                    watch_job(job_id, callback);
                }, CALLBACK_CHECK_TIME);
            }
        })
        .fail(function () {
            $("#search-result").html("<h2>Server error.</h2>");
        });
    }

    /**
       Request a TidalTrust value.
    */
    window.tt = function request_tidal_trust(source, sink, tag) {
        $.post('/jobs/algorithms/tidal_trust', {
            'source': source,
            'sink': sink,
            'tag': tag
        }, function (data) {
            // SUCCESS
            console.log("Ok: ", data);
        })
        .fail(function (data) {
            // FAIL
            console.log("Fail:", data);
        });
    }
    window.job_result = function request_job_result(job_id) {

        $.post('/jobs/job_result', {
            'job_id': job_id
        }, function (data) {
            // SUCCESS
            console.log("Ok: ", data);
        })
        .fail(function (data) {
            // FAIL
            console.log("Fail:", data);
        });

    }

    this.new_loader = function ( parent, css ) {
        return new Loader(parent, css);
    };

    /**
       A loader object used for displaying a loading gif tag.
     */
    var Loader = function ( parent, css ) {

        // A reference to this object
        var _self = this;

        var tag = $('<img>').attr({
            'src': 'static/images/loading2.gif',
            'alt': 'Loading'
        });

        var init = function () {
            if (typeof parent !== 'undefined') {
                _self.append_to(parent);
            }
            if (typeof css !== 'undefined') {
                _self.css(css);
            }
        };

        /**
           Appends this objects tag to the given parent.
         */
        this.append_to = function ( parent ) {
            if (parent instanceof jQuery) {
                parent.append(tag);
            } else if (parent instanceof HTMLElement) {
                parent.appendChild(tag[0]);
            } else {
                throw 'Parent not a DOM element.';
            }
        };

        /**
           Sets the CSS of the objects tag jQuery style.
         */
        this.css = function ( css ) {
            if (css instanceof Object) {
                tag.css(css);
            } else {
                throw 'CSS styling not an Object.';
            }
        };

        /**
           Deletes this objects tag from the dom tree.
         */
        this.delete = function () {
            tag.remove();
        };

        // Initialize the object
        init();

    };

}
