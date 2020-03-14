from django.urls import path
from . import views
import content.views as content_views
urlpatterns = [
    path('notes/detail', views.NoteViewAPIView.as_view()),
    path('notes/access', views.NotesAccessAPIView.as_view()),
    path('video/detail', views.VideoViewAPIView.as_view()),
    path('video/access', views.VideoAccessAPIView.as_view()),
    path('lectures', content_views.LectureListAPIView.as_view()),
    path('toc-list', views.TOCListView.as_view()),
    path('video/<pk>/detail', views.VideoView.as_view()),
    path('solved-examples', views.SolvedExampleView.as_view()),
    path('assessment-preview', views.AssesmentPreviewView.as_view()),
    path('assessment-attempt', views.AssesmentAttemptView.as_view()),
    path('question-submit', views.AttempQuestionSaveView.as_view()),
    path('attempt-submit', views.AssesmentAttemptSaveView.as_view()),
    path('assessment-review', views.AssessmentAttemptReviewView.as_view()),
    path('dpp-list', views.DPPListView.as_view()),
    path('exercises-list', views.ExerciseListView.as_view()),
    path('faculty/todo', views.FacultyToDoView.as_view()),
    path('assessment-scorecard', views.AssessmentScorecardView.as_view()),
]
