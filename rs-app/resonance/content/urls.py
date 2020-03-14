from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^lectures/$', views.LectureListAPIView.as_view()),
    re_path(r'^add_question_bank/$', views.QuestionTemplateView.as_view(), name="add_question_bank"),
    re_path(r'assessment_create/$', views.AssessmentCreateTemplateView.as_view(), name="AssessmentCreateTemplateView"),
    re_path(r'assessment_edit/(?P<id>\d+)/$', views.AssessmentEditTemplateView.as_view(), name="AssessmentEditTemplateView"),
    re_path(r'^assessment/$', views.AssessmentTemplateView.as_view(), name="AssessmentTemplateView"),
    re_path(r'^assessment_section/(?P<id>\d+)/$', views.AssessmentSectionQuestionTemplateView.as_view(), name="AssessmentSectionQuestionTemplateView"),
    re_path(r'^assessment_question_list/(?P<id>\d+)/$', views.AssessmentSectionListView.as_view(), name="AssessmentSectionListView"),
    re_path(r'^add_assessment_section/(?P<id>\d+)/$', views.AddSectionView.as_view(), name="AddSectionView"),
    re_path(r'^question_bank/$', views.QuestionListTemplateView.as_view(), name="QuestionListTemplateView"),
    re_path(r'^assessment_section_edit/(?P<assessment_id>\d+)/(?P<edit_id>\d+)/$', views.AssessmentSectionEditTemplateView.as_view(), name="AssessmentSectionEditTemplateView"),
    re_path(r'^assessment_question/(?P<id>\d+)/$', views.AssessmentSectionAddQuestionTemplateView.as_view(), name="AssessmentSectionAddQuestionTemplateView"),
]
