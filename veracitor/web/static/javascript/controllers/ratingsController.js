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
       This function is called by the super controller when the tab is opened.
     */
    this.on_tab_active = function () {
    };

    /**
       Add event handlers to the ratings view.
     */
    function add_event_handlers() {

	$("#information-table td").click(function(evt) {
	    alert("Information table row clicked!");
	});

	$("#producer-table td").click(function(evt) {
	    alert("Producer table row clicked!");
	});

	$("#new-group").click(function(evt) {
	   // $('#new-group-form').css('display','block');
	    $('#new-group').css('display','none');
	    $('#new-group-form').fadeIn();
	});

	$('#create-group').click(function(evt) {
	    alert("plz create group :(");
	});

	$('#producer-list').accordion({ collapsible: true, active: false, header: "h3"});
	
	$('#information-list').accordion({ collapsible: true, active: false, header: "h3"});

	
    }


    /**
       Makes a database request to the server.
       Fetches all groups that the current user has.
    */
    var request_groups = function(user_id) {
	$.post("/jobs/search/groups", {
	    'user_id' : user_id
	}, function (data) {
	    var job_id = data['job_id'];

	    controller.set_job_callback(job_id, function (data) {
		if(data.result.data.length > 0) {
		    search_result = data.result.data;

		    //var table = etc etc
		    // see searchController...
		    //Fill tables with result
		}
	    });
	});
    }

    /**
       Makes a database request to the server.
       Fetches a specific group that the current user has
    */
    var request_group = function(user_name,group_name ) {
	$.post("/jobs/ratings/group", {
	    'owner_name' : user_name,
	    'group_name' : group_name
	}, function (data) {
	    var job_id = data['job_id'];

	    controller.set_job_callback(job_id, function (data) {
		if(data.result.data.length > 0) {
		    search_result = data.result.data;

		    //var table = etc etc
		    // see searchController...
		    //Fill tables with result
		}
	    });
	});
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
