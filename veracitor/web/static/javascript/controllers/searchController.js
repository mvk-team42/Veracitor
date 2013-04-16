/**
    Creates an interface in which a user can specify and perform a search for
    producers on the web or within the system database.

    The user will be presented a number of input fields into which she/he
    can specify hers/his search. The user can then perform a search and will
    thereafter recieve a response with the search results.
    @constructor
 */
var SearchController = function (view, controller) {

    /** Initializing */

    // The time taken to switch between search types in milliseconds
    var SEARCH_SWITCH_TIME = 50;
    // The event key code for the enter key
    var ENTER = 13;

    var active_search_type = 0;

    /**
      Initialize the search tab:
      - Setup event handlers
      - Setup time period slider
     */
    (function () {
        initialize_time_period_slider();

        add_event_handlers();
    })();

    /**
       Initialize the time period slider.
     */
    function initialize_time_period_slider() {
     var range = {
            min: 1970,
            max: 2013,
            step: 10,
            range: 0
        };
        range.range = range.max - range.min;

        $("#slider").slider({
            range: true,
            min: range.min,
            max: range.max,
            values: [range.max - 10, range.max],
            slide: function(event, ui) {
                $("#time-period").html(ui.values[ 0 ] + " - " + ui.values[ 1 ]);
            }
        });
        $("#time-period").html($("#slider").slider("values", 0 ) +
                           " - " + $("#slider").slider("values", 1 ));

        var width = parseInt($("#slider-container").css("width"));
        var labels = $("#slider-labels");
        labels.css({
            width: width + "px"
        });

        // set start step
        var s = Math.floor(range.min / 10) * 10;
        while(s < range.min) {
            s += range.step;
        }

        var line;
        var label;
        for( ; s <= range.max; s += range.step) {
            label = $("<div>");
            label.css({
                position: "absolute",
                left: (width * (s - range.min) / range.range - 20) + "px"
            }).html(s);

            line = $("<div>");
            line.css({
                position: "absolute",
                left: "20px",
                top: "bottom",
                width: "1px",
                height: "10px",
                background: "#000"
            });
            label.append(line);

            labels.append(label);
        }
    }

    /**
       Add event handlers to the search view.
     */
    function add_event_handlers() {
        // define enter key press in local search field
        $("#database-search-field").keydown(function (evt) {
            if(evt.keyCode == ENTER) {
                // move focus to the local search button
                $("#database-search-button").focus();
            }
        });

        // search button click event
        $("#database-search-button").click(function (evt) {
            var search_text = $("#database-search-field").val();

            switch(active_search_type) {
                case 0:
                request_database_search(search_text, "Producer", null, null);
                break;

                case 1:
                break;
            }
        });

        // database search tab click event
        $("#database-search-tab").click(function (evt) {
            set_active_tab(0);
        });

        // add entity tab click event
        $("#add-entity-tab").click(function (evt) {
            set_active_tab(1);
        });

        // add search type radio source button click event
        $("#search-type-source > .radio").click(function (evt) {
            set_active_search_type(0);
        });

        // add search type radio information button click event
        $("#search-type-information > .radio").click(function (evt) {
            set_active_search_type(1);
        });

        set_active_tab(0);
        set_active_search_type(active_search_type);

        // set focus on the database search field
        $("#database-search-field").focus();
    }

    /**
       Sets the nth tab and content to be active/visible.
     */
    function set_active_tab(n) {
        $("#search-tabs > .head > .tab").removeClass("active");
        $("#search-tabs > .head > .tab:eq(" + n + ")").addClass("active");

        $("#search-tabs > .body > .content").css("display", "none");
        $("#search-tabs > .body > .content:eq(" + n + ")").css("display", "block");
    }

    /**
       Sets the nth search type to be active.
     */
    function set_active_search_type(n) {
        var active_tab = $("#search-tabs > .body > .content:eq(0)");
        active_search_type = n;

        active_tab.find(".search-type > .content > .overlay").css("display", "block");
        active_tab.find(".search-type:eq(" + n + ") > .content > .overlay").css("display", "none");
    }

    /**
        Makes a database search request to the server with the specified
        search term. In the case where the user has not specified any
        certain tags or time period (start and end date) the request is made
        with 'empty' fields (except from the required search term).
     */
    var request_database_search = function (search_term, type, start_date,
                                                end_date) {
        $("#search-result").html("Searching...")
        $.post("/jobs/search/producers", {
            'name' : search_term,
            'type' : type
        }, function (data) {
            var response = JSON.parse(data);
            console.log(data);
            var job_id = response['job_id']
            controller.watch_callback(function (data){
                var response = JSON.parse(data);
                $("#search-result").html(response.html);
            } ,'/jobs/job_result', job_id)

        })
        .fail(function (data) {
            var response = JSON.parse(data);
            console.log(data); // TODO
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
                        var url = $("#search-add-field").val();

                        request_crawl_procedure(url);
                    });
                }
            }
            $("#search-result").html("<h2>Server error.</h2>");
        });
    };

    /**
        Makes a database add request to the server with the specified
        search term. If the search term is a URL the a crawler is
        started on the server side. The crawler will notify the client
        that a crawler has been started with a callback.
     */
    var request_crawl_procedure = function (url) {
        $.post("/request_crawl_procedure", {
            'url' : url
        }, function (data) {
            var response = JSON.parse(data);

            if(response.error.type == "none") {
                $("#search-result").html("<h2>" + response.procedure.message + "</h2>");

                controller.watch_callback(function (response) {
                    $('#search-result').html("<h2>" + response.procedure.message + "</h2>");
                }, response.procedure.callback_url, response.procedure.id);

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
