from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact, name='contact'),
    path('capture-download/', views.capture_download_lead, name='capture_download_lead'),
]
