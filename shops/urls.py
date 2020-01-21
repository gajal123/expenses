from django.urls import path

from . import views

urlpatterns = [
    # path('stores/', views.stores, name='stores'),
    path('stores/', views.stores, name='user_login'),
    path('index/', views.index, name='dashboard')
]