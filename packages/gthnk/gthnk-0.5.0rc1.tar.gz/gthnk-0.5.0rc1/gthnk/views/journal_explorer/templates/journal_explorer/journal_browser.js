// http://stackoverflow.com/questions/4198041/jquery-smooth-scroll-to-an-anchor/12714767#12714767
$(".scroll").click(function(event){
    event.preventDefault();
    window.history.replaceState(null, this.title, url=this.hash);
    var dest=$('#entries_scroller').scrollTop()+($(this.hash).offset().top)-60;
    $('#entries_scroller').animate({scrollTop:dest}, 300,'swing');
 });

$(".top_of_page").click(function(event){
    $('#pages_scroller').animate({scrollTop:100}, 300,'swing');
})

var set_height = function(){
    $("#entries_scroller").css("height", $(window).height()-99);
    $("#pages_scroller").css("height", $(window).height()-57);
    $("#page_wrapper").css("height", $(window).height()+50);
}

$("#edit_button").click(function() {
    $("body").toggleClass("editing");
    $("#edit_button").toggleClass("active");

    if ($("body").hasClass("editing")) {
        $('.controllable .editable').fadeIn();
    }
    else {
        $('.controllable .editable').fadeOut();
    }
});


// search box inside day view
if ($("#search_box")) {
    $("#search_button").click(function() {
        $("#search_button").parent().toggleClass("active");
        $("#search_box").toggleClass("active");
        if ($("search_box").hasClass("active")) {
            $("search_box").show();
        }
        else {
            $("search_box").hide();
        }
    });
}

// http://www.daterangepicker.com/
// 1.3.15
// https://github.com/dangrossman/bootstrap-daterangepicker/tree/0d7f4f26618e09ba6d2488a7e42273fd2fb07ae7
$('a#calendar_button').daterangepicker(
    {
        format: 'YYYY-MM-DD',
        singleDatePicker: true,
        startDate: today // set this value in the html body, within script tags
    },
    function(start, end, label) {
        window.location = "/admin/journal/nearest/" + start.format('YYYY-MM-DD');
    }
);

$( window ).resize( set_height );

reveal_confirm_widget = function() {
    var container = $(this).parent().children()[1];
    console.log(container);
    $(container).toggle("slide");
}

hide_confirm_widget = function() {
    var container = $(this).parent();
    console.log(container);
    $(container).toggle("slide");
}

set_image_widths = function() {
    // set image widths
    var widths = $(".page_attachment a + div img").map(function(){
        return $(this).width();
    }).get();

    $(".image_container").each(function(index, value){
        $(value).css("width", widths[index]);
    });
}

$( document ).ready( function() {
    set_height();
    $('#pages_scroller').scrollTop(100);
    $(".delete_button").click(reveal_confirm_widget);
    $(".cancel_button").click(hide_confirm_widget);
    $('.controllable .editable').hide();
    $('.controllable .viewable').hide();

    /*$("img.lazy").lazy({
        appendScroll: $("div.image_container")
    });*/
} );

$(window).bind("load", function() {
    set_image_widths();
});

$("#entries, .image_container").hover(
    function() {
        if (!$("body").hasClass("editing")) {
            $(this).find('.controllable .viewable').fadeIn();
        }
    },
    function() {
        if (!$("body").hasClass("editing")) {
            $(this).find('.controllable .viewable').fadeOut();
        }
    }
);

$(".viewable a").click(function(){
    window.history.replaceState(null, this.title, url="#"+$(this).attr("anchorid"));
});

