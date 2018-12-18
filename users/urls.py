# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    #path('signup/', views.SignUp.as_view(), name='signup'),
    path('signup/', views.sign_up, name='signup'),
    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

]