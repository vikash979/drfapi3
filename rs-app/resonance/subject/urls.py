from django.urls import path
from . import views

urlpatterns = [
    path('master_subjects/', views.MasterSubjectViews.as_view()),
    path('subjects/', views.SubjectViews.as_view()),  
    path('class_subjects/', views.ClassSubjectViews.as_view()),
    

    path('class_subject/', views.get_class_subject_id,name='class_subject'),
    path('unit/',views.UnitCreationView.as_view()),
    path('chapter/',views.ChapterCreationView.as_view()),
    path('topic/',views.TopicCreationView.as_view()),
    path('sub_topic/',views.SubTopicCreationView.as_view()),
]