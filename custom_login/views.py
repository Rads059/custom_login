from datetime import date, timedelta
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from . import forms
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin


class SignupView(FormView):
    form_class = forms.SignupForm
    template_name= 'custom_login/signup.html'
    success_url= reverse_lazy('dashboard')
    password_reset=reverse_lazy('pass_reset')

    def form_valid(self, form):
        user=form.save(commit=False)
        user.save()
        login(self.request, user)
        if user is not None:
            if user.is_active:
                if date.today() - user.password_date > timedelta(days=90):
                    return HttpResponseRedirect(self.password_reset)
                return HttpResponseRedirect(self.success_url)

        return super().form_valid(form)

def Dashboard(request):
    """ make dashboard view """
    return render(request, 'custom_login/dashboard.html')


def Logout(request):
    """logout logged in user"""
    logout(request)
    return HttpResponseRedirect(reverse_lazy('login:dashboard'))


class LoginView(FormView):
    """login view"""

    form_class = forms.LoginForm
    success_url = reverse_lazy('login:dashboard')
    template_name = 'custom_login/login.html'

    def form_valid(self, form):
        """ process user login"""
        credentials = form.cleaned_data

        user = authenticate(username=credentials['email'],
                            password=credentials['password'])

        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(self.success_url)

        else:
            messages.add_message(self.request, messages.INFO, 'Wrong credentials\
                                please try again')
            return HttpResponseRedirect(reverse_lazy('login'))

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'custom_login/password_reset.html'
    email_template_name = 'custom_login/password_reset_email.html'
   
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('login:dashboard')
