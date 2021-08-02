from django.urls import path
from django.views.generic.edit import CreateView
from . import views


app_name = 'marketing'


urlpatterns = [
    path('follow-up-history/<int:pk>/', views.OrganizationFollowUpHistory.as_view(), name='follow_up_history'),
    path('create-quote/', views.CreateQuotes.as_view(), name='create_quote'),
    path('list-quote/', views.ListQuotes.as_view(),name='list_quotes'),
    path('detail-quote/<int:pk>/', views.DetailQuotes.as_view(),name='detail_quote'),
    path('download-quote/<int:pk>/', views.DownloadDetailQuote.as_view(), name='download-quote-pdf'),
    path('send-quote-to-email/', views.send_quote_email, name='quote-to-email')
]
