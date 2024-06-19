from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import UpdateView
from django.contrib.auth import get_user_model
from StockTaking import settings
from home.forms import AddTaskForm
from .models import Group

from users.forms import LoginUserForm, ProfileUserForm, RegisterUserForm, UserPasswordChangeForm

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

def logout_user(request):
    logout(request)
    return redirect('/users/login/')
    #return HttpResponse('Вы вышли!')

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация', 'default_image': settings.DEFAULT_USER_IMAGE}
    success_url = reverse_lazy('users')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            group = form.cleaned_data['group']
            group.user_set.add(self.object)
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': "Профиль пользователя", 'default_image': settings.DEFAULT_USER_IMAGE}

    def get_success_url(self):
        return reverse_lazy('profile')
    
    def get_object(self, queryset=None):
        return self.request.user
    
class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'users/password_change_form.html'

class GetUsers(PermissionRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'users/users.html'
    context_object_name = 'users'
    title_page = 'Пользователи'
    permission_required = 'home.view_users'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        
        return context
    
    def get_queryset(self):
        return get_user_model().objects.all()
    