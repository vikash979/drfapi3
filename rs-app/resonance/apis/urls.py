from django.urls import path, include
import users.views as user_views
urlpatterns = [
    path('auth/', include('apis.auth.urls')),
    path('students/', include('apis.student.urls')),
    path('content/', include('apis.content.urls')),
    path('faculty/', include('apis.faculty.urls')),
    path('profile', user_views.StudentAPIView.as_view()),
    path('dashboard', user_views.DashboardAPIView.as_view()),
]
