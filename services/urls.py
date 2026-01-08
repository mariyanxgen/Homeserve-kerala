from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ServiceCategoryViewSet,
    ServiceProviderViewSet,
    ServiceViewSet,
    BookingViewSet,
    ReviewViewSet,
    ProviderPortfolioViewSet,
    ServiceRequestViewSet
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'categories', ServiceCategoryViewSet, basename='category')
router.register(r'providers', ServiceProviderViewSet, basename='provider')
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'portfolio', ProviderPortfolioViewSet, basename='portfolio')
router.register(r'service-requests', ServiceRequestViewSet, basename='service-request')

urlpatterns = [
    path('', include(router.urls)),
]
