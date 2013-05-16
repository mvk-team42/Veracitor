/**
    Gathers the information and data related to a specific user.

    Information objects created or published by the user will be presented in
    a list. All the crucial information related to a users account will also be
    presented in this view, preferable in text fields to support editing.
    @constructor
 */
var AccountController = function (controller) {

    var ENTER = 13;

    /**
       This function is called by the super controller when the tab is opened.
     */
    this.on_tab_active = function () {
        // Set focus to the user name text field
        $('#account_view > .content > .register-content > .register-form > input[name=username]').focus();

	$('#account_view #view_self_in_network').click(function(evt) {
	    producer = $('#account_view #user_name').val()
	    controller.network.visualize_producer_in_network(producer, -1);
	    controller.switch_to_tab('network');

	});
    };

    (function () {

        $("#delete-user-button").click(function(evt){
            evt.preventDefault();
            $.post("/user/delete",
                   {"user_name": $("#delete_user #users").val()},
                   function(data) {
                       console.log("got here!");
                       console.log(data);
                       var uname = data.result || "not";
                       $("p#user-info").html("User " + uname +" deleted.").fadeOut(2000);
                       setTimeout(function(){
                           $("p#user-info").html("").fadeIn(500);
                       }, 2000);
                       $("#delete_user select").children("option[value=" + uname + "]").remove();
                   }
                  ).fail(function(){
                       $("#user-info").html("Unable to delete user.").fadeOut(2000);
                  });
        });

        $("#register-button").click(function(){
            var username = $(".register-form input[name='username']").val(),
            password = $(".register-form input[name='password']").val();
            $.post("/register", {
                "username": username,
                "password": password
            }, function(data){
                var job_id = data['job_id'];
                controller.set_job_callback(job_id, function(d){
                    var res = d.result;

                    if (res['user_created']) {
                        $(".register-content").html("User created! Please use login tab to login.");
                    } else if (typeof(res['error']) !== 'undefined' && res['error'] !== null) {
                        $(".register-content .error").html(res['error']);
                    }
                });

                $('.register-content .error').html("Registering...");
            });
        });

        // Bind the enter key to the submit button
        $('#account_view > .content > .register-content > .register-form > .field').keydown(function (evt) {
            if (evt.keyCode === ENTER) {
                $("#register-button").click();
            }
        });
    })();

};
