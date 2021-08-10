from django.urls import path
from . import views


app_name = 'marketing'


urlpatterns = [
    path('create-quote/', views.CreateQuotes.as_view(), name='create_quote'),
    path('delete-quote/<int:pk>/', views.DeleteQuote.as_view(), name='delete_quote'),
    path('list-quote/', views.ListQuotes.as_view(),name='list_quotes'),
    path('detail-quote/<int:pk>/', views.DetailQuotes.as_view(),name='detail_quote'),
    path('download-quote/<int:pk>/', views.DownloadDetailQuote.as_view(), name='download-quote-pdf'),
    path('send-quote-to-email/', views.send_quote_email, name='quote-to-email'),
    path('follow-up-history-list/<int:pk>/', views.ListOrganizationFollowUpHistory.as_view(), name='follow_up_history_list'),
    path('create-follow-up/<int:pk>/', views.CreateOrganizationFollowUp.as_view(), name='create_follow_up'),
    path('update-quote/<int:quote_pk>/<int:organization_pk>/', views.EditQuotes.as_view(), name='update_quote'),
    path('list-quotes-emails-history/', views.ListQuoteEmailsHistory.as_view(), name='emails_history'),
]
