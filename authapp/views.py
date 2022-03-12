from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView

from authapp.forms import UserLoginForm, UserRegisterForm


class LoginListView(LoginView):
    template_name = 'authapp/login.html'
    form_class = UserLoginForm
    title = 'Колендарь событий - Авторизация'
    success_url = reverse_lazy('event:index')


class RegisterFormView(FormView):
    model = User
    template_name = 'authapp/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('authapp:login')
    title = 'GeekShop | Регистрация'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.set_level(request, messages.SUCCESS)
            messages.success(request, 'Вы успешно зарегистрировались! ')

            return HttpResponseRedirect(reverse('authapp:login'))
        else:
            messages.set_level(request, messages.ERROR)
            messages.success(request, 'Произошла ошибка регистрации! ')

            return HttpResponseRedirect(reverse('authapp:login'))

class Logout(LogoutView):
    template_name = "cal/calendar.html"
    success_url = reverse_lazy('event:index')
