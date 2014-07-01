function activatePreviewColorbox() {
    $('a.colorboxLink.image').colorbox({
        photo: true,
        current: '{current}/{total}',
        width: '80%',
        height: '80%',
        title: function() {
            var $img = $('img', this);
            linkwrapper = $($(this).parent()).children('.preview_actions');
            if (linkwrapper !== null) {
                return $(this).attr('title') + linkwrapper.html();
            } else {
                return '';
            }
        },
    });

    $('a.colorboxLink.html').colorbox({
        current: '{current}/{total}',
        width: '80%',
        height: '80%',
        html: function(cache) {
            var url = $(cache.el).attr('href');

            var content;
            $.ajax({
                url: url,
                async: false,
                success: function(data) {
                    content = data;
                },
            });
            return $('<div id="colorboxAjaxContent" />').append($('#content > *', content))[0];
        },
        title: function() {
            var $el = $('*:first', this);
            linkwrapper = $($(this).parent()).children('.preview_actions');
            
            if (linkwrapper !== null){
                return $(this).attr('title') + linkwrapper.html();
            } else {
                return '';
            }
        },
    });
}


function activatePreviewGroups(data) {
    var headings = $('.previewGroupTitle', data);
    $.each(headings, function(index, value) {
        $value = $(value);

        if (index === 0) {
            $value.show();
        } else {
            var prev = headings.eq(index - 1).html();
            var current = $value.html();

            if (prev !== current) {
                $value.show();
            }
        }
        return;

    });
}

function loadMoreContent() {
    var url = $('base').attr('href') + '/previews';
    var bsize = parseInt($('.previewBatchSize').html(), radix = 10);
    var bstart = parseInt($('.previewBatchStart').html(), radix = 10);

    if (bstart === -1) {
        // stop loading more data
        return;
    }
    var newbstart = bstart + bsize;
    $('.previewBatchStart').html(newbstart);

    $.get(url, {
        'bstart': newbstart
    }, function(data) {

        if (data !== '') {
            $('.previewContainer .colorboxLinkWrapper:last').after(data);
            activatePreviewColorbox();
            activatePreviewGroups($('.previewContainer'));
        } else {
            $('.previewBatchStart').html(-1);
        }
    });
}

function initPreviewInfinitScroll() {
    $(window).on("scroll", function() {
        $('.previewContainer').addClass('infinitScroll');
        if ($(window).scrollTop() == $(document).height() - $(window).height()) {
            if ($('.previewContainer').length !== 0) {
                loadMoreContent();
            }
        }
    });
}
