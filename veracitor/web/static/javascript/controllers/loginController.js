/**
    The login page of the Veracitor application.
    @constructor
 */
var LoginController = function (controller) {

    /**
       This function is called by the super controller when the tab is opened.
     */
    this.on_tab_active = function () {
        // Set focus to the login user name field
        $('#login input[name=username]').focus();
    };

    (function () {
        $('#join_veracitor').click(function ( evt ) {
            controller.switch_to_tab('account');
        });
    })();

};
