from django.urls import path

from . import views

# app_name = 'shops'
urlpatterns = [
    path('stores/', views.stores, name='user_login'),
    path('stores/<int:store_id>/', views.stores_detail, name='store_details'),
    path('', views.index, name='dashboard')
]
