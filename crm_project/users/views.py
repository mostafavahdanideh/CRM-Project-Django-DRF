from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import views


class LoginUsers(views.LoginView):
    template_name = 'login_form.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("organization:list")
        return super().get(request, *args, **kwargs)

    def form_invalid(self, form):
        messages.info(self.request, form.errors)
        return super().form_invalid(form)


class LogoutUsers(views.LogoutView):
    pass
