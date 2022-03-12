from datetime import datetime, timedelta
from calendar import LocaleHTMLCalendar, HTMLCalendar

from django.utils.safestring import mark_safe

from .models import Event


class Calendar(LocaleHTMLCalendar):

    def get_events_day(self, events_per_day):
        events = ''
        for event in events_per_day:
            events += f" <li> <span class ='title'> {event.title} </span > <span class ='desc' >{event.description}</span ></li>"

        return f"<div class='events'> <ul style = 'opacity: 0' > {events} </ul> </div>"

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events):
        events_per_day = events.filter(date_event__day=day)

        day_event = ''
        if events_per_day.count() > 0:
            day_event = self.get_events_day(events_per_day)

        if day_event != '':
            return f"<td class='date_has_event'><span  class='date'> {day}</span> {day_event}</td>"
        if day == datetime.today().day:
            return f"<td class='today'><span  class='date'> <a class='date' href='event'>{day}</a></span></td>"
        elif day != 0:
            return f"<td class='date'><span><a  class='date' href='event'>{day}</a></span></td>"

        return "<td class='padding'></td>"

    # formats a week as a tr
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, user=None, year=None, month=None, withyear=True):
        events = Event.objects.filter(user__pk=user.pk, date_event__year=year, date_event__month=month)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(year, month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(year, month):
            cal += f'{self.formatweek(week, events)}\n'
        cal += f'{self.formatweekheader()}\n'
        return cal
