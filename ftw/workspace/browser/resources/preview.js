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

  $(function() {

    var dontupdatehistory = false;

    var init = function() {
      $("body").css("overflow", "hidden");
      $("#colorbox").addClass("file-preview-colorbox");
      $("#cboxOverlay").addClass("file-preview-colorbox-background");
      dontupdatehistory = false;
    };

    var prepareNavi = function() { $("iframe").load(buildNavi) };

    var cleanup = function() { $("body").css("overflow", "scroll"); };

    var destroy = function() { $(".previewnav .previewitem").removeClass("currentitem"); };

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
      onComplete: prepareNavi,
      onCleanup: cleanup,
      onClose: destroy
    };

    $(document).on("ready reload activity-fetched", function() {
      $(".documents-tab .file-mimetype").tooltip({
        "tipClass": "file-tooltip"
      });
      $(".colorboxLink").colorbox(settings);
    });

    $(window).on("popstate", function(event) {
      var state = event.originalEvent.state;
      dontupdatehistory = true;
      if (state) {
        $("iframe").contents().find(".previewnav .previewitem").children().eq(state.item_index).trigger("click");
      }
    });
  });

  function buildNavi() {
    var items = $(".previewitem").clone();
    var iframeContents = $("iframe").contents();
    var head = iframeContents.find("head");
    head.append($("<link/>", {
      rel: "stylesheet",
      href: "++resource++ftw.workspace-resources/preview.css",
      type: "text/css"
    }));
    iframeContents.find(".preview").first().prepend("<div class='navcontrol'>&#9664;</div>");
    iframeContents.find(".preview").first().prepend("<div class='previewnav'></div>");
    $.each(items, function(index, item) {
      if (index == currentitem_index) {
        $(item).addClass("currentitem")
        if (!dontupdatehistory) {
          var path = $(item).attr("href").replace(RegExp("^(" + "http://" + location.host + ")", "g"), "");
          window.history.pushState({ "item_index": index }, "", path);
        } else {
          dontupdatehistory = false;
        }
      }
      $(item).children(".file-mimetype").remove();
      $(item).children("span").remove();
      iframeContents.find(".previewnav").first().append(item);
    });
    items.on("click", function(event) {
      iframeContents.find(".currentitem").removeClass("currentitem");
      currentitem_index = $(event.currentTarget).index();
    });
    iframeContents.find(".navcontrol").first().on("click", function() {
      var previewnav = $("iframe").contents().find(".previewnav");
      if (!previewnav.hasClass("collapsed")) {
        previewnav.addClass("collapsed");
        iframeContents.find("iframe").width(iframeContents.find(".preview").width() - previewnav.width());
        iframeContents.find(".navcontrol").css({ left: previewnav.width() });
        iframeContents.find(".navcontrol").html("&#9654;");
      } else {
        iframeContents.find("iframe").removeAttr("style");
        iframeContents.find(".navcontrol").removeAttr("style");
        iframeContents.find(".navcontrol").html("&#9664;");
        iframeContents.find(".previewnav").removeClass("collapsed");
      }
    });
    var currentitem = $(".cboxIframe").contents().find(".currentitem");
    if (currentitem.length > 0) {
      currentitem.get(0).scrollIntoView(true);
    }
  }


}(jQuery));
