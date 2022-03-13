from django.urls import path

from cal.views import CalendarView, EventView, index, EventUpdateView, EventDeleteView

app_name = 'event'
urlpatterns = [
    path('', index, name='index'),
    path('calendar/<str:month>/', CalendarView.as_view(), name='calendar'),
    path('event/new/', EventView.as_view(), name='new_event'),
    path('event/edit/<int:pk>/', EventUpdateView.as_view(), name='event_edit'),
    path('event/delete/<int:pk>/', EventDeleteView.as_view(), name='event_delete'),
]
