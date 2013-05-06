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
      $("register-button").click(function(){
        var username = $("form input[name='username']").val(),
        password = $("form input[name='password']").val();
        $.post("/register",{"username": username,
                            "password": password},
              function(data){
                var job_id = data['job_id'];
                controller.set_job_callback(job_id, function(d){
                  if (d['user_created']) {
                    $("form").html("User created! Please use login tab to login.");
                  } else {
                    $(".error").html(d['error']);
                  }
                });
                $('.error').html("Registering...");
              });
      });
    };

};
