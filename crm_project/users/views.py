from django.shortcuts import render, redirect
from django.contrib.auth import views


class LoginUsers(views.LoginView):
    template_name = 'login_form.html'

    def get(self, request, *args: str, **kwargs):
        if request.path == "/":
            return redirect("expert:login")
        return super().get(request, *args, **kwargs)


class LogoutUsers(views.LogoutView):
    pass
