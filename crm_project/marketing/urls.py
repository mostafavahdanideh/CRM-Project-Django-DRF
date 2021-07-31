from django.urls import path
from django.views.generic.edit import CreateView
from . import views


app_name = 'marketing'


urlpatterns = [
    path('follow-up-history/<int:pk>/', views.OrganizationFollowUpHistory.as_view(), name='follow_up_history'),
    path('create-quote/', views.CreateQuotes.as_view(), name='create_quote'),
    path('list-quote/', views.ListQuotes.as_view(),name='list_quotes'),
]
