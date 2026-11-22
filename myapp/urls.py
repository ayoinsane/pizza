from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'cart', views.CartViewSet, basename='cart')
router.register(r'orders', views.OrderViewSet, basename='orders')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/register/', views.register_view),
    path('api/auth/login/', views.login_view),
    path('api/auth/logout/', views.logout_view),
    path('api/auth/user/', views.user_info_view),
]