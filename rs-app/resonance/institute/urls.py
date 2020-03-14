from django.urls import re_path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from institute import views

router = DefaultRouter()
#router.register(r'toc_model', views.TocModelViewSet)
#router.register(r'toc_model/get_list/', views.TocModelViewSet)

urlpatterns = [
    re_path('', include(router.urls)),
    re_path(r'^classs/$', views.ClassViews.as_view(), name="classs"),
    re_path(r'^center_finder$', views.CenterFinderApiView.as_view(), name="CenterFinderApiView"),
    re_path(r'^target_planner/$', views.TargetViews.as_view(), name='target_planner'),
    re_path(r'^edit_target/(?P<id>[0-9]+)/$', views.TargetViews.as_view(), name='edit_target'),
    re_path(r'^edit_class/(?P<id>[0-9]+)/$', views.ClassViews.as_view(), name='edit_class'),
    re_path(r'^program_class/$', views.ProgramViews.as_view(), name='program_class'),
    re_path(r'^edit_program_class/(?P<id>[0-9]+)/$', views.ProgramViews.as_view(), name='edit_program_class'),
    re_path(r'^sessions/$', views.SessionViews.as_view(), name='sessions'),
    re_path(r'^edit_sessions/(?P<id>[0-9]+)/$', views.SessionViews.as_view(), name='edit_sessions'),
    re_path(r'^phase/$', views.PhaseViews.as_view(), name='phase'),
    re_path(r'^edit_phase/(?P<id>[0-9]+)/$', views.PhaseViews.as_view(), name='edit_phase'),
    re_path(r'^batch/$', views.BatchViews.as_view(), name='batch'),
    re_path(r'^edit_batch/(?P<id>[0-9]+)/$', views.BatchViews.as_view(), name='edit_batch'),
    re_path(r'^get_corresponding_objects/$', views.corresponding_objects, name="get_corresponding_objects"),
    re_path(r'^lecture-planner/$', views.LecturePlannerView.as_view(), name="LecturePlannerView"),
    re_path(r'^create_lecture/$', views.create_lecture, name="create_lecture"),
    re_path(r'^delete_lecture/$', views.delete_lecture, name="delete_lecture"),   
    re_path(r'^edit_lecture_planner/(?P<pk>[0-9]+)/$', views.EditLecturePlanner.as_view(), name='edit_lecture_planner'),
    re_path(r'^csc_finder$', views.CscFinderApiView.as_view(), name="CscFinderApiView"),
    re_path(r'^centers/$', views.CenterView.as_view(), name='CenterView'),
    re_path(r'^get_toc_by_subject_id/$', views.get_toc_by_subject_id, name='get_toc_by_subject_id'),
    re_path(r'^create_lecture_toc_mapping/$', views.create_lecture_toc_mapping, name='create_lecture_toc_mapping'),
    re_path(r'^dpp/$', views.DppView.as_view(), name="DppView"),
   # re_path(r'^toc_model/$', views.TocModelViewSet.as_view({'get': 'list', 'post': 'create'}), name='toc_model'),
    #re_path(r'^toc_models/get_list/(?P<pk>[0-9]+)/$', views.TocModelViewSet.as_view({'get': 'list', 'post': 'create'}), name='toc_modelss'),
    re_path(r'^edit_lecture_planner/(?P<pk>[0-9]+)/$', views.EditLecturePlanner.as_view(), name='edit_lecture_planner'),
    re_path(r'^edit-dpp/(?P<pk>[0-9]+)/$', views.DppEditView.as_view(), name="edit_dpp"),

    re_path(r'^toc_lists/$', views.TocViews.as_view(), name="toc_lists"),
    re_path(r'^tocunit/$', views.TocUnitModelViewSet.as_view(), name="tocunit"),
    #re_path(r'^toc_model/get_list/(?P<pk>[0-9]+)/$', views.TocModelViewSet.as_view({'get': 'get_list'}), name='get_list'),

    
    re_path('', include(router.urls)),

    re_path(r'^created-lecture-toc-ids/$', views.CreatedLectureTocIds, name="created_lecture_toc_ids"),
    re_path(r'^edit-dpp/(?P<pk>[0-9]+)/$', views.DppEditView.as_view(), name="edit_dpp"),
    re_path(r'^get_dpp_by_subject_id/$', views.get_dpp_by_subject_id, name='get_dpp_by_subject_id'),
    re_path(r'^update_dpp_release_status/$', views.update_dpp_release_status, name='update_dpp_release_status'),
    re_path(r'^study-material/$', views.StudyMaterialView.as_view(), name='study_material'),
    re_path(r'^content/$', views.ContentView.as_view(), name='content'),
    re_path(r'^content/sm/create$', views.ContentSMCreateView.as_view(), name='content_sm_create'),
    re_path(r'^content/sm/edit/(?P<id>[0-9]+)/$', views.ContentSMEditView.as_view(), name='content_sm_edit'),
    re_path(r'^content/smpreview/(?P<sm_id>[0-9]+)/$', views.ContentSMPreviewView.as_view(), name='content_sm_preview'),
    re_path(r'^content/sm/list$', views.ContentSMListView.as_view(), name='content_sm_list'),
    
    re_path(r'^get_toc_by_subject_and_class/$', views.get_toc_by_subject_and_class, name='get_toc_by_subject_and_class'),
    re_path(r'^create_study_material/$', views.create_study_material, name='create_study_material'),
    re_path(r'^upload_content_data/$', views.upload_content_data, name='upload_content_data'),
    re_path(r'^program_class_subject/(?P<id>[0-9]+)/$', views.Program_Class_subjectViews.as_view(), name='Program_Class_subjectViews'),
    re_path(r'^program_class_subject/$', views.Program_Class_subjectViews.as_view(), name='Program_Class_subjectViews'),
    re_path(r'^program_session/$', views.ProgramSessionView.as_view(), name="program_session"),
    re_path(r'^session_program/$', views.session_program, name="session_program"),
    re_path(r'^login/$', views.LoginViews.as_view(), name='login'),
    re_path(r'^logout/$', views.logout_request, name="logout"),
    re_path(r'^created-dpps/$', views.created_dpps, name="created_dpps"),

]