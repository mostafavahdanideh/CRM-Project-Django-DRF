from django.urls import path
from . import views


app_name = 'marketing'


urlpatterns = [
    path('follow-up-history/<int:pk>/', views.OrganizationFollowUpHistory.as_view(), name='follow_up_history'),
]
