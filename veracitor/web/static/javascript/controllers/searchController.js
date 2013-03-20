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
            var result;
            var key;
            var tbody;
            var table = $("#search-result table");
            
            $("#search-result table").html("");
            
            // parse JSON object
            data = JSON.parse(data);
            
            for(result in data) { break; };
            
            console.log(result);
            
            if(result == "undefined") {
                console.log("could not find anything");
            }
            
            if(data.error) {
                $("#search-result table").append(
                    $("<thead></thead>").append(
                        $("<tr></tr>").append($("<th>").html(data.error))
                    )
                );
            } else {
                table.append(
                    $("<thead></thead>").append(
                        $("<tr></tr>")
                        .append($("<th>").html("Name"))
                        .append($("<th>").html("Type"))
                    )
                );
            
                tbody = $("<tbody>");
            
                for(result in data) {
                    tbody.append(
                        $("<tr></tr>")
                        .append($("<td>").html(data[result]['_data']['name']))
                        .append($("<td>").html(data[result]['type_']))
                    );
                }
                
                table.append(tbody);
                
                if(result == "undefined") {
                    console.log("undefined");
                }
            }
        })
        .fail(function () {
            $("#search-result table").append(
                $("<thead></thead>").append(
                    $("<tr></tr>").append($("<th>").html("Name"))
                )
            );
        });
    };
    
    /**
        Makes a web search request to the Controller with the spec-
        ified search term. The response data is handled by dis-
        play response data.

     */
    this.requestWebSearch = function (searchTerm) {
        // TODO
    };
    
    /**
        Displays response data from an earlier given request, and therefore
        works as a callback function.
    */
    this.displayResponseData = function (data) {
        // TODO
    };
    
    /**
        Displays the given producer in the NetworkView.
     */
    this.showProducerInNetwork = function (producer) {
        // TODO
    };
    
}

