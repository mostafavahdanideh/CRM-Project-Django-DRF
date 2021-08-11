"""crm_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from organization import views as organization_views
from users import views as users_view


urlpatterns = [
    path("", include('users.urls', namespace="experts")),
    path('organization/', include('organization.urls', namespace='our-organization')),
    path('marketing/', include('marketing.urls', namespace='marketing')),
    path('inventory/', include('inventory.urls', namespace='inventory')),
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('api/auth/', include('rest_auth.urls')),
    path('api/organizations/', organization_views.OrganizationsListAPIView.as_view(), name='organizations'),
    path('api/users/<int:pk>/', users_view.UserDetailAPIView.as_view(), name='user-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
