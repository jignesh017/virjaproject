from django.urls import path
from . import views

urlpatterns = [
    path('', views.brand_list, name='brand_list'),
]
