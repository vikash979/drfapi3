from django.urls import path
from . import views

urlpatterns = [
    path('toc/<pk>/detail/', views.TOCDetailView.as_view()),
    
    path('dashboard', views.DashboardAPIView.as_view()),
    

]