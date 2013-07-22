$(function() {
    _truncate_event_already_registered = false;
    truncate_overview = function(){
        var to_truncate = $('.box table.listing a.rollover');
        el_width = to_truncate.parent('td').width() - 30;
        to_truncate.css('width', el_width).smartTruncation();
    };
});
