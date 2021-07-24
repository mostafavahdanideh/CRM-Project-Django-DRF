from django.urls import path
from . import views


app_name = "expert"


urlpatterns = [
    path('', views.LoginUsers.as_view(), name='login-redirect'),
    path('login/', views.LoginUsers.as_view(), name='login'),
    path('logout/', views.LogoutUsers.as_view(), name='logout'),
]
