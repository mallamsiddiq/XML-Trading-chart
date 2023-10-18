import django
from django.contrib.auth import login as auth_login, authenticate
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.views import LogoutView

from django.contrib import messages

from django.views.generic import ListView
from .forms import RegistrationForm, BaseLoginForm

User = django.contrib.auth.get_user_model()


class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'authapp/register.html'
    success_url = reverse_lazy('home')

    def get_success_url(self):
        redirect_url = self.request.GET.get('next', self.success_url)

        return redirect_url

    def form_valid(self, form):
        form.save()
        
        email = form.cleaned_data.get('email') or form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            auth_login(self.request, user)
            
        return super().form_valid(form)
    


class AuthLoginView(FormView):
    template_name = 'authapp/login.html'
    form_class = BaseLoginForm  # You may need to import AuthenticationForm
    success_url = reverse_lazy('home')  # Replace with the actual URL for the user dashboard

    def form_valid(self, form):
        email = form.cleaned_data.get('email') or form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(self.request, email=email, password=password)

        if user is not None:
            auth_login(self.request, user)
            
            messages.success(self.request, f'You have been successfully logged in as {email}')
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Invalid username or password')
            form.add_error(None, "Invalid login credentials")
            return self.form_invalid(form)

class LogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'authapp/logout.html'

