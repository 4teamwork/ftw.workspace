jQuery(function($) {

     /*calander navigation*/
     $('a.#calendar-previous, a.#calendar-next').live(
       'click',
       function(e, o) {
         var month = $.find_param(this.href)['amp;month:int'];
         var year = $.find_param(this.href)['year:int'];
         tabbedview.param('month:int', month);
         tabbedview.param('year:int', year);
         tabbedview.reload_view();
         e.preventDefault();
         e.stopPropagation();
       });

     $('td.event a,  td.todayevent a').live(
       'click',
       function(e, o) {
         // tell the calendar tooltip to hide, because we will hide
         // the link and switch view...
         $(this).trigger('mouseleave');
         tabbedview.searchbox.val(this.id);
         tabbedview.prop('searchable_text', this.id);
         tabbedview.param('view_name', 'events');
         tabbedview.reload_view();
         e.preventDefault();
         e.stopPropagation();
       });

     $('.tabbedview_view').bind(
       'reload',
       function(e, o) {

      /*calendar tooltip*/
             $('td.event a, td.todayevent a').tooltip(
                 {showURL: false,
                  track: true,
                  fade: 250,
                  top:20,
                  left:15
                  });
           });

   });
