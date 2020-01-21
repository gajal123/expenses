from django.urls import path

from . import views

urlpatterns = [
    path('stores/', views.stores, name='user_login'),
    path('', views.index, name='dashboard')
]