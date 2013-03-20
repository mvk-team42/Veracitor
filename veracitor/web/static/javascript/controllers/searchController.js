/**
    Creates an interface in which a user can specify and perform a search for
    producers on the web or within the system database.

    The user will be presented a number of input fields into which she/he
    can specify hers/his search. The user can then perform a search and will
    thereafter recieve a response with the search results.
    @constructor
 */
var SearchController = function (view) {

    /** The time taken to switch between search types in milliseconds. */
    var SEARCH_SWITCH_TIME = 50;
    
    $("input[name=search-button]").click(function (evt) {
        var search_text = $("input[name=search-text]").val();
        var search_type_text = $("input[name=search-type-text]").val();
        
        request_database_search(search_text, search_type_text, null, null);
    });
    
    /**
        Makes a database search request to the Controller with the speci-
        fied search term. In the case where the user has not specified any
        certain tags or time period (start and end date) the request is made
        with “empty” fields (except from the required search term). The
        response data is handled by display response data.
     */
    var request_database_search = function (search_term, type, start_date,
                                                end_date) {
        $.post("/search_producers",{
            'name' : search_term,
            'type' : type
        }, function (data) {
            $("#search-result").html(data);
        })
        .fail(function () {
            $("#search-result").html("Server error.");
        });
    };
    
    /**
        Makes a web search request to the Controller with the spec-
        ified search term. The response data is handled by dis-
        play response data.

     */
    this.request_web_search = function (search_term) {
        // TODO
    };
    
    /**
        Displays response data from an earlier given request, and therefore
        works as a callback function.
    */
    this.display_response_data = function (data) {
        // TODO
    };
    
    /**
        Displays the given producer in the NetworkView.
     */
    this.show_producer_in_network = function (producer) {
        // TODO
    };
    
}

