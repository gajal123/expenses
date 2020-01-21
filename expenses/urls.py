from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from shops import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
# router.register(r'stores', views.StoreViewSet)
router.register(r'payments', views.PaymenOutstandingViewSet)

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path('', include('shops.urls')),
    path('api/', include(router.urls)),
    path('api/stores/', views.StoreView.as_view(), name='all_stores'),
    path('api/user_payment/', views.UserPayments.as_view(), name='user_payment'),
    path('api/purchase/', views.PurchaseItem.as_view(), name='purchase'),
    path('api/items/', views.UserItem.as_view(), name='purchase'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]

