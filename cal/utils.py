import calendar
from datetime import datetime, date

from .models import Event


class Calendar(calendar.LocaleHTMLCalendar):

    def get_events_day(self, events_per_day):
        events = ''
        for event in events_per_day:
            events += f" <li> <span class ='title'>" \
                      f"<a href='/event/edit/{event.pk}'>{event.title}</a>" \
                      f" </span > <span class ='desc' >{event.description}</span ></li>\n"

        return f"<div class='events'> <ul style = 'opacity: 0' > {events} </ul> </div>"

    def formatday(self, day, year, month, events):
        events_per_day = events.filter(date_event__day=day)

        day_event = ''
        if events_per_day.count() > 0:
            day_event = self.get_events_day(events_per_day)

        if day_event != '':
            return f"<td class='date_has_event'><span  class='date'> {day}</span> {day_event}</td>"
        if date(year, month, max(day, 1)) == datetime.today().date():
            return f"<td class='today'><span  class='date'>{day}</span></td>"
        elif day != 0:
            return f"<td class='date'><span>{day}</span></td>"

        return "<td class='padding'></td>"

    def formatweek(self, theweek, year, month, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, year, month, events)
        return f'<tr> {week} </tr>'

    def formatmonth(self, user=None, year=None, month=None, withyear=True):
        events = Event.objects.filter(user__pk=user.pk, date_event__year=year, date_event__month=month)
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(year, month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(year, month):
            cal += f'{self.formatweek(week, year, month, events)}\n'
        cal += f'{self.formatweekheader()}\n'
        return cal
