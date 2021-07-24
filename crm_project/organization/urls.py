from django.urls import path
from . import views

app_name = 'organization'

urlpatterns = [
    path('register/', views.say_hello, name="register"),
]