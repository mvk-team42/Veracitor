/**
   Creates an interface in which a user can specify and perform a search for
   producers on the web or within the system database.

   The user will be presented a number of input fields into which she/he
   can specify hers/his search. The user can then perform a search and will
   thereafter recieve a response with the search results.
   @constructor
*/
var SearchController = function (controller) {

    /** Initializing */

    // The time taken to switch between search types in milliseconds
    var SEARCH_SWITCH_TIME = 50;
    // The event key code for the enter key
    var ENTER = 13;

    var active_search_type = 0;

    // Array of source results
    var search_results = [];

    var crawls_displayed = [];

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
       This function is called by the super controller
       each time the tab is opened.
     */
    this.on_tab_active = function () {
        // set focus to the database search field
        $("#database-search-field").focus();

        return auto_update_crawler_results();
    };

    function auto_update_crawler_results(){
        update_crawler_results();

        display_crawler_results();
//        setTimeout(auto_update_crawler_results, 5000);
    }

    /**
       Initialize the time period slider.
    */
    function initialize_time_period_slider() {
        var range = {
            'min': 1970,
            'max': 2013,
            'step': 10,
            'range': 0
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
                var value = $("#search-type-source input[name='source_type']:checked").val();
                if (value === 'Producer') {
                    value = '';
                }
                request_database_producer_search(search_text, value, null, null);
                break;

            case 1:
                if(document.getElementById("time-period-yes").checked){
                    var values = $('#slider').slider("option", "values");
                    request_database_info_search(search_text, [], values[0]+"-1-1", values[1]+"-1-1")
                } else {
                    request_database_info_search(search_text, [], null, null)
                }
                break;
            }
        });

        // database search tab click event
        $("#database-search-tab").click(function (evt) {
            set_active_tab(0);
            $("#search-result-content").show();
            $("#crawl-result-content").hide();
        });

        // add entity tab click event
        $("#add-entity-tab").click(function (evt) {
            set_active_tab(1);
            $("#search-result-content").hide();
            $("#crawl-result-content").show();
        });

        // add search type radio source button click event
        $("#search-type-source .radio").click(function (evt) {
            set_active_search_type(0);
        });

        // add search type radio information button click event
        $("#search-type-information .radio").click(function (evt) {
            set_active_search_type(1);
        });

        set_active_tab(0);
        set_active_search_type(active_search_type);

        // Start crawl click event
        $("#crawler-search-button").click(function (evt) {
            var url = $("#crawler-search-field").val();
            var extra_info = $('#add-entity-content form input[type=checkbox]').is(':checked');
            if (extra_info) {
                request_source_crawl(url);
            } else {
                request_add_newspaper_crawl(url);
            }
        });

        // crawler tip-text
        $('.information .question-mark').click(function(){
            $('.information .tip-text').toggle();
        });

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
    var request_database_producer_search = function (search_term, type, start_date,
                                             end_date) {
        $("#search-result").html("Searching...");
        $.post("/jobs/search/producers", {
            'name' : search_term,
            'type' : type
        }, function(data) {
            insert_database_search_results(data, "producers");
        })
            .fail(function (data) {
                display_search_error(vera.const.search.server_error);
            });
    };

    var request_database_info_search = function (search_text, tags, start_date, end_date) {
        $("#search-result").html("Searching...")

        var paramObject = {
            'title_part' : search_text,
            'tags' : JSON.stringify(tags),
        };

        if (start_date !== null && end_date !== null) {
            paramObject['start_date'] = start_date;
            paramObject['end_date'] = end_date;
        }

        $.post("/jobs/search/information", paramObject, function(data) {
            insert_database_search_results(data, "information");
        })
            .fail(function (data) {
                display_search_error(vera.const.search.server_error);
            });
    };

    /**
     * Fetches the search results from an info or source search, renders the table html
     * and inserts it into the search results div table area thingy.
     */
    var insert_database_search_results = function(job_data, type){
        var job_id = job_data['job_id'];
        var urlLength = 35;

        controller.set_job_callback(job_id, function (data) {
            if(data.result.data){
                search_result = data.result.data[type];

                $('#search-result').html(data.result.html);

                if(type == "information"){

                    // Shorten urls if necessary and make them into links.
                    $.each($('#search-result tr td.url'), function(i, val){
                        url = $(this).html();
                        urltext = url.length > urlLength ?
                            url.substring(0,urlLength-3)+'...' :
                            url;

                        $(this).html('<a href="'+url+'" target="_blank">'+urltext+'</a>');
                    });

                }

                $('#search-result .link').click(function (evt) {
                    var prod;
                    if(type === "information"){
                        prod = search_result[$(this).parent().index()].publishers[0];
                    } else if (type === "producers"){
                        prod = search_result[$(this).parent().index()].name;
                    }

                    controller.network.visualize_producer_in_network(prod);
                    controller.switch_to_tab('network');
                });
            } else {
                display_search_error(vera.const.search['no_'+type]);
            }
        });
    };


    /**
       Requests an article crawl as specified by the web server.
       Also dispatches an update for the dom with the users current
       crawling jobs.
    */
    function request_article_crawl(url) {
        $.post("/jobs/crawler/scrape_article", {"url":url}, function(data) {
            $("#crawler-result table").append($("<thead>").html("Fetching crawls..."));
            update_crawler_results();
        }).fail(function(){
            display_crawler_error("Unable to start crawler.");
        });
    }

    /**
       Requests a crawl for simply adding the newspaper to the database.
    */
    function request_add_newspaper_crawl(url) {
        $.post("/jobs/crawler/add_newspaper", {"url":url}, function(data) {
            $("#crawler-result table").append($("<thead>").html("Fetching crawls..."));
            update_crawler_results();
        }).fail(function(){
            display_crawler_error("Unable to start crawler.");
        });
    }


    /**
       Requests a source crawl as specified by the web server.
       Also dispatches an update for the dom with the users current
       crawling jobs.
    */
    function request_source_crawl(url) {
        $.post("/jobs/crawler/request_scrape", {"url":url}, function(data) {
            $("#crawler-result table").append($("<thead>").html("Fetching crawls..."));
            update_crawler_results();
        }).fail(function(){
            display_crawler_error("Unable to start crawler.");
        });
    }

    /**
       Sends a request for getting the users crawler jobs and updates
       the ui accordingly.
    */
    function update_crawler_results() {
        var i = 0;
        $.post("/jobs/crawler/crawls", function(data) {
            for (id in data) {
                if(is_in_crawls(id)) {
                    continue;
                }
                data[id].id = id;
                crawls_displayed.push(data[id]);
            }
            update_crawls_producers();
        }).fail(function(){
            display_crawler_error("Unable to update crawls.");
        });
    }

    function is_in_crawls(id) {
        var i = 0;
        for (; i< crawls_displayed.length; i++) {
            if (crawls_displayed[i].id == id) {
                return true;
            }
        }
        return false;
    }

    function update_crawls_producers() {
        var i = 0;
        for (;i<crawls_displayed.length;i++) {
            var crawl = crawls_displayed[i];
            $.post('/jobs/job_result',{"job_id":crawl.id}, function(d){
                if (typeof(d['result']) !== "undefined") {
                    crawl["producer_name"] = d["result"]["producer_name"];
                }
            }).fail(function(data){
                // Do nothing since job wasn't done.
            });
        }
    }

    function display_crawler_results() {
        var i, thead= $("<thead>").append($("<tr>")
                                          .append($("<td>").html("Type"))
                                          .append($("<td>").html("URL"))
                                          .append($("<td>").html("Ready to visualize?")));

        crawls_displayed.sort(function(a,b){
            return parseDate(a['start_time']) < parseDate(b['start_time']);
        });

        for (i=0; i<crawls_displayed.length; i++) {

            // Add button to visualize producer in network
            var prod_td = $("<td>").html("No");
            var producer_name = crawls_displayed[i]["producer_name"];
            console.log(producer_name);
            if (typeof(producer_name) !== "undefined") {
                prod_td = $("<td>")
                    .append($("<button>")
                            .html("Show in network")
                            .click(function(){
                                controller.network.visualize_producer_in_network(producer_name);
                                controller.switch_to_tab("network");
                            }));
            }

            thead.append($("<tr>")
                         .attr("id", crawls_displayed[i]["id"])
                         .append($("<td>").html(crawls_displayed[i]["type"]))
                         .append($("<td>").html(crawls_displayed[i]["url"]))
                         .append(prod_td));
        }
        $("#crawler-result table").html(thead);
    }

    function display_crawler_error( error ) {
        $("#crawler-result").html($('<h2>').html(error));
    };


    var display_server_error = function ( error ) {
        $("#search-result").html($('<h2>').html(error));
    };

    function parseDate(input) {
        var parts = input.match(/(\d+)/g);
        return new Date(parts[0], parts[1] - 1, parts[2], parts[3], parts[4], parts[5]);
    }

    function display_search_error(message){
        $("#search-result").html(message);
    }

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
