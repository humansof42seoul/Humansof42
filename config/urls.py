"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include
from interview.views import interview_list, about
from user.views import log_out
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', interview_list, name="main"),
    path('about/', about),
    path('admin/', admin.site.urls),
    path('login/', include('user.urls')),
    path('logout/', log_out, name="logout"),
    path('interviews/', include('interview.urls')),
    path('summernote/', include('django_summernote.urls')),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
