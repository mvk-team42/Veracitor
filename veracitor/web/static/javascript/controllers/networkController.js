/**
    Displays information about a specific Producer, User or Information ob-
    ject in the database. Visualizes a portion of the system database via the
    WebUI.NetworkView.Visualizer.

    The view is divided into two distinct areas. One area contains detailed
    information about the selected source node. The other area contains a
    visualization of a portion of the database relative to the source node, as
    well as tools to alter the visualization of the network.
    @constructor
 */
var NetworkController = function (controller) {

    var network_controller = this;
    var visualizer = new Visualizer(controller, network_controller);
    var network_info;

    var global_tag = null;
    var selected_producer = null;
    var user;

    /**
       This function is called by the super controller
       each time the tab is opened.
     */
    this.on_tab_active = function () {

    };

    /**
       Initialize variables and events.
     */
    var initialize = function () {
        network_info = $('#network-graph > .info');

        hide_producer_information();
        display_network_information('Use the search to find producers and information.');

        $.post('/utils/get_user', {
            'user_name': vera.user_name
        }, function(data){
            user = data;

            // Generate the group select dropdown.
            for (var g in user.groups){
                $("#group_name").append($('<option>')
                                        .attr('value', user.groups[g].name)
                                        .html(user.groups[g].name));
            }
        });


        $('#add-to-group').click(function(evt) {
            $.post('/jobs/network/add_to_group', {
                'group_name': $('#group_name').val(),
                'producer': $('h1.title').text()
            }, function(data) {
                // TODO: display success/fail
                console.log(data);
            });
        });

        $('#network_rate_producer .button').click(function (evt) {
            var tag = $('#rate-producer-tag > option:selected').val();
            var rating = $('#network_rate_producer > .rating > option:selected').html();

            if (selected_producer !== null) {
                rate_producer(vera.user_name, selected_producer.name, tag, rating);
            }
        });

        $('#compute-trust').click( function(evt){
            var tag = $('#compute-trust-tag > option:selected').val();
            var algorithm = $('#compute-trust-algorithm > option:selected').val();

            if (selected_producer !== null) {
                request_trustcalc_value(vera.user_name, selected_producer.name, tag, algorithm);
            }
        });

        /**
           Toggle tip-text when clicking question mark icons. Needs the structure of the
           dom to be like this:

           <p>
             text <infobutton>
           </p>
           <p tip-text></p>
         */
        $('span.question-mark').click(function(evt){
            $(this).parent().next().toggle();
        });

        /**
           Fill the tag select dropdown with tags.
         */
        global_tag = '';
        $("#network-toolbox .tag-dropdown")
            .append($('<option>')
                    .attr('value', global_tag)
                    .html('-'));
        for (var t in vera.const.tags) {
            $(".tag-dropdown")
                .append($('<option>')
                        .attr('value', vera.const.tags[t])
                        .html(vera.const.tags[t]));
        }

        /**
         * Init autocomplete.
         */
        /*
        $( "#tag-autocomplete" ).autocomplete({
            source: vera.const.tags
        });
        */

        /**
           Fire event when a new tag is selected.
         */
        $('#global-tags').change(on_global_tag_change);

        $('#network-toolbox-layout').click(function (evt) {
            var loader = controller.new_loader($('#network-graph'), {
                'margin': '5px'
            });

            visualizer.recalculate_layout(function () {
                loader.delete();
            });
        });

        $('#network-toolbox-ratings').click(function (evt) {
            var bool = false;
            if ($(this).filter(':checked').length > 0) {
                bool = true;
            }
            visualizer.show_ratings(bool);
        });

        $('#selected-tag').html("None");

    };

    /**
       This function is called when the global tag is changed.
     */
    var on_global_tag_change = function (evt) {
        var tag = $(this).find(':selected').val();
        $('#selected-tag').html(tag);

        if (tag !== global_tag) {
            global_tag = tag;

            if (global_tag === '') {
                global_tag = null;
                $('#selected-tag').html("None");
            }

            if (global_tag !== null) {
                $('#rate-producer-tag').val(global_tag);
                $('#compute-trust-tag').val(global_tag);
            }

            if (selected_producer !== null) {
                // Update the network with the selected tag
                network_controller.visualize_producer_in_network(selected_producer.name);
            }
        }
    };

    /**
       Calculate a trust assessment value.
    */
    function request_trustcalc_value(source, sink, tag, algorithm) {
        // first hide old feedback
        $('#network-compute-trust .feedback').hide();

        // Show loader!
        var loader = controller.new_loader($('#network-compute-trust'),
                                           {'width':'16px', 'height':'16px'});

        $.post('/jobs/algorithms/'+algorithm, {
            'source': source,
            'sink': sink,
            'tag': tag
        }, function (data) {
            var job_id = data['job_id'];

            controller.set_job_callback(job_id, function (data) {
                // Go away loader!
                loader.delete();

                if(data.result.trust !== null){
                    $('#network-compute-trust .feedback.win #trust-result')
                        .html(data.result.trust);
                    $('#network-compute-trust .feedback.win #trust-result-threshold')
                        .html(data.result.threshold);
                    $('#network-compute-trust .feedback.win #trust-result-button')
                        .click((function (paths) {
                            return function (evt) {
                                visualize_paths_in_network(paths);
                            }
                        })(data.result.paths_used));
                    $('#network-compute-trust .feedback.win').show();
                }
                else {
                    $('#network-compute-trust .feedback.fail #fail-message')
                        .html(
                           // TODO: Display something interesting here?
                        );
                    $('#network-compute-trust .feedback.fail').show();
                }


            });
        })
        .fail(function () {
            $('#search-result').html('<h2>Server error.</h2>');
        });
    }

    /**
       Visualizes paths in the graph.
       @param paths The paths stored as lists in a dict object.
     */
    var visualize_paths_in_network = function (paths) {
        var loader = controller.new_loader($('#network-graph'), {
            'margin': '5px'
        });

        $.post('/jobs/network/paths_from_producer_lists', {
            'paths': JSON.stringify(paths)
        }, function (data) {
            visualizer.visualize_paths_in_network(data.paths, global_tag, function () {
                loader.delete();
            });
        }).fail(function (data) {
            // TODO: Handle server error
        });
    };

    /**
        Creates an interactive visualization network of the trust ratings
        directly or indirectly associated with the given Producer (source
        node) within the GlobalNetwork. Only nodes that have a trust
        relation with the source node at a maximum of depth nodes away
        from the source node will be visualized. If -1 is input as depth
        there will be no restrictions as to how close a node has to be to
        the source node in order to be part of the visualization (that is the
        entire network will be visualized).
     */
    this.visualize_producer_in_network = function (prod) {
        var loader = controller.new_loader($('#network-graph'), {
            'margin': '5px'
        });

        $.post('/jobs/network/path', {
            'source': vera.user_name,
            'target': prod,
            'tag': global_tag || ''
        }, function (data) {
            network_controller.display_producer_information(data.path.target);

            if (typeof data.path.nodes[data.path.source.name] !== 'undefined') {
                hide_network_information();

                selected_producer = data.path.target;

                visualizer.visualize_path_in_network(data.path.source.name,
                                                     data.path.target.name,
                                                     data.path.nodes,
                                                     data.path.ghosts,
                                                     data.path.tag,
                                                     function () {
                                                         loader.delete();
                                                     });
            } else {
                display_network_information('No path found');
            }
        }).fail(function (data) {
            // TODO: display fail
        });
    };

    /**
       Displays information about the given producer.
     */
    this.display_producer_information = function (prod) {
        // A reference to this controller
        var network_controller = this;

        selected_producer = prod;

        $('#network-info-view .title').html(prod.name);
        $('#network-info-view .description').html(prod.description);
        $('#network-info-view .url').html($('<a>').attr('href', prod.url).html(prod.url));
        $('#network-info-view .type').html(prod.type_of);

        // Display producer ratings
        if (typeof user.source_ratings[prod.name] !== 'undefined') {
            var ul = $('<ul>');

            if (global_tag !== '') {
                if (typeof user.source_ratings[prod.name][global_tag] !== 'undefined') {
                    ul.append($('<li>')
                              .append($('<p>')
                                      .append($('<b>').html('Tag:'))
                                      .append(global_tag)
                                      .append($('<b>').html('Rating:'))
                                      .append(user.source_ratings[prod.name][global_tag])));
                    $('#network-info-view .user-ratings').html(ul);
                } else {
                    $('#network-info-view .user-ratings').html($('<p>').html(vera.const.network.no_ratings));
                }
            } else {
                for (var tag in user.source_ratings[prod.name]) {
                    ul.append($('<li>')
                              .append($('<p>')
                                      .append($('<b>').html('Tag:'))
                                      .append(tag)
                                      .append($('<b>').html('Rating:'))
                                      .append(user.source_ratings[prod.name][tag])));
                }
                $('#network-info-view .user-ratings').html(ul);
            }
        } else {
            $('#network-info-view .user-ratings').html($('<p>').html(vera.const.network.no_ratings));
        }

        // Display information objects
        if (prod.infos.length > 0) {
            var ul = $('<ul>');
            for (var i = 0; i < prod.infos.length; i++) {
                ul.append($('<li>')
                          .append($('<p>').html(prod.infos[i].title))
                          .append($('<a>').attr('href', prod.infos[i].url).html(prod.infos[i].url))
                          .append($('<p>')
                                  .append($('<b>').html(
                                      typeof user.info_ratings[prod.infos[i].url] !== 'undefined' ?
                                          'Your rating: ' + user.info_ratings[prod.infos[i].url] : 'No rating set'))
                                  .append(get_rating_dropdown_html())
                                  .append($('<input>').attr({
                                      'type': 'button',
                                      'value': 'Rate information'
                                  }).click((function ( info_prod, url ) {
                                      return function ( evt ) {
                                          var rating = $(this).parent().find(':selected').html();

                                          rate_information(info_prod, url, rating);
                                      };
                                  })(prod.name, prod.infos[i].url)))));
            }
            $('#network-info-view .informations').html(ul);
        } else {
            $('#network-info-view .informations').html($('<p>').html(vera.const.network.no_information));
        }

        $('#network-info-view > .body > .producer-information').show();
        $(".feedback").hide();
        $(".tip-text").hide();
    };

    var hide_producer_information = function () {
        $('#network-info-view > .body > .producer-information').hide();
    };

    var rate_producer = function ( source, target, tag, rating ) {
        var loader = controller.new_loader($('#network_rate_producer'), {'width':'16px', 'height':'16px'});
        $.post('/jobs/network/rate/producer', {
            'source': source,
            'target': target,
            'tag': tag,
            'rating': rating,
        }, function ( data ) {
            // Update the user object
            user = data.source;

            loader.delete();

            network_controller.display_producer_information(data.target);

            network_controller.visualize_producer_in_network(data.target.name);
        }).fail(function ( data ) {
            // TODO
        });
    };

    var rate_information = function ( info_prod, url, rating ) {
        $.post('/jobs/network/rate/information', {
            'source_prod': vera.user_name,
            'info_prod': info_prod,
            'url': url,
            'rating': rating
        }, function (data) {
            // Update the user object
            user = data.source_prod;

            network_controller.display_producer_information(data.info_prod);
        }).fail(function (data) {
            console.log(data);
            // TODO: display fail
        });
    };

    var get_rating_dropdown_html = function () {
        var select = $('<select>').addClass('rating');

        for (var i = 1; i <= 5; i += 1) {
            select.append($('<option>').attr('value', i).html(i));
        }

        return select;
    };

    /**
        Visualizes the given trust network.
     */
    this.visualize_trust_network = function (network) {
        visualizer.visualize_trust_network(network);
    };

    var display_network_information = function ( info ) {
        network_info.css('display', 'block');
        network_info.find('.content').html($('<p>').html(info));

        try {
            visualizer.clear_graph();
        } catch (exc) {
            // cytoscape has not yet loaded
        }
    };

    var hide_network_information = function () {
        network_info.css('display', 'none');
    };

    /**
       Returns the global network tag.
       @return The global network tag.
     */
    this.get_global_tag = function () {
        return global_tag;
    };

    // Initialize this controller
    initialize();

}
