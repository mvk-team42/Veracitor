/**
   The master/super controller of the Veracitor web site.
   @constructor
*/
function SuperController() {

    // The time interval between callback checks
    var CALLBACK_CHECK_TIME = 500;

    /**
       Check the status of a started job on the server.
       @param f The function checking the callback.
       @param url The URL to check the callback against.
       @param id An id related to the job started on the server.
     */
    this.watch_callback = function (f, url, id) {
        $.post(url, {
            'id' : id
        }, (function (f, url, id) {
            return function (data) {
                var response = JSON.parse(data);

                console.log(response);

                if(response.procedure.status == "processing") {
                    setTimeout(watch_callback(f, url, id), CALLBACK_CHECK_TIME);
                } else {
                    f(response);
                }
            };
        })(f, url, id))
        .fail(function () {
            $("#search-result").html("<h2>Server error.</h2>");
        });
    }

}
