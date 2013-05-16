/**
   Handles a users ratings to other producer objects in the database.

   The user is presented a list with already rated producers and users, as
   well as groups, that is defined in the database. All set ratings can be
   altered directly in the list and there will be an option to display a se-
   lected producer in the NetworkView. Producers, users and groups not
   previously rated will be presented in a separate list and will be moved to
   the “rated list” when a rating is set.
   @constructor
*/

var RatingsController = function (controller) {

    var active_tag = '';

    /**
       Initialize the ratings tab:
       (currently done in the on_tab_active function below)
    */
    (function () {
    })();

    /**
       This function is called by the super controller
       each time the tab is opened.
     */
    this.on_tab_active = function () {
        $.post('/jobs/ratings/render',{}, function (data) {
            $('#ratings_view_content').html(data.html);

            //Must be called before populating tag dropdowns
            add_event_handlers(data.producers, data.information);
            if ($('.left #prod-tags option').length > 0 ) {
                $('#prod-tags').change();
            }
            if ($('.right #info-tags option').length > 0 ) {
                $('#info-tags').change();
            }
        });
    };

    /**
       TODO: Remove?
     */
    function initialize_filtering () {

    };

    /**
       Add event handlers to the ratings view.
    */
    function add_event_handlers(producers,information) {
        $('div.description')
            .click(function(evt) {
                var producer = $(this).children('input[type="hidden"]').val()
                controller.network.visualize_producer_in_network(producer);
                controller.switch_to_tab('network');
            });

        $('#ratings_view form').submit(function(evt) {
            return false;
        });

        $(".left #prod-tags").change(function() {
            var selectedValue = $(this).find(":selected").val().replace(/(\s|\.|#|\|)/g, "_");
            active_tag = selectedValue;
            $('#producer-list .group_active').not('.' + selectedValue).hide()
            $('#producer-list > div.group_active.' + selectedValue).show();
        });

        $(".right #info-tags").change(function() {
            var selectedValue = $(this).find(":selected").val().replace(/(\s|\.|#|\|)/g, "_");
            if( selectedValue != 'none' ) {
                $('.right #information-list >').not('div.' + selectedValue).hide()
                $('.right #information-list > div.' + selectedValue).show();
            }
            else {
                $('.right #information-list >').show();
            }
        });


        /*
         * Filters the producer-list on groups.
         * It uses a hidden div with hidden input tags
         * that contains all the producers that are within a
         * certain group to do the filtering.
         */
        $(".left #groups").change(function() {
            var selectedValue = $(this).find(":selected").val();
            if( selectedValue != 'all' ) {
                $("#rate-group").removeAttr("disabled");
                group_selector = '.left .group-members#' + selectedValue.replace(/(\s|\.|#|\|)/g, "_") + ' input';
                // Reset classes
                $('div#producer-list').children().addClass("group_inactive");
                $('div#producer-list').children().removeClass("group_active");
                $(group_selector).each(function() {
                    $('div#producer-list div#' + $(this).val().replace(/(\s|\.|#|\|)/g, "_")).addClass('group_active').removeClass('group_inactive');
                });
                $('div#producer-list div.group_inactive.' + active_tag).hide();
                $('div#producer-list div.group_active.' + active_tag).show();
                producer_selector = 'div#producer-list div#' + $(this).val();


            }
            else {
                $("#rate-group").attr("disabled", "disabled");
                $('div#producer-list').children().addClass("group_active");
                $('div#producer-list').children().removeClass("group_inactive");

                $('div#producer-list div.group_active.'+ active_tag).show();
            }
        });

        $("#new-group").click(function(evt) {
            show_new_group_form();
        });

        $("#rate-group").click(function(evt) {
            //   if(!$("#groups").val() == 'all') {
            show_rate_group_form();
            // }
        });

        $('#producer-list').accordion({ collapsible: true, active: false, header: "h3"});

        $('#information-list').accordion({ collapsible: true, active: false, header: "h3"});

        $('#create-group').click(function(evt) {
            $.post('/jobs/ratings/create_group',
                   {
                       'name' : $('#name').val(),
                       'tag' : $('#create-group-tag').find(':selected').val()
                   }, add_group)
        });

        $('#rate-group-submit').click(function(evt) {
            $.post('/jobs/ratings/rate_group',
                   {
                       'name' : $('#groups').find(':selected').val(),
                       'tag' : $('#rate-group-tag').find(':selected').val(),
                       'rating' : $('#rate-group-rating').find(':selected').val()
                   }, done_rating_group)
        });

    }


    function done_rating_group(data) {
        $('div#producer-list > :visible div.rating').html(data)
        var grouptext = $('#groups').find(':selected').text();
        grouptext = grouptext.slice(0,-1) + data
        $('#groups').find(':selected').text(grouptext)
        hide_rate_group_form();
    }

    function add_group(data) {
        hide_new_group_form();
        $('#groups')
            .append($("<option></option>")
                    .attr("value",data)
                    .text(data));
    }

    function show_rate_group_form() {
        $('#rate-group').css('display','none');
        $('#rate-group-form-div').fadeIn();
        $('#group-form-border-div').css('border','1px solid');
    }

    function hide_rate_group_form() {
        $('#rate-group-form-div').fadeOut();
        $('#rate-group').show();
        $('#group-form-border-div').css('border','');
    }

    function show_new_group_form() {
        $('#new-group').css('display','none');
        $('#new-group-form-div').fadeIn();
    }

    function hide_new_group_form() {
        $('#new-group-form-div').fadeOut();
        $('#new-group').show();
    }
};
