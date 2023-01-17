;(function ($) {
    "use strict";

    /*============= preloader js css =============*/
    var cites = [];
    cites[0] = "لقد صممنا Docly للقراء ، مع تحسين ليس لعرض الصفحات أو المشاركة";
    cites[1] = "تبين دوكلي أن السياق هو جزء أساسي من التعلم.";
    cites[2] = "يمكنك إنشاء أي نوع من وثائق المنتج باستخدام Docly";
    cites[3] = "نظام بحث بصري متقدم مدعوم من Ajax";
    var cite = cites[Math.floor(Math.random() * cites.length)];
    $('#preloader p').text(cite);
    $('#preloader').addClass('loading');

    $(window).on( 'load', function() {
        setTimeout(function () {
            $('#preloader').fadeOut(500, function () {
                $('#preloader').removeClass('loading');
            });
        }, 500);
    })

})(jQuery)