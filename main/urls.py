from django.urls import path
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    path('', views.home, name='main-home'),
    path('load_persons', views.person_load, name='load-persons'),
    path('notification_allow', views.notification_allow, name='notification-allow'),
    path('loader/', TemplateView.as_view(template_name='main/loader.html')),
]
