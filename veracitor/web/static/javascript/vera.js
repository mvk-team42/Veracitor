/**
    JavaScript code for the Veracitor project.
    Dependent on the global variable 'vera' recieved from a request made to
    the Veracitor home page.
    @name Vera
    @constructor
    @author John Brynte Turesson
 */
(function () {

    /** The super controller */
    var controller;

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
    /** The width of the side tabs */
    var SIDE_TAB_WIDTH = 40;
    /** The time taken to switch from one tab to another in milliseconds. */
    var TAB_SWITCH_TIME = 300;

    /**
        This function is run when the document is loaded.
        @name Vera#init
        @function
     */
    var init = function () {
        /** Index in vera.tabs */
        var tab;
        /** Key in vera.dom */
        var name;
        /** Side tab dom element */
        var side_tab;

        vera.local_storage = {
            'get_active_tab': function ( user ) {
                if (localStorage.getItem(this._private.ACTIVE_TAB + user) !== null) {
                    return parseInt(localStorage.getItem(this._private.ACTIVE_TAB + user));
                } else {
                    return 0;
                }
            },
            'set_active_tab': function ( user, tab_index ) {
                if (typeof user !== 'undefined') {
                    localStorage.setItem(this._private.ACTIVE_TAB + user, tab_index);
                }
            },
            '_private': {
                'ACTIVE_TAB': 'veracitor_active_tab_'
            }
        };

        var active_tab = vera.local_storage.get_active_tab(vera.user_name);

        vera.dom = {};

        // Add the super controller and its sub controllers
        controller = new SuperController(vera);

        for(tab = 0; tab < vera.tabs.length; tab ++) {
            key = vera.tabs[tab].key;

            vera.dom[key] = {};
            // Pointer to the view
            vera.dom[key].view = $("#" + vera.tabs[tab].viewid);
            // Pointer to the menu item
            vera.dom[key].menu = $("#" + vera.tabs[tab].menuid);
            // An index to specify the view position
            vera.dom[key].index = parseInt(tab);

            // Add click events
            vera.dom[key].menu.click(controller.menu_click);

            // Set the active tab and initialize the tab positions
            if(tab == active_tab) {
                vera.dom[key].view.css({
                    'left' : VIEW_POS.CENTER
                });
                vera.dom[key].menu.addClass(CLASSES.ACTIVE);

            } else {
                vera.dom[key].view.css({
                    'left' : (vera.dom[key].index < active_tab) ?
                            VIEW_POS.LEFT : VIEW_POS.RIGHT
                });
            }

            // Get the left side tab
            side_tab = vera.dom[key].view.find(".left.side-tab");

            if(tab == 0) {
                side_tab.remove();

            } else {
                // Set side tab text
                side_tab.find("p").html(vera.tabs[tab - 1].name);

                // Simulates a click in the menu
                side_tab.click((function (tab) {
                    return function () {
                        controller.switch_to_tab_index(tab);
                    };
                })(tab - 1));
            }

            // Get the right tab side
            side_tab = vera.dom[key].view.find(".right.side-tab");

            if(tab == vera.tabs.length - 1) {
                side_tab.remove();

            } else if(vera.tabs.length > 1) {
                // Set side tab text
                side_tab.find("p").html(vera.tabs[tab + 1].name);

                // Simulates a click in the menu
                side_tab.click((function (tab) {
                    return function () {
                        controller.switch_to_tab_index(tab);
                    };
                })(tab + 1));
            }
        }

        // activate the active tab
        controller.switch_to_tab_index(active_tab);
    }

    // Initialize when the document has loaded
    $(document).ready(init);

})();
