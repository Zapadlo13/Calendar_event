from datetime import datetime

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views import generic

from cal.models import Event
from .forms import NewEventForm

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
        html_cal = cal.formatmonth(self.request.user, d.year, d.month, withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context


class EventView(generic.FormView):
    model = Event
    template_name = 'cal/event.html'
    form_class = NewEventForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():

            event = form.save(commit=False)
            event.user = request.user
            event.save()

            messages.set_level(request, messages.SUCCESS)
            messages.success(request, 'Добавленно новое событие! ')

            return HttpResponseRedirect(reverse('event:index'))
        else:
            messages.set_level(request, messages.ERROR)
            messages.error(request, 'Произошла ошибка! ')

            return HttpResponseRedirect(reverse('event:index'))

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            messages.set_level(request, messages.ERROR)
            messages.error(request, 'Нельзя добавлять события без авторизации.')

            return HttpResponseRedirect(reverse('event:index'))
        return render(request, self.template_name, {'form': self.form_class})
