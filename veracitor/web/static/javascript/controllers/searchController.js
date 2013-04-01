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
    /** The event key code for the enter key. */
    var ENTER = 13;

    // define enter key press in local search field
    $("#local-search-field").keydown(function (evt) {
        if(evt.keyCode == ENTER) {
            // move focus to the local search button
            $("#local-search-button").focus();
        }
    });

    $("input[name=search-button]").click(function (evt) {
        var search_text = $("input[name=search-text]").val();
        var t, types, search_type;

        types = $("#search-types input");

        for(t = 0; t < types.length; t ++) {
            if(types[t].checked) {
                search_type = types[t].value;
                break;
            }
        }

        request_database_search(search_text, search_type, null, null);
    });

    /**
        Makes a database search request to the server with the specified
        search term. In the case where the user has not specified any
        certain tags or time period (start and end date) the request is made
        with “empty” fields (except from the required search term).
     */
    var request_database_search = function (search_term, type, start_date,
                                                end_date) {
        $.post("/search_producers", {
            'name' : search_term,
            'type' : type
        }, function (data) {
            var response = JSON.parse(data);

            $("#search-result").html(response.html);

            if(response.error.type != "none") {
                if(response.error.type == "no_result") {
                    // set focus on the search add text field
                    $("#search-add-field").focus();

                    // define enter key press in search add field
                    $("#search-add-field").keydown(function (evt) {
                        if(evt.keyCode == ENTER) {
                            // move focus to the local search button
                            $("#search-add-button").focus();
                        }
                    });

                    // add an event listener for the created button
                    $("#search-add-button").click(function () {
                        var search_text = $("#search-add-field").val();

                        request_database_add_entity(search_text);
                    });
                }
            }
        })
        .fail(function () {
            $("#search-result").html("<h2>Server error.</h2>");
        });
    };

    /**
        Makes a database add request to the server with the specified
        search term. If the search term is a URL the a crawler is
        started on the server side. The crawler will notify the client
        that a crawler has been started with a callback.
     */
    var request_database_add_entity = function (search_term) {
        $.post("/add_entity", {
            'url' : search_term
        }, function (data) {
            var response = JSON.parse(data);

            if(response.error.type == "none") {
                $("#search-result").html("<h2>Request succesfully sent to server.</h2>");
            } else {
                $("#search-result").html("<h2>" + response.error.message + "</h2>");
            }
        })
        .fail(function () {
            $("#search-result").html("<h2>Server error.</h2>");
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
