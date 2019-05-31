# pops/urls.py
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('case_study', views.CaseStudyViewSet)
router.register('run', views.RunViewSet)
router.register('output', views.OutputViewSet)
router.register('temperature_data', views.TemperatureDataViewSet)
router.register('lethal_temperature_data', views.LethalTemperatureDataViewSet)
router.register('precipitation_data', views.PrecipitationDataViewSet)


urlpatterns = [
    path('ajax', views.AJAXTestView.as_view(), name='ajax'),
    path('save_run_data', views.AJAXTestView.as_view(), name='save_run_data'),
    path('new_session', views.NewSessionView.as_view(), name='new_session'),
    path('case_study/help', TemplateView.as_view(template_name="pops/case_study_instructions.html"), name='case_study_help'),
    path('dashboard_layout', TemplateView.as_view(template_name="pops/dashboard/dashboard_layout.html")),
    path('spotted_lanternfly', TemplateView.as_view(template_name="pops/dashboard/spotted_lanternfly.html")),
    path('workspace', views.WorkspaceView.as_view(), name='workspace'),
    path('dashboard/<int:pk>', views.AJAXTestView.as_view(), name='dashboard'),
    path('case_study/create', views.CreateCaseStudyStart.as_view(), name='create_case_study_start'),
    path('case_study/create/new', views.NewCaseStudyView.as_view(), name='create_case_study'),
    path('case_study/<int:pk>/edit', views.NewCaseStudyView.as_view(), name='case_study_edit'),
    path('case_study/<int:pk>/extend', views.ExtendCaseStudyView.as_view(), name='case_study_extend'),
    path('case_study/list', views.ApprovedAndUserCaseStudyListView.as_view(), name='case_study_list'),
    path('case_study/<int:pk>/review', views.CaseStudyReview.as_view(), name='case_study_review'),
    path('case_study/submitted', views.case_study_submitted, name='case_study_submitted'),
    path('<int:pk>/', views.CaseStudyDetailView.as_view(), name='case-study'),
    path('api/', include(router.urls)),
    #path('case_study/<int:pk>/edit', views.case_study_edit, name='case_study_edit'),
    #path('myaccount', views.CaseStudyListView.as_view(), name='case-study-list'),
]