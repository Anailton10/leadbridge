from django.contrib.auth.views import LoginView
from .forms import CustomAuthForm


class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = CustomAuthForm
