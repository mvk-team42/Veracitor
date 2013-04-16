/**
   The master/super controller of the Veracitor web site.
   @constructor
*/
function SuperController() {

    // The time interval between callback checks
    var CALLBACK_CHECK_TIME = 500;

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
        }, (function (job_id, callback) {
            return function (data, status, jqXHR) {
                if(jqXHR.status == 200) {
                    callback(data);
                } else {
                    setTimeout(watch_job(job_id, callback), CALLBACK_CHECK_TIME);
                }
            };
        })(job_id, callback))
        .fail(function () {
            $("#search-result").html("<h2>Server error.</h2>");
        });
    }

}
