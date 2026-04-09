from django.urls import path
from . import views

urlpatterns = [
    path('', views.pricelist_list, name='pricelist_list'),
]
