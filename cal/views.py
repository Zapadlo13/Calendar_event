from datetime import datetime

from django.utils.safestring import mark_safe
from django.views import generic

from cal.models import Event

from .utils import Calendar


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return datetime.date(year, month, day=1)
    return datetime.today()


class CalendarView(generic.ListView):
    model = Event
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(locale='Russian_Russia')

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(d.year, d.month,withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context
