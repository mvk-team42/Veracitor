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

    var sigRoot = document.getElementById('network-holder');
    var sigInst = sigma.init(sigRoot);
    
    sigInst.drawingProperties({
        defaultLabelColor: '#ccc',
        font: 'Arial',
        edgeColor: 'source',
        defaultEdgeType: 'curve'
    }).graphProperties({
        minNodeSize: 0.5,
        maxNodeSize: 10,
        minEdgeSize: 1,
        maxEdgeSize: 1,
    });

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
    this.visualizeProducerInNetwork = function (sourceNode, depth) {
        // TODO
        // Generate and display a test graph
        drawGraph(generateData(40, 5, 5));
    };
    
    /**
        Visualizes the given trust network.
     */
    this.visualizeTrustNetwork = function (network) {
        // TODO
    };

    /**
        Generates some test graph data.
        @param nodes The number of generated nodes.
        @param tags The number of tag objects.
        @param maxNodes The maximum number of connections for one node (?).
     */
    var generateData = function (nodes, tags, maxNodes) {
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
    var drawGraph = function (data) {
        var i, j;

        for(i in data) {
            sigInst.addNode(i, {
                label: 'Node ' + i,
                color: '#ff0000',
                x: Math.random(),
                y: Math.random()
            });
        }
        
        for(i in data) {
            for(j in data[i]) {
                sigInst.addEdge("Edge " + i + "-" + j, i, j);
            }
        }
        
        sigInst.draw();
    }

};

