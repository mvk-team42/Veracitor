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
var Visualizer = function (super_controller, network_controller) {

    // A reference to this object
    var visualizer = this;
    // Show or hide ratings in network graph
    var show_ratings = true;

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
            },
            verauser: {
                background: '#3bf',
                border: '#09f'
            },
            ghost: {
                background: '#fff',
                border: '#aaa'
            }
        },
        edge: {
            select: {
                line: '#a00'
            },
            unselect: {
                line: '#444'
            },
            ghost: {
                line: '#aaa'
            }
        }
    };

    window.cy;

    /**
       Initialize the visualizer; Initialize cytoscape.
     */
    (function () {
        $('#cytoscape').cytoscape({
            ready: function () {
                cy = this;

                cy.on('click', 'node', node_click_event);
                /*
                cy.on('layoutstop', function () {
                    cy.nodes().unlock();
                });
                */

                // Fixes vanishing graph issue when resizing the window
                $(window).resize(function () {
                    // notify the renderer that the viewport has changed
                    cy.notify({
                        'type': 'viewport'
                    });
                });
            },
            style: cytoscape.stylesheet()
                .selector("node")
                .css({
                    "content": "data(id)",
                    "shape": "data(shape)",
                    "border-width": 3,
                    "background-color": color.node.unselect.background,
                    "border-color": color.node.unselect.border,
                    "text-outline-color": "#fff",
                    "text-outline-width": 1
                })
                .selector("edge")
                .css({
                    "width": "mapData(weight, 0, 100, 1, 4)",
                    "target-arrow-shape": "triangle",
                    "source-arrow-shape": "circle",
                    "line-color": "#444",
                    "text-outline-color": "#fff",
                    "text-outline-width": 1,
                    "font-size": 20
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
       Recalculates the layout of the nodes in the graph.
     */
    this.recalculate_layout = function ( callback ) {
        if (callback) {
            cy.one('layoutstop', callback);
        }

        cy.layout({
            'name': 'arbor',
            'fit': false
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

        visualizer.recalculate_layout();
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
    this.visualize_path_in_network = function (source, target, path, ghosts, tag, callback) {
        // Remove all elements in the graph
        cy.elements().remove();

        var cyelems = get_cytoscape_elements_from_path(source,
                                                       target,
                                                       path,
                                                       ghosts,
                                                       tag);
        cy.add(cyelems.nodes);
        cy.add(cyelems.edges);

        style_elements();

        visualizer.recalculate_layout(callback);
    };

    this.visualize_paths_in_network = function (paths, tag, callback) {
        // Remove all elements in the graph
        cy.elements().remove();

        for (var i in paths) {
            var cyelems = get_cytoscape_elements_from_path(paths[i].source,
                                                           paths[i].target,
                                                           paths[i].nodes,
                                                           paths[i].ghosts,
                                                           tag);
            cy.add(cyelems.nodes);
            cy.add(cyelems.edges);
        }

        style_elements();

        visualizer.recalculate_layout(callback);
    };

    var get_cytoscape_elements_from_path = function (source, target, path, ghosts, tag) {
        var safe_src, safe_trg;
        var nodes = [];
        var edges = [];

        for (var node in path) {
            safe_src = safe(node);

            nodes.push({
                'group': 'nodes',
                'data': {
                    'id': safe_src,
                    'name': node,
                    'data': path[node]
                },
                'position': get_initial_position(),
                'classes': path[node].type_of + ' ' + 'path'
            });

            for (var key in path[node].source_ratings) {
                safe_trg = safe(key);

                if (typeof path[key] !== 'undefined') {
                    edges.push({
                        'group': 'edges',
                        'data': {
                            'id': safe_src + '-' + safe_trg,
                            'source': safe_src,
                            'target': safe_trg,
                            'rating': path[node].source_ratings[key][tag] || ''
                        },
                        'classes': 'path'
                    });
                }
            }
        }

        for (var g in ghosts) {
            safe_src = safe(g);
            safe_trg = safe(ghosts[g]);

            nodes.push({
                'group': 'nodes',
                'data': {
                    'id': safe_src,
                    'name': g
                },
                'position': get_initial_position(),
                'classes': 'ghost'
            });

            edges.push({
                'group': 'edges',
                'data': {
                    'id': safe_src + '-' + safe_trg,
                    'source': safe_src,
                    'target': safe_trg,
                    'rating': ''
                },
                'classes': 'ghost'
            });
        }

        return {
            'nodes': nodes,
            'edges': edges
        };
    };

    this.fetch_neighbors = function ( name, tag, depth, callback ) {
        var id = safe(name);
        var source_node = cy.nodes('#' + id);

        $.post('/jobs/network/neighbors', {
            'name': name,
            'depth': depth
        }, function (data) {
            var safe_src, safe_trg;
            var edge_id, elem;
            var ghost_edges = {};
            var nodes = [];
            var edges = [];

            source_node.removeClass('ghost');

            for (var node in data.neighbors) {
                safe_src = safe(node);
                elem = cy.nodes('#' + safe_src);

                if (elem.empty()) {
                    nodes.push({
                        'group': 'nodes',
                        'data': {
                            'id': safe_src,
                            'name': node,
                            'data': data.neighbors[node]
                        },
                        'position': get_initial_position(),
                        'classes': 'ghost'
                    });
                }

                for (var key in data.neighbors[node].source_ratings) {
                    if (typeof data.neighbors[key] !== 'undefined') {
                        safe_trg = safe(key);
                        edge_id = safe_src + '-' + safe_trg;
                        elem = cy.edges('#' + edge_id);

                        // Check if the edge does not exist
                        if (elem.empty()) {
                            // Check if the edge is a ghost edge
                            if (cy.nodes('#' + safe_src).empty() ||
                                cy.nodes('#' + safe_trg).empty() ||
                                cy.nodes('#' + safe_src).hasClass('ghost') ||
                                cy.nodes('#' + safe_trg).hasClass('ghost')) {

                                // Check if the edge has already been added
                                if (cy.edges('#' + safe_trg + '-' + safe_src).empty() &&
                                    (typeof ghost_edges[safe_src] === 'undefined' ||
                                     typeof ghost_edges[safe_src][safe_trg] === 'undefined')) {

                                    edges.push({
                                        'group': 'edges',
                                        'data': {
                                            'id': edge_id,
                                            'source': safe_src,
                                            'target': safe_trg,
                                            'rating': ''
                                        },
                                        'classes': 'ghost'
                                    });

                                    // Add the edge
                                    if (typeof ghost_edges[safe_src] === 'undefined') {
                                        ghost_edges[safe_src] = {};
                                    }
                                    ghost_edges[safe_src][safe_trg] = true;
                                    if (typeof ghost_edges[safe_trg] === 'undefined') {
                                        ghost_edges[safe_trg] = {};
                                    }
                                    ghost_edges[safe_trg][safe_src] = true;
                                }
                            } else {
                                edges.push({
                                    'group': 'edges',
                                    'data': {
                                        'id': edge_id,
                                        'source': safe_src,
                                        'target': safe_trg,
                                        'rating': data.neighbors[node].source_ratings[key][tag] || ''
                                    }
                                });

                                // Remove any related ghost edge
                                elem = cy.edges('#' + safe_trg + '-' + safe_src);
                                if (!elem.empty() && elem.hasClass('ghost')) {
                                    elem.remove();
                                }
                            }

                        // If the edge exist
                        } else {
                            // Remove any related ghost edges
                            if (!cy.nodes('#' + safe_src).hasClass('ghost') &&
                                !cy.nodes('#' + safe_trg).hasClass('ghost') &&
                                !elem.parallelEdges('.ghost').empty()) {

                                // Update the rating
                                elem.data('rating', data.neighbors[node].source_ratings[key][tag] || '');

                                elem.parallelEdges().css({
                                    'line-color': color.edge.unselect.line,
                                    'line-style': 'solid',
                                    'source-arrow-shape': 'circle',
                                    'target-arrow-shape': 'triangle',
                                    'width': 1
                                });
                                elem.parallelEdges().removeClass('ghost');
                            }
                        }
                    }
                }
            }

            if (nodes.length > 0) {
                // TODO: This causes display errors with arbor.js
                //cy.nodes().lock();

                cy.add(nodes);
                cy.add(edges);
            } else if (edges.length > 0) {
                cy.add(edges);
            }

            // Update source node
            source_node.data('data', data.neighbors[source_node.data().name]);
            source_node.addClass(data.neighbors[source_node.data().name].type_of);
            source_node.css({
                'background-color': color.node.unselect.background,
                'border-color': color.node.unselect.border,
                'border-width': 3
            });

            style_elements();

            // Display producer information
            network_controller.display_producer_information(source_node.data().data);

            visualizer.recalculate_layout(callback);
        }).fail(function (data) {
            // TODO: Handle request fail
            console.log(data);

            if (callback) {
                callback();
            }
        });
    };

    /**
       Styles all nodes and edges in the graph.
     */
    var style_elements = function () {
        cy.nodes().css({
            'content': 'data(name)'
        });

        if (show_ratings) {
            cy.edges().css({
                'content': 'data(rating)'
            });
        } else {
            cy.edges().css({
                'content': ''
            });
        }

        // Highlight the path nodes and edges
        cy.nodes('.path').css({
            'background-color': color.node.select.background,
            'border-color': color.node.select.border,
            'shape': 'ellipse'
        });
        cy.edges('.path').css({
            'line-color': color.edge.select.line,
            'width': 2
        });

        // Style the ghost nodes and edges
        cy.nodes('.ghost').css({
            'background-color': color.node.ghost.background,
            'border-color': color.node.ghost.border,
            'border-width': 1
        });
        cy.edges('.ghost').css({
            'line-color': color.edge.ghost.line,
            'line-style': 'dashed',
            'source-arrow-shape': 'none',
            'target-arrow-shape': 'none',
            'width': 1
        });

        // Style the user nodes
        cy.nodes('.User').css({
            'background-color': color.node.user.background,
            'border-color': color.node.user.border,
            'shape': 'rectangle'
        });

        // Style the user
        cy.nodes('[name="' + vera.user_name + '"]').css({
            'background-color': color.node.verauser.background,
            'border-color': color.node.verauser.border
        });
    };

    var get_initial_position = function () {
        return {
            'x': 0,
            'y': 0
        };
    };

    this.clear_graph = function () {
        cy.elements().remove();
    };

    this.show_ratings = function ( bool ) {
        show_ratings = bool;

        if (show_ratings) {
            cy.edges().css({
                'content': 'data(rating)'
            });
        } else {
            cy.edges().css({
                'content': ''
            });
        }
    };

    /**
       Returns a safe string for selectors with white spaces
       replaced by underscores.
     */
    var safe = function ( s ) {
        return s.replace(/(\s|#|\.|\|)/g, '_');
    };

    var node_click_event = function (evt) {
        var node = this;

        if (typeof node.hasClass('ghost') !== 'undefined') {
            var loader = super_controller.new_loader($('#network-graph'), {
                'margin': '5px'
            });

            visualizer.fetch_neighbors(node.data().name,
                                       network_controller.get_global_tag(),
                                       1,
                                       function () {
                                           loader.delete();
                                       });
        } else {
            network_controller.display_producer_information(node.data().data);
        }
    };

};
