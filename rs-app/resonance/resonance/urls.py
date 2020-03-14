"""resonance URL Configuration

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
from django.urls import path, include
from users import views as users_views
from subject import views as subject_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',users_views.EmptyView.as_view()),
    path('student/', users_views.StudentCreateView.as_view()),
    path('api/v1/', include('apis.urls')),
    path('dashboard/',users_views.DashboardView.as_view()),
    path('content/', include('content.urls')),

    path('user/', include('users.urls')),
    path('subject/', include('subject.urls')),
    path('institute/', include('institute.urls')),

   # path('institute/', users_views.StudentCreateView.as_view()),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
