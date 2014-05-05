function activatePreviewColorbox(){

  $('a.colorboxLink').colorbox(
  {
    'photo': true,
    'current': '{current}/{total}',
    'width': '80%',
    'height': '80%',
    'title': function() {
        return $(this).attr('title') +
               'Details'.link($('img',this).attr('detail_url')) +
               'Download'.link($('img',this).attr('download_url'));
    }
  });
}

function short_name(str, maxLen) {
    if (str.length < maxLen) return str;
    part = (maxLen - 3)/2; // minus the three dots
    return str.substring(0, part)+"..."+str.substring(str.length-part);
}

function activatePreviewGroups(data){
  var headings = $('.previewGroupTitle', data);
  $.each(headings, function(index, value){
    $value = $(value);

    if (index === 0){
      $value.show();
    } else {
      var prev = headings.eq(index-1).html();
      var current = $value.html();

      if (prev !== current){
        $value.show();
      }
    }
    return;

  });
}

function loadMoreContent(){
  var url = $('base').attr('href') + '/previews';
  var bsize = parseInt($('.previewBatchSize').html(), radix=10);
  var bstart = parseInt($('.previewBatchStart').html(), radix=10);

  if (bstart === -1){
    // stop loading more data
    return;
  }
  var newbstart = bstart + bsize;
  $('.previewBatchStart').html(newbstart);

  $.get(url, {'bstart': newbstart}, function(data) {

    if (data !== ''){
      $('.previewContainer a:last').after(data);
      activatePreviewColorbox();
      activatePreviewGroups($('.previewContainer'));
    } else {
      $('.previewBatchStart').html(-1);
    }
  });
}

function initPreviewInfinitScroll(){
  $(window).on("scroll", function() {
    $('.previewContainer').addClass('infinitScroll');
    if ($(window).scrollTop() == $(document).height() - $(window).height()) {
      if ($('.previewContainer').length !== 0){
        loadMoreContent();
      }
    }
  });
}
