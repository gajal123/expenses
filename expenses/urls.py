from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from shops import views

router = routers.DefaultRouter()
router.register(r'stores', views.StoreViewSet)
router.register(f'items', views.ItemViewSet)
router.register(f'purchases', views.PurchaseViewSet)

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path('', include('shops.urls')),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

