"""pops_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('', include('pops.urls')),
    path('', include('team.urls')),
    path('', TemplateView.as_view(template_name="temp_landing.html"), name='temp_landing'),
    path('home/', TemplateView.as_view(template_name="landing_page.html"), name='landing_page'),
    path('about/', TemplateView.as_view(template_name="about.html"), name='about'),
    #path('team/', TemplateView.as_view(template_name="team.html"), name='team'),
    path('explore/', TemplateView.as_view(template_name="explore.html"), name='explore'),
    path('accounts/', include('users.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('faq', TemplateView.as_view(template_name="faqs.html"), name='FAQs'),
    path('tutorials', TemplateView.as_view(template_name="tutorials.html"), name='tutorials'),
    path('terms_and_conditions/', TemplateView.as_view(template_name="terms_and_conditions.html"), name='terms_and_conditions'),
    path('privacy_policy/', TemplateView.as_view(template_name="privacy_policy.html"), name='privacy_policy'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

 
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)