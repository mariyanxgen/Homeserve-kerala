"""
Provider-specific views for the provider portal
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Avg, Count, Q
from django.utils import timezone
from datetime import date, timedelta
from services.models import (
    ServiceProvider, Service, Booking, Review, 
    ProviderEarnings, ProviderStats, Message, Notification,
    ProviderAvailability, ProviderLeave, ServiceCategory, Payment, BookingExtension
)


def provider_required(view_func):
    """Decorator to ensure user has a provider profile"""
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'provider_profile'):
            messages.error(request, 'You need a provider account to access this page.')
            return redirect('provider_onboarding')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@provider_required
def provider_home(request):
    """Provider portal home page"""
    provider = request.user.provider_profile
    
    # Today's stats
    today = date.today()
    today_bookings = Booking.objects.filter(
        provider=provider,
        booking_date=today
    ).order_by('booking_time')
    
    # Recent pending bookings (need attention)
    recent_pending = Booking.objects.filter(
        provider=provider,
        status='pending'
    ).order_by('-created_at')[:5]
    
    # Pending actions
    pending_bookings = Booking.objects.filter(
        provider=provider,
        status='pending'
    ).count()
    
    unread_messages = Message.objects.filter(
        receiver=request.user,
        is_read=False
    ).count()
    
    # Quick stats
    this_week_start = today - timedelta(days=today.weekday())
    this_week_earnings = ProviderEarnings.objects.filter(
        provider=provider,
        created_at__gte=this_week_start
    ).aggregate(total=Sum('net_amount'))['total'] or 0
    
    this_week_bookings = Booking.objects.filter(
        provider=provider,
        created_at__gte=this_week_start
    ).count()
    
    context = {
        'provider': provider,
        'today_bookings': today_bookings,
        'recent_pending': recent_pending,
        'pending_bookings': pending_bookings,
        'unread_messages': unread_messages,
        'this_week_earnings': this_week_earnings,
        'this_week_bookings': this_week_bookings,
    }
    return render(request, 'provider/home.html', context)


@login_required
@provider_required
def provider_services(request):
    """Manage provider services"""
    provider = request.user.provider_profile
    
    services = Service.objects.filter(provider=provider).order_by('-created_at')
    categories = ServiceCategory.objects.filter(is_active=True)
    
    # Stats
    active_count = services.filter(is_active=True).count()
    inactive_count = services.filter(is_active=False).count()
    total_bookings = Booking.objects.filter(service__provider=provider).count()
    avg_price = services.aggregate(Avg('price'))['price__avg'] or 0
    
    context = {
        'provider': provider,
        'services': services,
        'categories': categories,
        'active_count': active_count,
        'inactive_count': inactive_count,
        'total_bookings': total_bookings,
        'avg_price': avg_price,
    }
    return render(request, 'provider/services.html', context)


@login_required
@provider_required
def add_service(request):
    """Add a new service"""
    from django.contrib import messages as django_messages
    
    provider = request.user.provider_profile
    categories = ServiceCategory.objects.filter(is_active=True)
    
    if request.method == 'POST':
        # Get form data
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        duration_minutes = request.POST.get('duration_minutes', 60)
        pricing_type = request.POST.get('pricing_type', 'fixed')
        is_emergency_available = request.POST.get('is_emergency_available') == 'on'
        service_image = request.FILES.get('service_image')
        
        # Create service
        try:
            category = ServiceCategory.objects.get(id=category_id)
            service = Service.objects.create(
                provider=provider,
                category=category,
                title=title,
                description=description,
                price=price,
                duration_minutes=duration_minutes,
                pricing_type=pricing_type,
                is_emergency_available=is_emergency_available,
                service_image=service_image,
                is_active=True,
                approval_status='pending'  # Set to pending for admin approval
            )
            django_messages.success(request, f'Service "{title}" submitted successfully! Waiting for admin approval.')
            return redirect('/provider/services/')
        except Exception as e:
            django_messages.error(request, f'Error adding service: {str(e)}')
    
    context = {
        'provider': provider,
        'categories': categories,
    }
    return render(request, 'provider/add_service.html', context)


@login_required
@provider_required
def edit_service(request, service_id):
    """Edit an existing service"""
    from django.contrib import messages as django_messages
    
    provider = request.user.provider_profile
    service = get_object_or_404(Service, id=service_id, provider=provider)
    categories = ServiceCategory.objects.filter(is_active=True)
    
    if request.method == 'POST':
        # Get form data
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        duration_minutes = request.POST.get('duration_minutes', 60)
        pricing_type = request.POST.get('pricing_type', 'fixed')
        is_emergency_available = request.POST.get('is_emergency_available') == 'on'
        service_image = request.FILES.get('service_image')
        
        # Update service
        try:
            category = ServiceCategory.objects.get(id=category_id)
            service.title = title
            service.description = description
            service.category = category
            service.price = price
            service.duration_minutes = duration_minutes
            service.pricing_type = pricing_type
            service.is_emergency_available = is_emergency_available
            if service_image:
                service.service_image = service_image
            # Reset to pending if previously rejected
            if service.approval_status == 'rejected':
                service.approval_status = 'pending'
            service.save()
            
            django_messages.success(request, f'Service "{title}" updated successfully!')
            return redirect('/provider/services/')
        except Exception as e:
            django_messages.error(request, f'Error updating service: {str(e)}')
    
    context = {
        'provider': provider,
        'service': service,
        'categories': categories,
        'is_edit': True,
    }
    return render(request, 'provider/add_service.html', context)


@login_required
@provider_required
def provider_bookings(request):
    """Manage all bookings"""
    provider = request.user.provider_profile
    
    # Filter by status
    status_filter = request.GET.get('status', 'all')
    
    bookings = Booking.objects.filter(provider=provider).order_by('-created_at')
    
    if status_filter != 'all':
        bookings = bookings.filter(status=status_filter)
    
    # Stats
    stats = {
        'all': Booking.objects.filter(provider=provider).count(),
        'pending': Booking.objects.filter(provider=provider, status='pending').count(),
        'confirmed': Booking.objects.filter(provider=provider, status='confirmed').count(),
        'in_progress': Booking.objects.filter(provider=provider, status='in_progress').count(),
        'completed': Booking.objects.filter(provider=provider, status='completed').count(),
        'cancelled': Booking.objects.filter(provider=provider, status='cancelled').count(),
    }
    
    context = {
        'provider': provider,
        'bookings': bookings,
        'stats': stats,
        'current_filter': status_filter,
    }
    return render(request, 'provider/bookings.html', context)


@login_required
@provider_required
def confirm_booking(request, booking_id):
    """Confirm a booking"""
    from django.contrib import messages as django_messages
    from django.utils import timezone
    
    provider = request.user.provider_profile
    booking = get_object_or_404(Booking, id=booking_id, provider=provider)
    
    if booking.status == 'pending':
        booking.status = 'confirmed'
        booking.confirmed_at = timezone.now()
        booking.save()
        django_messages.success(request, f'Booking #{booking.id} for {booking.customer_name} confirmed successfully!')
    else:
        django_messages.error(request, 'Booking cannot be confirmed.')
    
    return redirect('/provider/bookings/')


@login_required
@provider_required
def complete_booking(request, booking_id):
    """Mark booking as completed and create earnings record"""
    from django.contrib import messages as django_messages
    from django.utils import timezone
    from decimal import Decimal
    
    provider = request.user.provider_profile
    booking = get_object_or_404(Booking, id=booking_id, provider=provider)
    
    if booking.status in ['confirmed', 'in_progress']:
        booking.status = 'completed'
        booking.completed_at = timezone.now()
        booking.save()
        
        # Create earnings record if payment exists
        try:
            payment = Payment.objects.get(booking=booking, status='completed')
            
            # Check if earnings record doesn't already exist
            if not hasattr(booking, 'provider_earning'):
                # Calculate commission (platform takes 10%)
                commission_percentage = Decimal('10.00')
                gross_amount = payment.amount
                commission_amount = (gross_amount * commission_percentage) / Decimal('100.00')
                net_amount = gross_amount - commission_amount
                
                # Create earnings record
                ProviderEarnings.objects.create(
                    provider=provider,
                    booking=booking,
                    payment=payment,
                    gross_amount=gross_amount,
                    commission_percentage=commission_percentage,
                    commission_amount=commission_amount,
                    net_amount=net_amount,
                    payout_status='pending'
                )
                django_messages.success(request, f'Booking #{booking.id} marked as completed! Earnings of ₹{net_amount} recorded.')
            else:
                django_messages.success(request, f'Booking #{booking.id} marked as completed!')
        except Payment.DoesNotExist:
            django_messages.warning(request, f'Booking #{booking.id} marked as completed! Note: No payment record found yet.')
    else:
        django_messages.error(request, 'Booking cannot be marked as completed.')
    
    return redirect('/provider/bookings/')


@login_required
@provider_required
def cancel_booking(request, booking_id):
    """Cancel a booking"""
    from django.contrib import messages as django_messages
    
    provider = request.user.provider_profile
    booking = get_object_or_404(Booking, id=booking_id, provider=provider)
    
    if booking.status in ['pending', 'confirmed']:
        booking.status = 'cancelled'
        booking.save()
        django_messages.warning(request, 'Booking cancelled.')
    else:
        django_messages.error(request, 'Booking cannot be cancelled.')
    
    return redirect('/provider/bookings/')


@login_required
@provider_required
def booking_detail(request, booking_id):
    """View booking details"""
    provider = request.user.provider_profile
    booking = get_object_or_404(Booking, id=booking_id, provider=provider)
    
    context = {
        'provider': provider,
        'booking': booking,
    }
    return render(request, 'provider/booking_detail.html', context)


@login_required
@provider_required
def provider_earnings(request):
    """Earnings and analytics page"""
    provider = request.user.provider_profile
    
    # Date range filter
    days = int(request.GET.get('days', 30))
    start_date = date.today() - timedelta(days=days)
    
    # Earnings data
    earnings = ProviderEarnings.objects.filter(
        provider=provider,
        created_at__gte=start_date
    ).order_by('-created_at')
    
    # Summary
    total_earned = earnings.aggregate(total=Sum('net_amount'))['total'] or 0
    pending_payout = earnings.filter(payout_status='pending').aggregate(total=Sum('net_amount'))['total'] or 0
    paid_out = earnings.filter(payout_status='paid').aggregate(total=Sum('net_amount'))['total'] or 0
    
    # Stats by date
    daily_stats = ProviderStats.objects.filter(
        provider=provider,
        date__gte=start_date
    ).order_by('-date')
    
    # Calculate totals
    total_bookings = daily_stats.aggregate(total=Sum('bookings_completed'))['total'] or 0
    avg_rating = daily_stats.aggregate(avg=Avg('average_rating_day'))['avg'] or 0
    
    context = {
        'provider': provider,
        'earnings': earnings[:50],  # Recent 50
        'total_earned': total_earned,
        'pending_payout': pending_payout,
        'paid_out': paid_out,
        'daily_stats': daily_stats[:30],
        'total_bookings': total_bookings,
        'avg_rating': avg_rating,
        'days_filter': days,
    }
    return render(request, 'provider/earnings.html', context)


@login_required
@provider_required
def provider_messages_page(request):
    """Messages page"""
    provider = request.user.provider_profile
    
    # Get all conversations
    messages_list = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('-created_at')
    
    # Group by conversation
    conversations = {}
    for msg in messages_list:
        other_user = msg.receiver if msg.sender == request.user else msg.sender
        if other_user.id not in conversations:
            conversations[other_user.id] = {
                'user': other_user,
                'messages': [],
                'unread': 0,
            }
        conversations[other_user.id]['messages'].append(msg)
        if msg.receiver == request.user and not msg.is_read:
            conversations[other_user.id]['unread'] += 1
    
    context = {
        'provider': provider,
        'conversations': conversations.values(),
    }
    return render(request, 'provider/messages.html', context)


@login_required
@provider_required
def provider_calendar(request):
    """Calendar and availability management"""
    provider = request.user.provider_profile
    
    # Get weekly availability
    availability = ProviderAvailability.objects.filter(
        provider=provider
    ).order_by('weekday')
    
    # Upcoming bookings for calendar
    upcoming = Booking.objects.filter(
        provider=provider,
        booking_date__gte=date.today(),
        status__in=['pending', 'confirmed']
    ).order_by('booking_date', 'booking_time')[:30]
    
    context = {
        'provider': provider,
        'availability': availability,
        'upcoming_bookings': upcoming,
    }
    return render(request, 'provider/calendar.html', context)


@login_required
@provider_required
def provider_profile_page(request):
    """Provider profile and settings"""
    provider = request.user.provider_profile
    
    # Reviews
    reviews = Review.objects.filter(provider=provider).order_by('-created_at')[:20]
    
    # Documents
    from services.models import ProviderDocument, ProviderInsurance
    documents = ProviderDocument.objects.filter(provider=provider)
    insurance = ProviderInsurance.objects.filter(provider=provider).first()
    
    context = {
        'provider': provider,
        'reviews': reviews,
        'documents': documents,
        'insurance': insurance,
    }
    return render(request, 'provider/profile.html', context)


@login_required
@provider_required
def provider_reviews(request):
    """Reviews page"""
    provider = request.user.provider_profile
    
    reviews = Review.objects.filter(provider=provider).order_by('-created_at')
    
    # Stats
    total_reviews = reviews.count()
    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0
    
    rating_distribution = {
        5: reviews.filter(rating=5).count(),
        4: reviews.filter(rating=4).count(),
        3: reviews.filter(rating=3).count(),
        2: reviews.filter(rating=2).count(),
        1: reviews.filter(rating=1).count(),
    }
    
    context = {
        'provider': provider,
        'reviews': reviews,
        'total_reviews': total_reviews,
        'avg_rating': avg_rating,
        'rating_distribution': rating_distribution,
    }
    return render(request, 'provider/reviews.html', context)


@login_required
@provider_required
def edit_profile(request):
    """Edit provider profile"""
    from django.contrib import messages as django_messages
    
    provider = request.user.provider_profile
    
    if request.method == 'POST':
        provider.business_name = request.POST.get('business_name')
        provider.contact_number = request.POST.get('contact_number')
        provider.alternate_contact = request.POST.get('alternate_contact', '')
        provider.email = request.POST.get('email')
        provider.address = request.POST.get('address')
        provider.city = request.POST.get('city')
        provider.state = request.POST.get('state')
        provider.pincode = request.POST.get('pincode')
        provider.bio = request.POST.get('bio')
        provider.experience_years = request.POST.get('experience_years', 0)
        
        if request.FILES.get('profile_image'):
            provider.profile_image = request.FILES.get('profile_image')
        
        provider.save()
        django_messages.success(request, 'Profile updated successfully!')
        return redirect('/provider/profile/')
    
    context = {'provider': provider}
    return render(request, 'provider/edit_profile.html', context)


@login_required
@provider_required
def change_password(request):
    """Change password"""
    from django.contrib.auth import update_session_auth_hash
    from django.contrib import messages as django_messages
    
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if not request.user.check_password(old_password):
            django_messages.error(request, 'Current password is incorrect.')
        elif new_password != confirm_password:
            django_messages.error(request, 'New passwords do not match.')
        elif len(new_password) < 8:
            django_messages.error(request, 'Password must be at least 8 characters.')
        else:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            django_messages.success(request, 'Password changed successfully!')
            return redirect('/provider/profile/')
    
    context = {'provider': request.user.provider_profile}
    return render(request, 'provider/change_password.html', context)


@login_required
@provider_required
def set_availability(request):
    """Set weekly availability"""
    from django.contrib import messages as django_messages
    
    provider = request.user.provider_profile
    
    if request.method == 'POST':
        # Delete existing availability
        ProviderAvailability.objects.filter(provider=provider).delete()
        
        # Add new availability
        for day in range(7):
            if request.POST.get(f'available_{day}'):
                ProviderAvailability.objects.create(
                    provider=provider,
                    weekday=day,
                    is_available=True,
                    start_time=request.POST.get(f'start_time_{day}', '09:00'),
                    end_time=request.POST.get(f'end_time_{day}', '18:00'),
                )
        
        django_messages.success(request, 'Availability updated successfully!')
        return redirect('/provider/calendar/')
    
    availability = ProviderAvailability.objects.filter(provider=provider)
    context = {'provider': provider, 'availability': availability}
    return render(request, 'provider/set_availability.html', context)


@login_required
@provider_required
def add_leave(request):
    """Add leave/unavailable dates"""
    from django.contrib import messages as django_messages
    
    provider = request.user.provider_profile
    
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        leave_type = request.POST.get('leave_type', 'personal')
        reason = request.POST.get('reason', '')
        
        ProviderLeave.objects.create(
            provider=provider,
            start_date=start_date,
            end_date=end_date,
            leave_type=leave_type,
            reason=reason,
            is_approved=True
        )
        
        django_messages.success(request, 'Leave added successfully!')
        return redirect('/provider/calendar/')
    
    context = {'provider': provider}
    return render(request, 'provider/add_leave.html', context)
