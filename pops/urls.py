# pops/urls.py
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('case_study', views.CaseStudyViewSet)
#router.register('run', views.RunViewSet)
router.register('run', views.RunModelWriteViewSet)
router.register('run_collection', views.RunCollectionModelWriteViewSet)
router.register('run_detail', views.RunDetailViewSet)
router.register('run_collection_detail', views.RunCollectionDetailViewSet)
#router.register('run_collection', views.RunCollectionViewSet)
router.register('output', views.OutputViewSet)
router.register('temperature_data', views.TemperatureDataViewSet)
router.register('lethal_temperature_data', views.LethalTemperatureDataViewSet)
router.register('precipitation_data', views.PrecipitationDataViewSet)
router.register('session', views.SessionModelWriteViewSet)
router.register('session_detail', views.SessionDetailViewSet)


urlpatterns = [
    #path('ajax', views.AJAXTestView.as_view(), name='ajax'),
    path('plots', TemplateView.as_view(template_name="pops/dashboard/plotting_test.html")),
    path('output/<int:pk>', views.OutputDetailView.as_view(), name='output_detail'),
    path('get_output', views.get_output_view, name='get_output'),
    path('get_run_collection', views.get_run_collection, name='get_run_collection'),
    path('check_status', views.check_status, name='check_status'),
    path('check_for_new_TL_run', views.check_for_new_TL_run, name='check_for_new_TL_run'),
    path('delete_runs', views.delete_runs, name='delete_runs'),
    path('edit_run_collection', views.edit_run_collection, name='edit_run_collection'),
    path('delete_run_collection', views.delete_run_collection, name='delete_run_collection'),
    path('save_run_data', views.NewRunView.as_view(), name='save_run_data'),
    path('save_run_collection_data', views.DashboardView.as_view(), name='save_run_collection_data'),
    path('save_session_data', views.NewSessionView.as_view(), name='save_session_data'),
    path('save_run_collection_data_test', views.DashboardTestView.as_view(), name='save_run_collection_data_test'),
    path('session/new', views.NewSessionView.as_view(), name='new_session'),
    path('session/list', views.SessionListView.as_view(), name='session_list'),
    path('session/share/<int:pk>', views.SessionShareView.as_view(), name='session_share'),
    path('case_study/help', TemplateView.as_view(template_name="pops/case_study_instructions.html"), name='case_study_help'),
    path('dashboard_layout', TemplateView.as_view(template_name="pops/dashboard/dashboard_layout.html")),
    path('spotted_lanternfly', TemplateView.as_view(template_name="pops/dashboard/spotted_lanternfly.html")),
    path('workspace', views.WorkspaceView.as_view(), name='workspace'),
    path('dashboard/<int:pk>', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/', RedirectView.as_view(pattern_name='workspace'), name='dashboard_root'),
    path('dashboard-test/<int:pk>', views.DashboardTestView.as_view(), name='dashboard-test'),
    path('case_study/create', views.CreateCaseStudyStart.as_view(), name='create_case_study_start'),
    path('case_study/create/new', views.NewCaseStudyView.as_view(), name='create_case_study'),
    path('case_study/<int:pk>/edit', views.NewCaseStudyView.as_view(), name='case_study_edit'),
    path('case_study/<int:pk>/extend', views.ExtendCaseStudyView.as_view(), name='case_study_extend'),
    path('case_study/list', views.ApprovedAndUserCaseStudyListView.as_view(), name='case_study_list'),
    path('case_study/<int:pk>/review', views.CaseStudyReview.as_view(), name='case_study_review'),
    path('case_study/submitted', views.case_study_submitted, name='case_study_submitted'),
    path('cs/<int:pk>/', views.CaseStudyDetailView.as_view(), name='case-study'),
    path('api/', include(router.urls)),
    #path('case_study/<int:pk>/edit', views.case_study_edit, name='case_study_edit'),
    #path('myaccount', views.CaseStudyListView.as_view(), name='case-study-list'),
]