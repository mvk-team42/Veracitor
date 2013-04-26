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
    var mass = 10, constraint = 8000, friction = 100, length = 200, pullforce = 10000;
    var settle = 15, threshold = 0.00001, curlen, amount, update;

    // forces acting on each node
    var node_forces = {};

    // constructor
    // options : object containing layout options
    var EqualizerLayout = function (options) {
        this.options = $$.util.extend(true, {}, defaults, options);
    };

    EqualizerLayout.prototype.run = function () {
        var options = this.options;
        var cy = options.cy;
        var i;

        for(i = 0; i < 1; i += 1) {
            equalize_graph(cy);
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
            equalize_edge(edge);
        });

        cy.nodes().each(function (i, node) {
            equalize_node(node);
        });
    };

    var equalize_node = function (node) {
        var fx = node_forces[node];
        var fy = node_forces[node];

        if(xv > threshold) {
            xv -= xv * settle * time.delta;
            if(xv < 0) {
                xv = 0
            }
        } else if(xv < -threshold) {
            xv -= xv * settle * time.delta;
            if(xv > 0) {
                xv = 0
            }
        }
        if(yv > threshold) {
            yv -= yv * settle * time.delta;
            if(yv < 0) {
                yv = 0
            }
        } else if(yv < -threshold) {
            yv -= yv * settle * time.delta;
            if(yv > 0) {
                yv = 0
            }
        }

        xv += (fx / mass) * time.delta;
        yv += (fy / mass) * time.delta;

        fx = 0;
        fy = 0;

        x += xv * time.delta;
        y += yv * time.delta;

        this.setXY(x, y);
    }

    var equalize_edge = function (edge) {
        var fx, fy;
        var dx = c1.getX() - c2.getX();
        var dy = c1.getY() - c2.getY();
        var d = Math.sqrt(Math.pow(dx, 2) + Math.pow(dy, 2));

        if(d !== 0) {
            fx = -(dx / d) * (d - len) * constraint;
            fy = -(dy / d) * (d - len) * constraint;
            c1.applyForce(fx, fy);
            c2.applyForce(-fx, -fy);

            fx = -(c1.getXV() - c2.getXV()) * friction;
            fy = -(c1.getYV() - c2.getYV()) * friction;
            c1.applyForce(fx, fy);
            c2.applyForce(-fx, -fy);
        }

        l.setAttributeNS(null, "x1", c1.getX());
        l.setAttributeNS(null, "y1", c1.getY());
        l.setAttributeNS(null, "x2", c2.getX());
        l.setAttributeNS(null, "y2", c2.getY());
    }

    // register the layout
    $$('layout', 'equalizer', EqualizerLayout);

})(cytoscape);
