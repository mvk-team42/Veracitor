/**
    Creates an interface in which a user can specify and perform a search for
    producers on the web or within the system database.

    The user will be presented a number of input fields into which she/he
    can specify hers/his search. The user can then perform a search and will
    thereafter recieve a response with the search results.
    @constructor
 */
var SearchController = function (view) {

    /** Search types */
    var SEARCH_TYPE = {
        'WEB' : 0,
        'DATABASE' : 1
    };
    /** The time taken to switch between search types in milliseconds. */
    var SEARCH_SWITCH_TIME = 50;
    
    /** The current search type. */
    var currentSearchType;

    $("#search-type-select input[name=web]").click(function (evt) {
        $(this).addClass("active");
        $("#search-type-select input[name=database]").removeClass("active");

        $("#database-search").slideUp(SEARCH_SWITCH_TIME);
        
        $("input[name=search-button]").attr("value", "Web search");
        $("#search-info").html("Perform a web search for sources and publications.");
        
        currentSearchType = SEARCH_TYPE.WEB;
    });
    
    $("#search-type-select input[name=database]").click(function (evt) {
        $(this).addClass("active");
        $("#search-type-select input[name=web]").removeClass("active");
           
        $("#database-search").slideDown(SEARCH_SWITCH_TIME);
        
        $("input[name=search-button]").attr("value", "Database search");
        $("#search-info").html("Perform a local search in the database for sources or publications.");
        
        currentSearchType = SEARCH_TYPE.DATABASE;
    });
    
    // Set default search type
    $("#search-type-select input[name=database]").click();
    
    $("input[name=search-button]").click(function (evt) {
        var searchText = $("input[name=search-text]").val();
        var searchTypeText = $("input[name=search-type-text]").val();
        
        requestDatabaseSearch(searchText, searchTypeText, null, null);
    });
    
    /**
        Makes a database search request to the Controller with the speci-
        fied search term. In the case where the user has not specified any
        certain tags or time period (start and end date) the request is made
        with “empty” fields (except from the required search term). The
        response data is handled by display response data.
     */
    var requestDatabaseSearch = function (searchTerm, tags, startDate, endDate) {
        $.post("/search_producers",{
            'name' : searchTerm,
            'type' : tags // TODO search by type or tags?
        }, function (data) {
            var result;
            var tag;
            var key;
            var resultTag = $("#search-result");
            
            // parse JSON object
            data = JSON.parse(data);
            
            resultTag.html("");
            
            if(data.error) {
                resultTag.html(data.error);
            } else {
                for(result in data) {
                    tag = $("<div>");
                    
                    for(key in data[result]) {
                        tag.append($("<p>").html(
                            key + ": " + data[result][key]
                        ));
                    }
                    
                    resultTag.append(tag);
                }
            }
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

