# pops/urls.py
from django.urls import path, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('case_study/help', TemplateView.as_view(template_name="pops/case_study_instructions.html"), name='case_study_help'),
    path('case_study/create', views.create_case_study, name='create_case_study'),
    path('case_study/<int:pk>/review', views.case_study_review, name='case_study_review'),
    path('case_study/submitted', views.case_study_submitted, name='case_study_submitted'),
    path('case_study/<int:pk>/', views.case_study_details, name='case_study_details'),
    path('case_study/<int:pk>/edit', views.case_study_edit, name='case_study_edit'),
    path('myaccount', views.CaseStudyListView.as_view(), name='case-study-list'),
    path('plot/', views.Graph.as_view(), name='plotly_test'), 
]