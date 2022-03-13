import calendar
from datetime import datetime, timedelta, date

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django.views import generic

from cal.models import Event
from .forms import EventForm

from .utils import Calendar


def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = str(next_month.year) + '-' + str(next_month.month)
    return month


def index(request):
    return HttpResponseRedirect(f'calendar/{datetime.today().year}-{datetime.today().month}')


class CalendarView(generic.ListView):
    model = Event
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        d = get_date(self.kwargs.get('month', None))

        cal = Calendar(locale='Russian_Russia')

        html_cal = cal.formatmonth(self.request.user, d.year, d.month, withyear=True)

        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)

        return context


class EventView(generic.FormView):
    model = Event
    template_name = 'cal/event.html'
    form_class = EventForm

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


class EventUpdateView(generic.UpdateView):
    model = Event
    template_name = 'cal/event-update-detele.html'
    form_class = EventForm
    success_url = reverse_lazy('event:index')


class EventDeleteView(generic.DeleteView):
    model = Event
    template_name = 'cal/event-update-detele.html'
    success_url = reverse_lazy('event:index')

    def delete(self, request, *args, **kwargs):
        messages.set_level(request, messages.ERROR)
        messages.error(request, 'Событие удалено!')

        return HttpResponseRedirect(reverse('event:index'))
