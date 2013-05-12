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
    var visualizer = new Visualizer(network_controller);
    var network_info;

    var global_tag = null;
    var selected_producer = null;
    var selected_tag = null;
    var user;

    /**
       This function is called by the super controller when the tab is opened.
     */
    this.on_tab_active = function () {

    };

    /**
       Initialize variables and events.
     */
    var initialize = function () {
        network_info = $('#network-graph > .info');

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

        $('#network_rate_producer > .button').click(function (evt) {
            var tag = $('#rate-producer-tag > option:selected').val();
            var rating = $('#network_rate_producer > .rating > option:selected').html();

            if (selected_producer !== null) {
                rate_producer(vera.user_name, selected_producer.name, tag, rating);
            }
        });

        $('#compute-trust').click( function(evt){
            var tag = $('#compute-trust-tag > option:selected').val();

            if (selected_producer !== null) {
                request_tidaltrust_value(vera.user_name, selected_producer.name, tag);
            }
        });

        /**
           Toggle tip-text when clicking question mark icons. Needs the structure of the
           dom to be like this:

           <p>
             text <infobutton>
           </p>
           <div tip-text></div>
         */
        $('.network-info-piece span.question-mark').click(function(evt){
            $(this).parent().next().toggle();
        });

        /**
           Fill the tag select dropdown with tags.
         */
        global_tag = vera.const.tags[0];
        for (var t in vera.const.tags) {
            $(".tag-dropdown")
                .append($('<option>')
                        .attr('value', vera.const.tags[t])
                        .html(vera.const.tags[t]));
        }

        /**
         * Init autocomplete.
         */
        $( "#tag-autocomplete" ).autocomplete({
            source: vera.const.tags
        });

        /**
           Fire event when a new tag is selected.
         */
        $('#global-tags').change(on_global_tag_change);


    };

    /**
       This function is called when the global tag is changed.
     */
    var on_global_tag_change = function (evt) {
        var tag = $(this).find(':selected').val();

        if (tag !== global_tag) {
            global_tag = tag;

            $('#rate-producer-tag').val(global_tag);
            $('#compute-trust-tag').val(global_tag);
        }
    };

    /**
       Request a TidalTrust value.
    */
    function request_tidaltrust_value(source, sink, tag) {
        // first hide old feedback
        $('#network-compute-trust .feedback').hide();

        $.post('/jobs/algorithms/tidal_trust', {
            'source': source,
            'sink': sink,
            'tag': tag
        }, function (data) {
            var job_id = data['job_id'];

            controller.set_job_callback(job_id, function (data) {
                // TODO: display success/
                //console.log(data);



                if(data.result.trust !== null){
                    $('#network-compute-trust .feedback.win #trust-result')
                        .html(data.result.trust);
                    $('#network-compute-trust .feedback.win #trust-result-threshold')
                        .html(data.result.threshold);
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
        $.post('/jobs/network/path', {
            'source': vera.user_name,
            'target': prod,
            'tag': global_tag || ''
        }, function (data) {
            network_controller.display_producer_information(data.path.target);

            if (data.path.nodes.length > 0) {
                hide_network_information();

                selected_producer = data.path.target;

                visualizer.visualize_path_in_network(data.path.source.name,
                                                     data.path.target.name,
                                                     data.path.nodes,
                                                     data.path.ghosts,
                                                     data.path.tag);
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

        if (prod.infos.length > 0) {
            var ul = $('<ul>');
            for (var i = 0; i < prod.infos.length; i++) {
                if (prod.infos[i] !== null) { // initially an issue in the database
                    ul.append($('<li>')
                              .append($('<p>').html(prod.infos[i].title))
                              .append($('<a>').attr('href', prod.infos[i].url).html(prod.infos[i].url))
                              .append(get_rating_dropdown_html())
                              .append($('<input>').attr({
                                  'type': 'button',
                                  'value': 'Rate information'
                              }).click((function ( url ) {
                                  return function ( evt ) {
                                      var rating = $(this).parent().find(':selected').html();
                                      rate_information(url, rating);
                                  };
                              })(prod.infos[i].url))));
                }
            }
            $('#network-info-view .informations').html(ul);
        } else {
            $('#network-info-view .informations').html($('<p>').html(vera.const.network.no_information));
        }

        $(".feedback").hide();
        $(".tip-text").hide();
    };

    var rate_producer = function ( source, target, tag, rating ) {
        $.post('/jobs/network/rate/producer', {
            'source': source,
            'target': target,
            'tag': tag,
            'rating': rating,
        }, function ( data ) {
            network_controller.visualize_producer_in_network(data.target.name);
        }).fail(function ( data ) {
            // TODO
        });
    };

    var rate_information = function ( url, rating ) {
        $.post('/jobs/network/rate/information', {
            'prod': vera.user_name,
            'url': url,
            'rating': rating
        }, function (data) {
            // TODO: display success/fail
        }).fail(function (data) {
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

    // Initialize this controller
    initialize();

}
