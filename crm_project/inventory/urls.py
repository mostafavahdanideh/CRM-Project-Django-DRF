from django.urls import path
from . import views


app_name = 'inventory'


urlpatterns = [
    path('add-product/', views.AddCompanyProduct.as_view(), name='add-company-product'),
    path('list-products/', views.ListCompanyProduct.as_view(), name='list-company-products'),
    path('detail-product/<int:pk>/', views.DetailCompanyProduct.as_view(), name='detail-company-product'),
    path('update-product/<int:pk>/', views.UpdateCompanyProduct.as_view(), name='update-company-product'),
]
