from django.urls import path

from cal.views import CalendarView

app_name = 'event'
urlpatterns = [
    path('', CalendarView.as_view(), name='index')
]
