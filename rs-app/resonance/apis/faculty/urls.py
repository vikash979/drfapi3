from django.urls import path
from . import views
import content.views as content_views
import users.views as user_views

urlpatterns = [
    path('todo', views.FacultyTodoListAPIView.as_view()),
    path('releasing-lecture-content', views.LectureContentReleasingAPIView.as_view()),
 	path('lectures', content_views.FacultyLectureListAPIView.as_view()),
 	path('release-lecture-content', views.LectureContentReleaseView.as_view()),
    path('release-dpp', views.DPPReleaseView.as_view()),
    path('lecture-toc-delivered', views.LectureTOCDeliveredView.as_view()),
    path('create-exercise', views.ExerciseCreateView.as_view()),
    path('toc-content', views.TOCContentView.as_view()),
    path('profile', user_views.FacultyAPIView.as_view()),
    path('exercises-summary', views.FacultyExerciseListAPIView.as_view()),
    path('dpp-summary', views.FacultyExerciseListAPIView.as_view()),
    path('assessment-review', views.AssessmentAttemptReviewView.as_view()),
	path('question-student-responses', views.QuestionStudentResponsesListAPI.as_view()),
    path('faculty-dpps-to-release',views.FacultyDPPtoReleaseView.as_view()),
]
