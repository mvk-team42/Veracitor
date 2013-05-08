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

    var visualizer = new Visualizer(this);

    /**
       This function is called by the super controller when the tab is opened.
     */
    this.on_tab_active = function () {
	add_event_handlers();
    };

    function add_event_handlers() {
	$('#add-to-group').click(function(evt) {
	    $.post('/jobs/network/add_to_group',
		   {
		       'group_name' : $('#group_name').val(),
		       'producer' : $('h1.title').text()
		       
		   }, function(data) {
		   });
	});
    }

    /**
       Request a SUNNY value.
    */
    function request_sunny_value(source, sink, tag) {
         $.post('/jobs/algorithms/tidal_trust', {
            'source': source,
            'sink': sink,
            'tag': tag
        }, function (data) {
            var job_id = data['job_id'];

            controller.set_job_callback(job_id, function (data) {
                console.log(data.result);

                $('#calculated-trust').html(data.result.trust);
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
    this.visualize_producer_in_network = function (prod, depth) {
        var network_controller = this;

        $.post('/jobs/network/path', {
            'source': vera.user_name,
            'target': prod.name
        }, function (data) {
            network_controller.display_producer_information(prod);

            console.log(data);

            visualizer.visualize_path_in_network(data.path.source,
                                                 data.path.target,
                                                 data.path.nodes,
                                                 data.path.ghosts);
        }).fail(function (data) {
            console.log(data);
        });

        /*
        $.post('/jobs/network/neighbors', {
            'name': session.user.name,
            'depth': depth
        }, function (data) {
            network_controller.display_producer_information(prod);

            console.log(data);

            visualizer.visualize_producer_in_network(prod, data.neighbors, depth);
        }).fail(function (data) {
            console.log(data);
        });
        */
    };

    /**
       Displays information about the given producer.
     */
    this.display_producer_information = function (prod) {
        // A reference to this controller
        var network_controller = this;

        $('#network-info-view .title').html(prod.name);
        $('#network-info-view .description').html(prod.description);
        $('#network-info-view .url').html($('<a>').attr('href', prod.url).html(prod.url));
        $('#network-info-view .type').html(prod.type_of);

        var ul = $('<ul>');
        for (var i in prod.infos) {
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
                              network_controller.rate_information(url, rating);
                          };
                      })(prod.infos[i].url))));
        }
        $('#network-info-view .informations').html(ul);
    };

    this.rate_information = function ( url, rating ) {
        $.post('/jobs/network/rate_information', {
            'prod': vera.user_name,
            'url': url,
            'rating': rating
        }, function (data) {
            console.log('Rated!');
        }).fail(function (data) {
            console.log(data);
        });
    };

    var get_rating_dropdown_html = function () {
        var select = $('<select>').addClass('rating');;

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

}
