// $(window).on('load', function() {
//     console.log("root loaded");
//     debugger;
//     $(".cboxIframe").on("load", function(){
//         console.log("iframe loaded")
//         $(this).contents().find('.currentitem')
//         if (currentitem.length > 0){
//             console.log("scoll to preview")
//             currentitem.get(0).scrollIntoView(true);
//         }
//     });
// });

$(function(){

  $(document).on('cbox_complete', function() {
    console.log("cbox_complete");
    // var currentitem = $(".cboxIframe").contents().find('.currentitem')
    // if (currentitem.length > 0){
    //     console.log("scoll to preview")
    //     currentitem.get(0).scrollIntoView(true);
    // }
  });

  $(document).on('cbox_load', function() {
    console.log("cbox_load");
    // var currentitem = $(".cboxIframe").contents().find('.currentitem')
    // if (currentitem.length > 0){
    //     console.log("scoll to preview")
    //     currentitem.get(0).scrollIntoView(true);
    // }
  });

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
        dontupdatehistory = false;

  },
      onComplete: function() {
        console.log("complete");
        currentitem_index = $.colorbox.element().index()
        $('iframe').load(function() {
            buildNavi();
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

$(window).on('popstate', function(event) {
    var state = event.originalEvent.state;
    dontupdatehistory = true;
    if (state) {
        $('iframe').contents().find('.previewnav .previewitem').children().eq(state['item_index']).trigger('click');
    }
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
            if(!dontupdatehistory){
                window.history.pushState({'item_index': index},"", $(current_item).attr("href").replace(RegExp('^('+'http://'+location.host+')','g'), ''));
                }
            else{
                dontupdatehistory = false;
            }
        }
        $(current_item).children('.file-mimetype').remove();
        $(current_item).children('span').remove();
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
    var currentitem = $(".cboxIframe").contents().find('.currentitem')
    if (currentitem.length > 0){
        debugger;
        console.log("scoll to preview")
        currentitem.get(0).scrollIntoView(true);
    }
}