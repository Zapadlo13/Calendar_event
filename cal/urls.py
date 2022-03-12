from django.urls import path

from cal.views import CalendarView, EventView

app_name = 'event'
urlpatterns = [
    path('', CalendarView.as_view(), name='index'),
    path('event/', EventView.as_view(), name='new_event')
]
