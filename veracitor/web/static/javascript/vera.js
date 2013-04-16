/**
    JavaScript code for the Veracitor project.
    Dependent on the global variable 'vera' recieved from a request made to
    the Veracitor home page.
    @name Vera
    @constructor
    @author John Brynte Turesson
 */
(function () {

    /** The current visible tab. */
    var activeTab;
    /** Controllers */
    var controllers = {
        'search' : null,
        'network' : null,
        'groups' : null,
        'account' : null
    };

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
        var sideTab;

        activeTab = 1;

        vera.dom = {};

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
            vera.dom[key].menu.click(menuClick);

            // Set the active tab and initialize the tab positions
            if(tab == activeTab) {
                vera.dom[key].view.css({
                    'left' : VIEW_POS.CENTER
                });
                vera.dom[key].menu.addClass(CLASSES.ACTIVE);

            } else {
                vera.dom[key].view.css({
                    'left' : (vera.dom[key].index < activeTab) ?
                            VIEW_POS.LEFT : VIEW_POS.RIGHT
                });
            }

            // Get the left side tab
            sideTab = vera.dom[key].view.find(".left.side-tab");

            if(tab == 0) {
                sideTab.remove();

            } else {
                // Set side tab text
                sideTab.find("p").html(vera.tabs[tab - 1].name);

                // Simulates a click in the menu.
                // A function is generated with the corresponding key in its scope.
                sideTab.click((function (tabIndex) {
                    return function() {
                        switchToTab(tabIndex);
                    };
                })(tab - 1));
            }

            // Get the right tab side
            sideTab = vera.dom[key].view.find(".right.side-tab");

            if(tab == vera.tabs.length - 1) {
                sideTab.remove();

            } else if(vera.tabs.length > 1) {
                // Set side tab text
                sideTab.find("p").html(vera.tabs[tab + 1].name);

                // Simulates a click in the menu.
                // A function is generated with the corresponding key in its scope.
                sideTab.click((function (tabIndex) {
                    return function() {
                        switchToTab(tabIndex);
                    };
                })(tab + 1));
            }
        }

        // Add controllers
        controllers.super = new SuperController();
        controllers.search = new SearchController(
            vera.dom.search, controllers.super);
        controllers.network = new NetworkController(
            vera.dom.network, controllers.super, new Visualizer());
        controllers.ratings = new RatingsController(
            vera.dom.ratings, controllers.super);
        controllers.account = new AccountController(
            vera.dom.account, controllers.super);
    }
    // Run this function when the document has loaded
    $(document).ready(init);

    /**
        Handles the event fired when a menu tab is clicked.
        If the current visible tab is to the left of the clicked
        tab it will be animated out from the screen to the left,
        otherwise to the right.
        The clicked tab will be animated in to the screen, following
        the motion of the previous visible tab.
        @name Vera#menuClick
        @function
        @param {Event} evt The fired event.
     */
    var menuClick = function (evt) {
        /** A key in the vera.dom object of tab objects. */
        var tab;
        /** The index of the clicked tab. */
        var clickedTab;

        clickedTab = 0;

        // Retrieve the index of the clicked tab
        for(tab in vera.dom) {
            if(vera.dom[tab].menu[0] == evt.currentTarget) {
                clickedTab = vera.dom[tab].index;
            }
        }

        for(tab in vera.dom) {

            if(vera.dom[tab].index == clickedTab) {
                vera.dom[tab].menu.addClass(CLASSES.ACTIVE);

                // Animate the clicked tab to the center of the screen
                vera.dom[tab].view.animate({
                    'left' : VIEW_POS.CENTER
                }, TAB_SWITCH_TIME, null);

            } else if(vera.dom[tab].index == activeTab) {
                vera.dom[tab].menu.removeClass(CLASSES.ACTIVE);

                // Animate the previous visible tab out of the screen
                vera.dom[tab].view.animate({
                    'left' : (vera.dom[tab].index < clickedTab) ?
                            VIEW_POS.LEFT : VIEW_POS.RIGHT
                }, TAB_SWITCH_TIME, null);

            } else {
                vera.dom[tab].menu.removeClass(CLASSES.ACTIVE);

                // Move the tab relative to the clicked tab
                vera.dom[tab].view.css({
                    'left' : (vera.dom[tab].index < clickedTab) ?
                            VIEW_POS.LEFT : VIEW_POS.RIGHT
                });
            }
        }

        activeTab = clickedTab;

        return false;
    }

    /**
        Switches to the tab with the given index.
        @param tabIndex The index of the target tab.
     */
    var switchToTab = function (tabIndex) {
        if(tabIndex >= 0 && tabIndex < vera.tabs.length) {
            vera.dom[vera.tabs[tabIndex].key].menu.click();
        }
    }

})();
