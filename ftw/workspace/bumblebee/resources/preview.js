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
            console.log(currentindex);
            window.history.pushState({'index': currentindex}, "", path);
        }
        else{dontupdatehistory = false;}

        // Bumblebee-integration
        if (typeof initBumblebee !== 'undefined' && $.isFunction(initBumblebee)) {
                initBumblebee();
        };
    };
    var cleanup = function() { $("body").css("overflow", "scroll");
                               window.history.pushState({}, "", current_state);
                               currentindex = -1 };

    var destroy = function() {  };

    var settings = {
      iframe: false,
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

      onOpen: init,
      onComplete: changeUrl,
      onCleanup: cleanup,
      onClose: destroy
    };

    $(document).on("ready reload activity-fetched", function() {
      $(".documents-tab .file-mimetype").tooltip({
        "tipClass": "file-tooltip"
      });
      $(".colorboxLink").colorbox(settings);
      if (getUrlParameter('overlay')) {
        var uid = getUrlParameter('overlay')
        var element = document.getElementById(uid);
        $(element).click();
      }

    });

$(window).on('popstate', function(event) {
    if(history.state.index == undefined && location.pathname + location.hash != current_state){
        return;
    }
    else if(history.state.index == undefined && location.pathname + location.hash == current_state){
        $.colorbox.close();
        return;
    }

    if((history.state.index < currentindex && !(history.state.index == 0 && currentindex ==$('.colorboxLink').length -1)) || (currentindex ==0 && history.state.index == $('.colorboxLink').length -1)){
        dontupdatehistory = true;
        currentindex = history.state.index;
        $.colorbox.prev();
    }
    else{
        dontupdatehistory = true;
        currentindex = history.state.index;
        $.colorbox.next();
    }
});


}(jQuery));


