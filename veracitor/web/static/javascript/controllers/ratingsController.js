/**
    Handles a users ratings to other producer objects in the database.

    The user is presented a list with already rated producers and users, as
    well as groups, that is defined in the database. All set ratings can be
    altered directly in the list and there will be an option to display a se-
    lected producer in the NetworkView. Producers, users and groups not
    previously rated will be presented in a separate list and will be moved to
    the “rated list” when a rating is set.
    @constructor
 */
var RatingsController = function (controller) {

    /**
       Initialize the ratings tab:
       - Setup event handlers 
    */
    (function () {

        add_event_handlers();

    })();


     /**
       Add event handlers to the ratings view.
     */
    function add_event_handlers() {
	//TODO
    }


    /**
       Makes a database request to the server. 
       Fetches all groups that the current user has.
    */
    var request_groups = function(user_id) {
	//TODO Make job call.
	//See searchController for example.
    }


    /**
       Makes a database request to the server.
       Fetches information objects, optionally 
       filtered by tag.
       TODO: Any more filters?
    */
    var request_information_objects = function(tag) {
	//TODO: Implement.
    }


    //TODO. Nåt sånt?
    function set_producer_reliability_rating(producer_id) {
   
    }

    //TODO. Nåt sånt?
    function set_information_credibility_rating(information_id) {

    }

};
