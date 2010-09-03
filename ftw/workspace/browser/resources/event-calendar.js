jq(function() {

     /*calander navigation*/
     jq('a.#calendar-previous, a.#calendar-next').live(
       'click',
       function(e, o) {
         var month = jq.find_param(this.href)['amp;month:int'];
         var year = jq.find_param(this.href)['year:int'];
         tabbedview.param('month:int', month);
         tabbedview.param('year:int', year);
         tabbedview.reload_view();
         e.preventDefault();
         e.stopPropagation();
       });

     jq('td.event a,  td.todayevent a').live(
       'click',
       function(e, o) {
         tabbedview.searchbox.val(this.id);
         tabbedview.prop('searchable_text', this.id);
         tabbedview.param('view_name', 'events');
         tabbedview.reload_view();
         e.preventDefault();
         e.stopPropagation();
       });

     jq('.tabbedview_view').bind(
       'reload',
       function(e, o) {

         /* rollover description */
         jq('a.rollover-description').tooltip(
           {showURL: false,
            track: true,
            fade: 250
           });

         /*calendar tooltip*/
         jq('td.event a, td.todayevent a').tooltip(
           {showURL: false,
            track: true,
            fade: 250
           });
       });

   });