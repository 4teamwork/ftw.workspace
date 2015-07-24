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


    var dontupdatehistory = false;
    var current_state;
    var init = function() {
      $("body").css("overflow", "hidden");
      $("#colorbox").addClass("file-preview-colorbox");
      $("#cboxOverlay").addClass("file-preview-colorbox-background");
      dontupdatehistory = false;
    };

    var changeUrl = function(){
        if (!current_state){
            current_state = window.location.pathname + window.location.hash;
        }
        var path = $.colorbox.element().attr("href").replace(RegExp("^(" + "http://" + location.host + ")", "g"), "");
        window.history.replaceState({}, "", path);

    };
    var cleanup = function() { $("body").css("overflow", "scroll");
                               window.history.replaceState({}, "", current_state); };

    var destroy = function() {  };

    var settings = {
      iframe: true,
      rel: "previews",
      width: "95%",
      height: "90%",

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
    });

}(jQuery));
