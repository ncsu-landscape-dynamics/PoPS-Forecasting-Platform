# pops/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('case_study/create', views.create_case_study, name='create_case_study'),
    path('case_study/submitted', views.case_study_submitted, name='case_study_submitted'),
    path('case_study/<int:pk>/', views.case_study_details, name='case_study_details'),
]