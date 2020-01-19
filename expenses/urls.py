from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from shops import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.register(r'stores', views.StoreViewSet)
router.register(f'items', views.ItemViewSet)

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path('', include('shops.urls')),
    path('api/', include(router.urls)),
    path('api/user_stores/', views.UserStores.as_view(), name='user_stores'),
    path('api/purchase/', views.PurchaseItem.as_view(), name='purchase'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]

