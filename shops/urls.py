from django.urls import path

from . import views

urlpatterns = [
    path('stores/', views.stores, name='stores'),
    path('index/', views.index, name='dashboard')
]