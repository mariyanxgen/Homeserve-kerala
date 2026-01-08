"""
URL patterns for frontend views (server-side rendered)
"""
from django.urls import path
from .frontend_views import (
    home_view, services_view, service_detail_view, provider_detail_view,
    book_service_view, booking_confirmation_view, how_it_works_view,
    dashboard_view, provider_dashboard_view, customer_dashboard_view,
    provider_confirm_booking_view, provider_complete_booking_view, customer_cancel_booking_view
)
from .auth_views import (
    register_view, login_view, logout_view, profile_view, provider_onboarding_view
)

urlpatterns = [
    # Frontend pages
    path('', home_view, name='home'),
    path('services/', services_view, name='services'),
    path('how-it-works/', how_it_works_view, name='how_it_works'),
    path('service/<int:service_id>/', service_detail_view, name='service_detail'),
    path('provider/<int:provider_id>/', provider_detail_view, name='provider_detail'),
    
    # Booking
    path('book/<int:service_id>/', book_service_view, name='book_service'),
    path('booking/confirmation/<int:booking_id>/', booking_confirmation_view, name='booking_confirmation'),
    
    # Dashboards
    path('dashboard/', dashboard_view, name='dashboard'),
    path('dashboard/provider/', provider_dashboard_view, name='provider_dashboard'),
    path('dashboard/customer/', customer_dashboard_view, name='customer_dashboard'),
    # Dashboard actions
    path('dashboard/provider/booking/<int:booking_id>/confirm/', provider_confirm_booking_view, name='provider_confirm_booking'),
    path('dashboard/provider/booking/<int:booking_id>/complete/', provider_complete_booking_view, name='provider_complete_booking'),
    path('dashboard/customer/booking/<int:booking_id>/cancel/', customer_cancel_booking_view, name='customer_cancel_booking'),

    # Authentication
    path('register/', register_view, name='register'),
    path('register/provider/', provider_onboarding_view, name='provider_onboarding'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
]
