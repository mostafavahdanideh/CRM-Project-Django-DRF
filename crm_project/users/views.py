from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import get_user_model, views
from rest_framework import generics
from . import serializers


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


class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializers
    