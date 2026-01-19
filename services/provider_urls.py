"""
URL patterns for provider portal
"""
from django.urls import path
from .provider_views import (
    provider_home,
    provider_services,
    add_service,
    edit_service,
    delete_service,
    provider_bookings,
    confirm_booking,
    complete_booking,
    cancel_booking,
    booking_detail,
    provider_earnings,
    provider_messages_page,
    provider_calendar,
    set_availability,
    add_leave,
    provider_profile_page,
    edit_profile,
    change_password,
    provider_reviews,
)

app_name = 'provider'

urlpatterns = [
    path('', provider_home, name='home'),
    path('services/', provider_services, name='services'),
    path('services/add/', add_service, name='add_service'),
    path('services/edit/<int:service_id>/', edit_service, name='edit_service'),
    path('services/delete/<int:service_id>/', delete_service, name='delete_service'),
    path('bookings/', provider_bookings, name='bookings'),
    path('bookings/<int:booking_id>/confirm/', confirm_booking, name='confirm_booking'),
    path('bookings/<int:booking_id>/complete/', complete_booking, name='complete_booking'),
    path('bookings/<int:booking_id>/cancel/', cancel_booking, name='cancel_booking'),
    path('bookings/<int:booking_id>/', booking_detail, name='booking_detail'),
    path('earnings/', provider_earnings, name='earnings'),
    path('messages/', provider_messages_page, name='messages'),
    path('calendar/', provider_calendar, name='calendar'),
    path('calendar/set-availability/', set_availability, name='set_availability'),
    path('calendar/add-leave/', add_leave, name='add_leave'),
    path('profile/', provider_profile_page, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/change-password/', change_password, name='change_password'),
    path('reviews/', provider_reviews, name='reviews'),
]
