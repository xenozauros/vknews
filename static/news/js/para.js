var token= $.cookie('csrftoken');
var jumboHeight = $('.jumbotron').outerHeight();
function parallax() {
    var scrolled = $(window).scrollTop();
    $('.bg').css('height', (jumboHeight-scrolled) + 'px');
};

$(window).scroll(function(e) {
    parallax();
});



function affixResize() {
    var $affixElement = $('div[data-spy="affix"]');
        $affixElement.width($affixElement.parent().width());
};                            
$(affixResize);
$(window).resize(affixResize);

var cl = new CanvasLoader('load_indicator');
    cl.setDiameter(58);
    cl.setDensity(15);
    cl.setRange(0.9);
    cl.setSpeed(1);

