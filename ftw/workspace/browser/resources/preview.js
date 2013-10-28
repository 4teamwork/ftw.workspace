function activateColorbox(){
  $('a.colorboxLink').colorbox(
  {
    'photo': true,
    'current': '{current}/{total}',
    'maxWidth': '100%',
    'maxHeight': '100%'
  });
}

function activateGroups(data){
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

  $.post(url, {'bstart': newbstart}, function(data) {

    if (data !== ''){
      $('.previewContainer a:last').after(data);
      activateColorbox();
      activateGroups($('.previewContainer'));
    } else {
      $('.previewBatchStart').html(-1);
    }
  });
}

function initPreviewInfinitScroll(){
  activateColorbox();
  activateGroups($('.previewContainer'));

  $(window).on("scroll", function() {
    $('.previewContainer').addClass('infinitScroll');
    if ($(window).scrollTop() == $(document).height() - $(window).height()) {
      if ($('.previewContainer').length !== 0){
        loadMoreContent();
      }
    }
  });
}
