DISABLE_REFRESH = false;
REFRESH_TIME = 60000;

$(function(){
    $("#refresh_time").html(REFRESH_TIME / 1000);
    refresh_stream = function()
    {
        if(DISABLE_REFRESH)
        {
            setTimeout(refresh_stream, REFRESH_TIME);
            return;
        }

        $("#sample_ajax_status").show();
        $.get(UI.samples_interface + "?op=" + Math.random(), function(new_samples){
            $("#sample_ajax_status").hide();
            $("#stream_list").html('').append(new_samples);

            $("#notify").fadeIn('slow', function(){
                    var self = this;
                    setTimeout(function(){$(self).fadeOut('slow', function(){});}, 1000);
                    });
            setTimeout(refresh_stream, REFRESH_TIME);
        })
    };

    setTimeout(refresh_stream, REFRESH_TIME);

    $("#toggle_refresh").click(function(){
        DISABLE_REFRESH = !DISABLE_REFRESH;

        if(DISABLE_REFRESH)
        {
            $(this).html("启动");
        }
        else
        {
            $(this).html("停止");
        }
    });

}
);
