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
var NetworkController = function (view, controller, visualizer) {

    // Display something in the network
    //visualizer.visualizeProducerInNetwork(null, -1);

    $('#calculate-sunny').click(function (evt) {
        request_sunny_value('SvD', 'DN', 'newspaper');
    });

    /**
       Request a TidalTrust value.
    */
    window.tt = function request_tidal_trust(source, sink, tag) {
        $.post('/algorithms/tidal_trust', {
            'source': source,
            'sink': sink,
            'tag': tag
        }, function (data) {
            // SUCCESS
//            var response = JSON.parse(data);
            console.log("Ok: ", data);
        })
        .fail(function (data) {
            // FAIL
            console.log("Fail:", data);
        });
    }
    window.job_result = function request_job_result(job_id) {

        $.post('/jobs/job_result', {
            'job_id': job_id
        }, function (data) {
            // SUCCESS
//            var response = JSON.parse(data);
            console.log("Ok: ", data);
        })
        .fail(function (data) {
            // FAIL
            console.log("Fail:", data);
        });
    
    }
    
    /**
       Request a SUNNY value.
    */
    function request_sunny_value(source, sink, tag) {
        $.post('/calculate_sunny_value', {
            'source': source,
            'sink': sink,
            'tag': tag
        }, function (data) {
            var response = JSON.parse(data);

            if(response.error.type == 'none') {
                $('#calculated-trust').html(response.procedure.trust);

                controller.watch_callback(function (response) {
                    //$('#calculated-trust').html(response.procedure.trust);
                }, response.procedure.callback_url, response.procedure.id);
            } else {
                $('#search-result').html('<h2>' + response.error.message + '</h2>');
            }
        })
        .fail(function () {
            $('#search-result').html('<h2>Server error.</h2>');
        });
    }

}
