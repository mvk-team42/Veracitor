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
var Visualizer = function (controller) {

    var color = {
        node: {
            select: {
                background: '#f66',
                border: '#a00'
            },
            unselect: {
                background: '#ddd',
                border: '#555'
            },
            user: {
                background: '#fb3',
                border: '#f90'
            }
        },
        edge: {
            select: {
                line: '#a00'
            }
        }
    };

    var holder = document.getElementById('network-holder');
    window.cy;

    /**
       Initialize the visualizer; Initialize cytoscape.
     */
    (function () {
        $('#network-graph').cytoscape({
            ready: function () {
                cy = this;

                cy.on('click', 'node', node_click_event);
                cy.on('layoutstop', function () {
                    cy.nodes().unlock();
                });
            },
            style: cytoscape.stylesheet()
                .selector("node")
                .css({
                    "content": "data(id)",
                    "shape": "data(shape)",
                    "border-width": 3,
                    "background-color": color.node.unselect.background,
                    "border-color": color.node.unselect.border
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
    this.visualize_producer_in_network = function (prod, neighbors, depth) {
        var i, j;
        var nodes = [];
        var edges = [];

        for(i in neighbors) {
            nodes.push({
                'group': 'nodes',
                'data': {
                    'id': neighbors[i].name,
                    'data': neighbors[i]
                }
            });

            for(j in neighbors[i].source_ratings) {
                if (typeof neighbors[neighbors[i].source_ratings[j].name] !== 'undefined') {
                    edges.push({
                        'group': 'edges',
                        'data': {
                            'id': neighbors[i].name + '-' + neighbors[i].source_ratings[j].name,
                            'source': neighbors[i].name,
                            'target': neighbors[i].source_ratings[j].name
                        }
                    });
                }
            }
        }

        console.log(nodes);
        console.log(edges);

        cy.elements().remove();
        cy.add(nodes);
        cy.add(edges);

        cy.nodes('#' + prod.name).css({
            'background-color': color.node.select.background,
            'border-color': color.node.select.border
        });

        for(i = 0; i < neighbors.length - 1; i += 1) {
            cy.edges('[source="' + neighbors[i].name + '"][target="' + neighbors[i + 1].name + '"]').css({
                'line-color': color.edge.select.line,
                'width': 2
            });
        }

        cy.nodes('#' + session.user.name).css({
            'background-color': color.node.user.background,
            'border-color': color.node.user.border
        });

        cy.fit(cy.nodes());
        cy.layout({
            'name': 'arbor'
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
    this.visualize_path_in_network = function (source, target, path, ghosts) {
        var i, j;
        var existing_nodes = [];
        var nodes = [];
        var edges = [];

        for(i in path) {
            nodes.push({
                'group': 'nodes',
                'data': {
                    'id': path[i].name,
                    'data': path[i]
                }
            });
            existing_nodes.push(path[i].name);

            for(j in path[i].source_ratings) {
                edges.push({
                    'group': 'edges',
                    'data': {
                        'id': path[i].name + '-' + path[i].source_ratings[j].name,
                        'source': path[i].name,
                        'target': path[i].source_ratings[j].name
                    }
                });
            }
        }

        for (i in ghosts) {
            nodes.push({
                'group': 'nodes',
                'data': {
                    'id': ghosts[i]
                }
            });
        }

        cy.elements().remove();
        cy.add(nodes);
        cy.add(edges);

        for (i = 0; i < existing_nodes.length; i += 1) {
            cy.nodes('#' + existing_nodes[i]).css({
                'background-color': color.node.select.background,
                'border-color': color.node.select.border,
                'shape': 'ellipse'
            });
            if (i < existing_nodes.length - 1) {
                cy.edges('[source="' + existing_nodes[i] + '"][target="' + existing_nodes[i + 1] + '"]').css({
                    'line-color': color.edge.select.line,
                    'width': 2
                });
            }
        }

        for (i in ghosts) {
            cy.nodes('#' + ghosts[i]).addClass('ghost');
        }

        cy.nodes('#' + source).css({
            'background-color': color.node.user.background,
            'border-color': color.node.user.border,
            'shape': 'roundrectangle'
        });

        cy.layout({
            'name': 'arbor'
        });
    };

    /**
        Visualizes the given trust network.
     */
    this.visualize_trust_network = function (network) {
        // TODO
    };

    var node_click_event = function (evt) {
        var node = this;

        if (node.hasClass('ghost')) {
            $.post('/jobs/network/neighbors', {
                'name': node.id(),
                'depth': 1
            }, function (data) {
                var nodes = [];
                var edges = [];
                var ghosts = [];

                for (i in data.neighbors) {
                    nodes.push({
                        'group': 'nodes',
                        'data': {
                            'id': data.neighbors[i].name,
                            'data': data.neighbors[i]
                        }
                    });

                    for (j in data.neighbors[i].source_ratings) {
                        edges.push({
                            'group': 'edges',
                            'data': {
                                'id': data.neighbors[i].name + '-' + data.neighbors[i].source_ratings[j].name,
                                'source': data.neighbors[i].name,
                                'target': data.neighbors[i].source_ratings[j].name
                            }
                        });

                        if (cy.nodes('#' + data.neighbors[i].source_ratings[j].name).empty()) {
                            nodes.push({
                                'group': 'nodes',
                                'data': {
                                    'id': data.neighbors[i].source_ratings[j].name
                                }
                            });
                            ghosts.push(data.neighbors[i].source_ratings[j].name);
                        }
                    }
                }

                cy.nodes().lock();
                cy.add(nodes);
                cy.add(edges);

                for (i in ghosts) {
                    cy.nodes('#' + ghosts[i]).addClass('ghost');
                }
                node.removeClass('ghost');

                cy.layout();
            }).fail(function (data) {
                console.log(data);
            });
        }
    };

};
