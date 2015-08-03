// $(window).on("load", function() {
//     console.log("root loaded");
//     debugger;
//     $(".cboxIframe").on("load", function(){
//         console.log("iframe loaded")
//         $(this).contents().find(".currentitem")
//         if (currentitem.length > 0){
//             console.log("scoll to preview")
//             currentitem.get(0).scrollIntoView(true);
//         }
//     });
// });


(function($) {

  "use strict";

    var currentindex = -1;
    var dontupdatehistory = false;
    var current_state;
    var init = function() {
      $("body").css("overflow", "hidden");
      $("#colorbox").addClass("file-preview-colorbox");
      $("#cboxOverlay").addClass("file-preview-colorbox-background");
      if(currentindex == -1){
        currentindex = $('.colorboxLink').index($.colorbox.element());
        }
    $('#cboxNext').unbind('click');
    $('#cboxPrevious').unbind('click');
        $('#cboxNext').on('click', function() {
            if(currentindex < $('.colorboxLink').length -1) {
                currentindex++;
            }
            else {
                currentindex = 0;
            }
            $.colorbox.next();
        });

        $('#cboxPrevious').on('click', function() {
            if(currentindex > 0){
                currentindex--;
            }
            else {
                currentindex = $('.colorboxLink').length -1;
            }
            $.colorbox.prev();
        });

    };

    var getUrlParameter = function getUrlParameter(sParam) {
        var sPageURL = decodeURIComponent(window.location.search.substring(1)),
            sURLVariables = sPageURL.split('&'),
            sParameterName,
            i;

        for (i = 0; i < sURLVariables.length; i++) {
            sParameterName = sURLVariables[i].split('=');

            if (sParameterName[0] === sParam) {
                return sParameterName[1] === undefined ? true : sParameterName[1];
            }
        }
    };

    var changeUrl = function(){
        if (!current_state){
            current_state = window.location.pathname + window.location.hash;
        }
        var path = window.location.pathname + "?overlay=" + $.colorbox.element().attr("id") + window.location.hash
        if (!dontupdatehistory){
            window.history.pushState({'index': currentindex}, "", path);
        }
        else{dontupdatehistory = false;}
    };
    var cboxComplete = function(){
        changeUrl();

        // Bumblebee-integration
        if (typeof initBumblebee !== 'undefined' && $.isFunction(initBumblebee)) {
                initBumblebee();
        };

        // After clicking a version-entry, the old journal will be deleted and is no longer
        // available for the version-colorbox. Its no longer possible to swich between the versions.
        // To fix this, we copy the given journal into the dom and it will be available for
        // the versioning-colorbox too. After closing the version-colorbox we delete it.
        // see: cbFileVersionPreviewClosed-event
        $('.journalItemLink.cboxElement').on("click", function(){
          $('#colorbox').after($('.journal').css('display', 'none').addClass('tempJournal'))
        })

    };
    var cleanup = function() { $("body").css("overflow", "scroll");
                               window.history.pushState({}, "", current_state);
                               currentindex = -1 };
    var clickUIDElement = function() {
      if (getUrlParameter('overlay')) {
        var uid = getUrlParameter('overlay');
        var element = document.getElementById(uid);
        $(element).click();
      }
    }
    var settings = {
      photo: false,
      iframe: false,
      html: false,
      inline: false,
      rel: "previews",
      width: "95%",
      height: "90%",

      className: 'cbFilePreview',
      trapFocus: true,
      fixed: true,
      reposition: false,
      scrolling: true,
      arrowKey: true,
      transition: "none",
      current: "{current} / {total} Dateien",
      title: " ",
      fadeOut: 0,
      loop: true,

      onOpen: init,
      onComplete: cboxComplete,
      onCleanup: cleanup,
    };
    var init = function() {
      $(".documents-tab .file-mimetype").tooltip({
        "tipClass": "file-tooltip"
      });
      $(".colorboxLink").colorbox(settings);
      settings['iframe'] = true;
      $(".Image.colorboxLink").colorbox(settings);
      settings['iframe'] = false;

      clickUIDElement();
    };
    var resizeColorbox = function() {
      if ($('.cbFilePreview').is(':visible')){
        $.colorbox.resize({width:$('body').width()*0.95, height:$('body').height()*0.9});
      };
    };
    $(document).on("cbFileVersionPreviewClosed", function() {
      $('.tempJournal').remove();
      init();
    })
    $(document).on("ready reload activity-fetched", function() {
      init();
      $(".simplelayout-content:first").on('refreshed', function() {
        init();
      });
    });

$(window).on('popstate', function(event) {
    if(history.state == true && history.state.index == undefined){
      if (location.pathname + location.hash == current_state){
        $.colorbox.close();
      }
      return;
    }

    if(history.state && ((history.state.index < currentindex && !(history.state.index == 0 && currentindex ==$('.colorboxLink').length -1)) || (currentindex ==0 && history.state.index == $('.colorboxLink').length -1))){
        dontupdatehistory = true;
        currentindex = history.state.index;
        $.colorbox.prev();
    }
    else{
        dontupdatehistory = true;
        if (history.state){
            currentindex = history.state.index;
            $.colorbox.next();
        }
    }
});
$( window ).on('resize', function() {
  resizeColorbox();
});

}(jQuery));


