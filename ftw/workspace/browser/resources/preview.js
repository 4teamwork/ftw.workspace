$(function(){

  $(document).on('ready reload activity-fetched', function() {
    $('.documents-tab .file-mimetype').tooltip({'tipClass': 'file-tooltip'});


    $('.colorboxLink').colorbox({
      iframe: true,
      rel: 'previews',
      width: '95%',
      height: '90%',

      trapFocus: true,
      fixed: true,
      reposition: false,
      scrolling: true,
      arrowKey: true,
      transition: 'none',
      current: '{current} / {total} Dateien',
      title: ' ',

      onOpen: function() {
        $('body').css('overflow', 'hidden');
        $('#colorbox').addClass('file-preview-colorbox');
        $('#cboxOverlay').addClass('file-preview-colorbox-background');


  },
      onComplete: function() {
        currentitem_index = $.colorbox.element().index()
        $('iframe').load(function() {
            buildNavi();
            setTimeout(function(){
                $('iframe').contents().find('.currentitem').get(0).scrollIntoView(true);}, 50);
         });
      },

      onCleanup: function() {
        $('body').css('overflow', 'scroll');
      },

      onClose: function() {
        $('.previewnav .previewitem').removeClass('currentitem');

      }
    });

  });
});

function buildNavi(){
    var items = $('.previewitem').clone();
    var head = $("iframe").contents().find("head");
    head.append($("<link/>", { rel: "stylesheet", href: "++resource++ftw.workspace-resources/preview.css", type: "text/css" }));
    $('iframe').contents().find('.preview').first().prepend('<div class="navcontrol">&#9664;</div>');
    $('iframe').contents().find('.preview').first().prepend('<div class="previewnav"></div>');
    for (index = 0; index < items.length; ++index){
        current_item = items[index];
        if (index == currentitem_index){
            $(current_item).addClass('currentitem')
        }
        $(current_item).children('.file-mimetype').remove();
        $(current_item).children('p').remove();
        $('iframe').contents().find('.previewnav').first().append(current_item);
    }
    items.on('click', function( event ) {
        $('iframe').contents().find('.currentitem').removeClass('currentitem');
        currentitem_index = $(event.currentTarget).index();
    });
    $('iframe').contents().find('.navcontrol').first().on('click', function(){
        var previewnav = $('iframe').contents().find('.previewnav');
        if (! previewnav.hasClass('collapsed')) {
            previewnav.addClass('collapsed');
            $('iframe').contents().find('iframe').width(
                $('iframe').contents().find('.preview').width() - previewnav.width());
            $('iframe').contents().find('.navcontrol').css({left: previewnav.width()});
            $('iframe').contents().find('.navcontrol').html("&#9654;");
        }
        else {
            $('iframe').contents().find('iframe').removeAttr("style");
            $('iframe').contents().find('.navcontrol').removeAttr("style");
            $('iframe').contents().find('.navcontrol').html("&#9664;");
            $('iframe').contents().find('.previewnav').removeClass('collapsed');
        }
    })
}
