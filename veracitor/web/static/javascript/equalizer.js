/**
   An equalized force-directed layout for the cytoscape.js library.
   @author John Brynte Turesson
 */
;(function ($$) {

    // default layout options
    var defaults = {
        'ready': function(){},
        'stop': function(){}
    };

    // physics variables
    var mass = 1, constraint = 400, friction = 100, length = 1;
    var settle = 15, threshold = 0.01;

    // forces acting on each node
    var node_forces = {};

    // constructor
    // options : object containing layout options
    var EqualizerLayout = function (options) {
        this.options = $$.util.extend(true, {}, defaults, options);
    };

    var time;
    var iterations;

    EqualizerLayout.prototype.run = function () {
        var options = this.options;
        var cy = options.cy;
        var i;

        cy.nodes().each(function (i, node) {
            node.position({
                'x': Math.random(),
                'y': Math.random()
            });
        });

        for(i = 0; i < 1; i += 1) {
            time = 0;
            iterations = 0;
            equalize_graph(cy);
            console.log('average: ' + time/iterations + ' ms/node, total time: ' + time + ' ms');
        }

        // trigger layoutready when each node has had its position set at least once
        cy.one('layoutready', options.ready);
        cy.trigger('layoutready');

        // trigger layoutstop when each node has had its position set at least once
        cy.one('layoutstop', options.stop);
        cy.trigger('layoutstop');
    }

    // called on continuos layouts to stop them before they finish
    EqualizerLayout.prototype.stop = function () {
        var options = this.options;
    };

    var equalize_graph = function (cy) {
        cy.edges().each(function (i, edge) {
            equalize_edge(cy, edge);
        });

        cy.nodes().each(function (i, node) {
            var t = new Date().getTime();
            equalize_node(node);
            time += new Date().getTime() - t;
            iterations += 1;
        });
    };

    var equalize_node = function (node) {
        var x = node.position('x');
        var y = node.position('y');
        var fx = node_forces[node.data('id')].fx;
        var fy = node_forces[node.data('id')].fy;

        //console.log('fx: ' + fx + ', fy: ' + fy);

        x -= fx / mass;
        y -= fy / mass;

        node.position({
            'x': x,
            'y': y
        });

        /*
        if(fx > threshold) {
            x -= fx / mass;
        } else if(fx < -threshold) {
            x += fx / mass;
        }*/
    };

    var equalize_edge = function (cy, edge) {
        var source = cy.filter('node[id="' + edge.data('source') + '"]')[0];
        var target = cy.filter('node[id="' + edge.data('target') + '"]')[0];

        var fx, fy;
        var dx = source.position('x') - target.position('x');
        var dy = source.position('y') - target.position('y');
        var d = Math.sqrt(Math.pow(dx, 2) + Math.pow(dy, 2));

        if(d !== 0) {
            fx = -(dx / d) * (d - length) * constraint;
            fy = -(dy / d) * (d - length) * constraint;
            apply_force(source.data('id'), fx, fy);
            apply_force(target.data('id'), -fx, -fy);

            /*
            fx = -(c1.getXV() - c2.getXV()) * friction;
            fy = -(c1.getYV() - c2.getYV()) * friction;
            c1.applyForce(fx, fy);
            c2.applyForce(-fx, -fy);*/
        }
    };

    var apply_force = function (node, fx, fy) {
        if (typeof(node_forces[node]) === 'undefined') {
            node_forces[node] = {
                'fx': fx,
                'fy': fy
            };
        } else {
            node_forces[node].fx += fx;
            node_forces[node].fy += fy;
        }
    };

    // register the layout
    $$('layout', 'equalizer', EqualizerLayout);

})(cytoscape);
