from django.urls import path
from .import views

urlpatterns = [
    path('api/v1/content_save',views.ContentSaver.as_view()),
  
]