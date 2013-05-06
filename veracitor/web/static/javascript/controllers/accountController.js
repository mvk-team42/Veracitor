/**
    Gathers the information and data related to a specific user.

    Information objects created or published by the user will be presented in
    a list. All the crucial information related to a users account will also be
    presented in this view, preferable in text fields to support editing.
    @constructor
 */
var AccountController = function (controller) {

    /**
       This function is called by the super controller when the tab is opened.
     */
    this.on_tab_active = function () {

      $("#register-button").click(function(){
        var username = $(".register-form input[name='username']").val(),
        password = $(".register-form input[name='password']").val();
        console.log("username: " + username +" pass: " + password);
        $.post("/register",{"username": username,
                            "password": password},
              function(data){
                var job_id = data['job_id'];
                controller.set_job_callback(job_id, function(d){
                  console.log(d);
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
    };

};
