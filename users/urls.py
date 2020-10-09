# users/urls.py
from django.urls import path
from . import views
from django.views.generic import TemplateView, RedirectView


# These are for the custom user views. We are still using some of django's
# built-in user views in django.contrib.auth.urls (like login and password_reset). The
# path to the custom URLs is listed in the pops_website/urls.py file.
urlpatterns = [
    path('signup/', views.sign_up, name='signup'),
    path('account_activation_sent/', views.account_activation_sent, 
         name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('my_account/', views.my_account, name='my_account'),
    path('update/', views.UpdateAccount.as_view(), name='update_account'),
    path('email_list/add', views.AddNewEmail.as_view(), name='add_email'),
    path('temp_email_add/', TemplateView.as_view(template_name="accounts/add_email.html"), name="temp_email_add"),
]
