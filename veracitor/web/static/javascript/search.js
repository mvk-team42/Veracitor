    /* OLD VARIABLES */
    var menu, arrows, search, network, account, info, svg;
    var advanced;
    var easing_fast = 50;
    
    var info_data;
    var current_search_data;
    
    var searchType = {
        "web" : 0,
        "database" : 1
    };
    var currentSearch;
    
    // d3 graph variables
    var color, force;
    
        /* TODO CHECK THIS CODE */
        advanced = false;
        
        $("#free-text-search > .search-area").keydown(function (evt) {
            if(evt.keyCode == 13) {
                $("#free-text-search input[name=search]").click();
            }
        });
        
        $("#source-tag-search > .search-area").keydown(function (evt) {
            if(evt.keyCode == 13) {
                $("#source-tag-search input[name=search]").click();
            }
        });
        
        // search areas
        $("#search-type-select input[name=web]").click(function (evt) {
            $(this).addClass("active");
               $("#search-type-select input[name=database]").removeClass("active");

            $("#database-search").slideUp(easing_fast);
            
            $("input[name=search-button]").attr("value", "Web search");
            $("#search-info").html("Perform a web search for sources and publications.");
            
            currentSearch = searchType.web;
        });
        $("#search-type-select input[name=database]").click(function (evt) {
            $(this).addClass("active");
               $("#search-type-select input[name=web]").removeClass("active");
               
            $("#database-search").slideDown(easing_fast);
            
            $("input[name=search-button]").attr("value", "Database search");
            $("#search-info").html("Perform a local search in the database for sources or publications.");
            
            currentSearch = searchType.database;
        });
        
        currentSearch = searchType.web;
        $("#search-type-select input[name=web]").click();
        $("#database-search").hide();
        
        setupSearch();
        
/* FUNCTIONS */


    function setupSearch() {
        // source and tag search
        $("input[name=search-button]").click(function (evt) {
        switch(currentSearch) {
        case searchType.database:
            var i, tag;
            var request = {};
            
            tag = $('input[name=search-text]');
            request['source'] = tag.val();
            
            tag = $('#source-tag-search input[type=checkbox]');
            for(i in tag) {
                if(tag.get(i).checked) {
                    if(!request['tag']) {
                        request['tag'] = [];
                    }
                       request['tag'].push(tag.get(i).name);
                   }
            }
            if(request['tag']) {
                request['tag'] = request['tag'].toString().replace(/\,/g,'+');
            }
            
            sendRequest(request);
        break;
        case searchType.web:
            sendRequest({
                'free_text' : $("input[name=search-text]").val()
            });
        break;
        }});
    }
    
    function sendRequest(request) {
        var i, j, _tags, data = [];
        
        // For javascript
        if(request["source"] != undefined) {
            if(request["tag"] != undefined) {
                _tags = request["tag"].split("+");
                
                for(i in Database.sources) {
                    if(~Database.sources[i].name.toLowerCase().indexOf(request["source"].toLowerCase())) {
                        for(j in _tags) {
                            if(~Database.sources[i].tag.toLowerCase().indexOf(_tags[j].toLowerCase())) {
                                data.push({
                                    "fields" : Database.sources[i]
                                });
                                
                                break;
                            }
                        }
                    }
                }
            } else {
                for(i in Database.sources) {
                    if(~Database.sources[i].name.toLowerCase().indexOf(request["source"].toLowerCase())) {
                        data.push({
                            "fields" : Database.sources[i]
                        });
                    }
                }
            }
        } else if(request["free_text"] != undefined) {
            for(i in Database.publications) {
                if(~Database.publications[i].title.toLowerCase().indexOf(request["free_text"].toLowerCase())) {
                    data.push({
                        "fields" : Database.publications[i]
                    });
                }
            }
        }
    
        //$.get("/search", request, function (data) {
            var _body, _row, _table, _height, _oldheight, _scroll;
            
            _table = $('#search-result table');
            _table.html("");
            
            if(data.length){
                current_search_data = data;

                if(request.source != undefined){
                    _table.append(
                    $("<thead></thead>")
                        .append($("<tr></tr>")
                            .append($("<th>Title</th>"))
                            .append($("<th>Type</th>"))
                            .append($("<th>Tag</th>"))
                            .append($("<th>Rating</th>").addClass("rating"))));
                }/* else {
                    _table
                        .before($("<p></p>")
                            .append($("<p></p>")
                                .html("Sort by:"))
                            .append($("<label></label>")
                                .html("<input type='radio' name='web_sort' checked='true'></input> Publications"))
                            .append($("<label></label>")
                                .html("<input type='radio' name='web_sort'></input> Sources")));
                }*/
                
                _body = $("<tbody></tbody>");
                
                for (i=0;i<data.length;i++) {
                    if(request.free_text != undefined) {
                        _table.append(
                        $("<tr></tr>").attr("index", i)
                            .append($("<td></td>")
                                .append($("<p></p>").addClass("title").html(data[i].fields.title))
                                .append($("<p></p>").addClass("source").html(data[i].fields.source))
                                .append($("<p></p>").addClass("summary").html(data[i].fields.summary))
                                .append($("<p></p>").addClass("href")
                                    .append($("<a></a>").attr("href", data[i].fields.href).html(data[i].fields.href)))
                                .append($("<p></p>").addClass("rating").html(data[i].fields.trustworthy))));
                    } else {
                        _row = $("<tr></tr>").attr("index", i).addClass("clickable")
                            .append($("<td>Title</td>").html(data[i].fields.name))
                            .append($("<td>Type</td>").html(data[i].fields.source_type))
                            .append($("<td>Tag</td>").html(data[i].fields.tag));
                        
                        if(data[i].fields.rating > 1) {
                            _row.append(
                            $("<td></td>").addClass("rating user-rating")
                                .append($("<div></div>").html(data[i].fields.rating)));
                        } else {
                            _row.append(
                            $("<td></td>").addClass("rating")
                                .append($("<div></div>").html(1)));
                        }
                        
                        _body.append(_row);
                    }
                }
                
                _body.find("tr").click(searchResultClick);
                _table.append(_body);
            } else {
                _table.append(
                $("<thead></thead>")
                    .append($("<tr></tr>")
                        .append($("<th></th>").html("Couldn't find anything."))));
            }
        //});
        
        setTimeout(scrollDown, 50);
    }
    
    function scrollDown () {
        var _content = $("#search > .content"),
            _offset = $("#search-result")[0].offsetTop;
        
        if(_content[0].scrollHeight - _offset < _content.height()) {
            _offset = _content[0].scrollHeight - _content.height() - parseInt(_content.css("padding-top")) - parseInt(_content.css("padding-bottom"));
        }
        
        _content.animate({
            "scrollTop" : _offset
        }, "slow");
    }
    
    function searchResultClick(evt){
        data = current_search_data[evt.currentTarget.getAttribute('index')];
    
        $("#network-info-view .title").html(data.fields.name);
        $("#network-info-view .description").html(data.fields.description);
        $("#network-info-view .type").html(data.fields.source_type);
        $("#network-info-view .tags").html(data.fields.tag);
        $("#network-info-view .rating").html(data.fields.rating);
        
        networkClick();
    }