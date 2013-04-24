/**
   The master/super controller of the Veracitor web site.
   @constructor
*/
function SuperController() {

    // The time interval between callback checks
    var CALLBACK_CHECK_TIME = 100;

    /**

       @param f The function checking the callback.
       @param id An id related to the job started on the server.
     */
    this.set_job_callback = function (job_id, callback) {
        watch_job(job_id, callback);
    }

    /**
       Check the status of a started job on the server.
       @param callback The callback function.
       @param job_id An id related to the job started on the server.
     */
    var watch_job = function (job_id, callback) {
        $.post('/jobs/job_result', {
            'job_id' : job_id
        }, function (data, status, jqXHR) {
            if(jqXHR.status == 200) {
                callback(data);
            } else {
                setTimeout(function () {
                    watch_job(job_id, callback);
                }, CALLBACK_CHECK_TIME);
            }
        })
        .fail(function () {
            $("#search-result").html("<h2>Server error.</h2>");
        });
    }

    /**
       Request a TidalTrust value.
    */
    window.tt = function request_tidal_trust(source, sink, tag) {
        $.post('/jobs/algorithms/tidal_trust', {
            'source': source,
            'sink': sink,
            'tag': tag
        }, function (data) {
            // SUCCESS
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
            console.log("Ok: ", data);
        })
        .fail(function (data) {
            // FAIL
            console.log("Fail:", data);
        });

    }

}
