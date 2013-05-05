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

    window.cy;

    /**
       Initialize the visualizer; Initialize cytoscape.
     */
    (function () {
        $('#cytoscape').cytoscape({
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
            'border-width': 0,
            'shape': 'rectangle'
        });
        var animation = new Animation('/static/images/veracitor_logo_2.png', 2, 2, '0:3', 1000);
        animation.animate(cy.nodes('#' + source));

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

    var Animation = function ( url, w, h, frames, time ) {
        var images;
        var animation_cycle;
        var animation_frame;
        var animating;
        var frame_time;
        var node;

        var timer = {
            'delta': 0,
            'time': 0,
            'millis': +new Date,
            'reset': function () {
                this.time = 0;
                this.millis = +new Date;
            },
            'requestAnimationFrame': function ( callback ) {
                var time = - this.millis + (this.millis = +new Date);
                this.time += time;
                this.delta = (time / 1000) % 1;
                window.requestAnimationFrame(callback);
            }
        };

        var ready = false;
        var ready_queue = [];
        var image = new Image();
        image.onload = function () {
            divide_image(this);
            parse_animation_cycle(frames);

            ready = true;
            for (var i in ready_queue) {
                ready_queue[i]();
            }
        };
        image.src = url;

        var divide_image = function ( img ) {
            var dx = img.width / w;
            var dy = img.height / h;

            if (dx % 1 > 0 || dy % 1 > 0) {
                throw 'Image could not be divided.';
            }

            var canvas = document.createElement('canvas');
            canvas.width = dx;
            canvas.height = dy;
            var ctx = canvas.getContext('2d');
            images = new Array(w * h);
            // Divide the image and save each piece
            for (var j = 0; j < h; j += 1) {
                for (var i = 0; i < w; i += 1) {
                    ctx.clearRect(0, 0, dx, dy);
                    ctx.drawImage(img, i * dx, j * dy, dx, dy, 0, 0, dx, dy);
                    images[j * w + i] = canvas.toDataURL();
                }
            }
        };

        var parse_animation_cycle = function ( frames ) {
            animation_cycle = [];
            var s = frames.split(' ');
            var range, from, to, step;
            for (var i in s) {
                if (!s[i].match(/(\d+)(:\d+)?/g)) {
                    throw 'Could not parse animation frame cycle.';
                }
                range = s[i].split(':');
                from = parseInt(range[0]);
                if (range.length > 1) {
                    to = parseInt(range[1]);
                } else {
                    to = from;
                }
                if (to > from) {
                    step = 1;
                } else {
                    step = -1;
                }

                for (var j = from; j != to + step; j += step) {
                    animation_cycle.push(j);
                }
            }
            // Set the time for each image
            frame_time = time / animation_cycle.length;
        };

        var animation_loop = function () {
            if (timer.time > frame_time) {
                timer.reset();
                animation_frame += 1;
                if (animation_frame === animation_cycle.length) {
                    animation_frame = 0;
                }
                node.css('background-image', images[animation_cycle[animation_frame]]);
            }

            if (animating) {
                timer.requestAnimationFrame(animation_loop);
            }
        };

        this.animate = function ( n ) {
            if (ready) {
                node = n;
                node.css('background-image', images[animation_cycle[0]]);
                animation_frame = 0;
                animating = true;
                timer.reset();
                animation_loop();
            } else {
                var animation = this;
                ready_queue.push(function () {
                    animation.animate(n);
                });
            }
        };

        this.stop = function () {
            animating = false;
        };
    };
};
