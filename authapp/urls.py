from django.urls import path

from authapp.views import LoginListView, RegisterFormView, Logout
from cal.views import CalendarView

app_name = 'authapp'
urlpatterns = [
    path('login/', LoginListView.as_view(), name='login'),
    path('register/', RegisterFormView.as_view(), name='register'),
    path('logout/', Logout.as_view(), name='logout'),
]
