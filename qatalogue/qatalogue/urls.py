"""qatalogue URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path, include
from main import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    path('dealer_registration/', views.dealer_registration),
    path('registration/', views.registration),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'^producers/(?P<id>\d+)', views.producer),
    re_path(r'^ads/dealers/(?P<name>\w+)', views.dealer),
    re_path(r'^ads/search', views.search, name='search'),
    re_path(r'^ads/(?P<category>\w+)/add_product', views.add_product),
    re_path(r'^ads/(?P<category>\w+)/add', views.add_ad),
    re_path(r'^ads/(?P<category>\w+)/(?P<id>\d+)', views.ad),
    re_path(r'^ads/(?P<category>\w+)', views.ads),
    re_path(r'^dealers', views.dealers),
    path('', views.main_paige),
    path('admin/', admin.site.urls),
]
