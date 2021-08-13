from django.shortcuts import redirect, render
from django.utils import translation
from django.urls import reverse
from django.utils.http import is_safe_url


def show_home(request):
    return render(request=request, template_name="home.html")


def change_language(request):
    # we have to use LANGUAGE_CODE for activate
    translation.activate(request.GET.get("lang", "fa"))
    next_url = request.GET.get("next", reverse("home:home"))

    if is_safe_url(next_url, allowed_hosts=request.get_host()):
        return redirect(next_url)
    else:
        return redirect(next_url)
