from django.urls import path
from . import views

urlpatterns = [
    path('division/', views.DivisionsViews.as_view()),
    path('department/', views.DepartmentsViews.as_view()),
    path('employement/', views.EmployementsViews.as_view()),
    path('designation/', views.DesignationViews.as_view()),
    path('faculties/', views.FacultiesViews.as_view()),
    path('faculties/add/', views.AddFacultiesViews.as_view()),
    path('faculties/update/<int:id>', views.UpdateFacultiesViews.as_view()),
    path('students/update/<int:id>', views.UpdateStudentViews.as_view()),
    path('student_listing/', views.StudentsViews.as_view()),
    path('student/add/', views.AddStudentsViews.as_view()),
    path('student/', views.StudentAPIView.as_view()),
    path('program_session/', views.get_program_session_batch,name='program_session'),
    path('program_class/', views.get_program_class,name='program_class'),
    path('batch_phase/', views.get_phase_batch,name='batch_phase'),
    path('program_phase_session/',views.get_programsession_phase,name='get_programsession_phase'),
    path('reporting_man/', views.get_reporting_manager_stcd,name='reporting_man'),
]
