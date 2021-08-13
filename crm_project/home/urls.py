from django.urls.conf import path
from . import views


app_name = 'home'


urlpatterns = [
    path('', views.show_home, name='home'),
    path('change-lang/', views.change_language, name='change_language')
]
