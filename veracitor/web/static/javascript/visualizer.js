/**
    Visualizes an interactive network representation of a trust network, rel-
    ative to a Producer object.

    The network will be interactive in the way that a user can select a node
    other than the source node by clicking with the mouse. A visualized
    network will be visible with a specific Producer as the source node. Vi-
    sualizes a limited trust network from a bigger trust network relative to a
    specific producer.
    @constructor
 */
var Visualizer = function () {

    var holder = document.getElementById('network-holder');
    window.cy;

    /**
       Initialize the visualizer; Initialize cytoscape.
     */
    (function () {
        $('#network-graph').cytoscape({
            ready: function () {
                cy = this;

                // Generate and display a test graph
                draw_graph(generate_data(20, 5, 5));
            },
            style: cytoscape.stylesheet()
                .selector("node")
                .css({
                    "content": "data(id)",
                    "shape": "data(shape)",
                    "border-width": 3,
                    "background-color": "#DDD",
                    "border-color": "#555"
                })
                .selector("edge")
                .css({
                    "width": "mapData(weight, 0, 100, 1, 4)",
                    "target-arrow-shape": "triangle",
                    "source-arrow-shape": "circle",
                    "line-color": "#444"
                })
                .selector(":selected")
                .css({
                    "background-color": "#000",
                    "line-color": "#000",
                    "source-arrow-color": "#000",
                    "target-arrow-color": "#000"
                })
                .selector(".ui-cytoscape-edgehandles-source")
                .css({
                    "border-color": "#5CC2ED",
                    "border-width": 3
                })
                .selector(".ui-cytoscape-edgehandles-target, node.ui-cytoscape-edgehandles-preview")
                .css({
                    "background-color": "#5CC2ED"
                })
                .selector("edge.ui-cytoscape-edgehandles-preview")
                .css({
                    "line-color": "#5CC2ED"
                })
                .selector("node.ui-cytoscape-edgehandles-preview, node.intermediate")
                .css({
                    "shape": "rectangle",
                    "width": 15,
                    "height": 15
                })
        });
    })();

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
    this.visualize_producer_in_network = function (sourceNode, depth) {
        // TODO
    };

    /**
        Visualizes the given trust network.
     */
    this.visualize_trust_network = function (network) {
        // TODO
    };

    /**
        Generates some test graph data.
        @param nodes The number of generated nodes.
        @param tags The number of tag objects.
        @param maxNodes The maximum number of connections for one node (?).
     */
    var generate_data = function (nodes, tags, maxNodes) {
        var i, j, k,
            my_nodes, my_tags,
            rnd_nodes, rnd_tags,
            rnd_n, rnd_t,
            data;

        selectedNode = null;

        data = {};

        for(i = 0; i < nodes; i++) {
            data[i] = {};
            my_nodes = [i];
            rnd_nodes = Math.floor(Math.random() * maxNodes) + 1;

            for(j = 0; j < rnd_nodes; j++) {
                do {
                    rnd_n = Math.floor(Math.random() * (Math.random() > 0.2 ? rnd_nodes + 1 : nodes));
                } while(my_nodes.indexOf(rnd_n) >= 0);
                my_nodes.push(rnd_n);

                data[i][rnd_n] = {};
                my_tags = [];
                rnd_tags = Math.floor(Math.random() * (tags - 1)) + 1;

                for(k = 0; k < rnd_tags; k++) {
                    do {
                        rnd_t = Math.floor(Math.random() * tags);
                    } while(my_tags.indexOf(rnd_t) >= 0);
                    my_tags.push(rnd_t);

                    data[i][rnd_n][rnd_t] = Math.random();
                }
            }
        }

        return data;
    }

    /**
        Draws a graph representation given the data.
        @param data The data, on the form specified by the function generateData.
     */
    var draw_graph = function (data) {
        var nodes = [];
        var edges = [];
        var from, to, size;

        for(from in data) {
            size = 0;
            for(to in data[from]) {
                edges.push({
                    group: 'edges',
                    data: {
                        id: 'n'+from+'-n'+to,
                        source: 'n'+from,
                        target: 'n'+to
                    }
                });
                size += 1;
            }

            nodes.push({
                group: 'nodes',
                data: {
                    id: 'n'+from,
                    weight: size
                },
                position: {
                    x: 0,
                    y: 0
                }
            });
        }

        cy.add(nodes);
        cy.add(edges);

        cy.fit(cy.nodes());
        cy.layout({
            name: 'random'
        });
    }

};
