from django.http.response import HttpResponse
from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.


def say_hello(request):
    return render(request=request, context={'retult': True}, template_name="register.html")