"""
Django views for HomeServe frontend pages
Server-side rendering without JavaScript
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from services.models import ServiceCategory, Service, ServiceProvider, Booking, Payment
from services.forms import BookingForm
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home_view(request):
    """Homepage with service categories"""
    # Redirect logged-in providers to their dashboard
    if request.user.is_authenticated:
        try:
            provider = ServiceProvider.objects.get(user=request.user)
            return redirect('/provider/')
        except ServiceProvider.DoesNotExist:
            # Not a provider, show regular home page
            pass
    
    categories = ServiceCategory.objects.filter(is_active=True).prefetch_related('services')
    
    # Add service count to each category
    for category in categories:
        category.service_count = category.services.filter(is_active=True).count()
    
    context = {
        'categories': categories,
        'total_services': Service.objects.filter(is_active=True, approval_status='approved').count(),
        'total_providers': ServiceProvider.objects.filter(verification_status='verified').count(),
    }
    return render(request, 'frontend/index.html', context)


def services_view(request):
    """Services listing page with filters"""
    # Redirect logged-in providers to their dashboard
    if request.user.is_authenticated:
        try:
            provider = ServiceProvider.objects.get(user=request.user)
            return redirect('/provider/services/')
        except ServiceProvider.DoesNotExist:
            pass
    
    # Get filter parameters
    category_id = request.GET.get('category')
    category_name = request.GET.get('category_name')
    district = request.GET.get('district')
    search_query = request.GET.get('q')
    price_range = request.GET.get('price')
    pricing_type = request.GET.get('pricing_type')
    emergency_only = request.GET.get('emergency')
    
    # Base queryset
    services = Service.objects.filter(is_active=True, approval_status='approved').select_related('category', 'provider')
    
    # Apply filters
    if category_id:
        services = services.filter(category__id=category_id)
    
    if district:
        services = services.filter(provider__city__icontains=district)
    
    if search_query and search_query != 'None':
        services = services.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(provider__business_name__icontains=search_query)
        )
    
    if price_range:
        if price_range == '5000+':
            services = services.filter(price__gte=5000)
        else:
            min_price, max_price = price_range.split('-')
            services = services.filter(price__gte=min_price, price__lte=max_price)
    
    if pricing_type:
        services = services.filter(pricing_type=pricing_type)
    
    if emergency_only:
        services = services.filter(is_emergency_available=True)
    
    # Pagination
    paginator = Paginator(services, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all categories for filter dropdown
    categories = ServiceCategory.objects.filter(is_active=True)
    
    # Get all unique districts from active service providers
    districts = ServiceProvider.objects.filter(verification_status='verified').values_list('city', flat=True).distinct().order_by('city')
    
    # Selected category for page title
    selected_category = None
    if category_id:
        selected_category = ServiceCategory.objects.filter(id=category_id).first()
    elif category_name:
        selected_category = ServiceCategory.objects.filter(name=category_name).first()
    
    context = {
        'services': page_obj,
        'categories': categories,
        'districts': districts,
        'selected_category': selected_category,
        'filters': {
            'category': category_id or '',
            'district': district or '',
            'search': search_query or '',
            'price': price_range or '',
            'pricing_type': pricing_type or '',
            'emergency': emergency_only or '',
        }
    }
    return render(request, 'frontend/services.html', context)


def service_detail_view(request, service_id):
    """Service detail page"""
    # Redirect logged-in providers to their dashboard
    if request.user.is_authenticated:
        try:
            provider = ServiceProvider.objects.get(user=request.user)
            return redirect('/provider/services/')
        except ServiceProvider.DoesNotExist:
            pass
    
    service = get_object_or_404(
        Service.objects.select_related('category', 'provider'),
        id=service_id,
        is_active=True
    )
    
    context = {
        'service': service,
    }
    return render(request, 'frontend/service_detail.html', context)


def book_service_view(request, service_id):
    """Booking page for a service - accessible to both logged-in and guest users"""
    # Redirect logged-in providers to their dashboard
    if request.user.is_authenticated:
        try:
            provider = ServiceProvider.objects.get(user=request.user)
            messages.info(request, 'Providers cannot book services. Please use a customer account.')
            return redirect('/provider/')
        except ServiceProvider.DoesNotExist:
            pass
    
    service = get_object_or_404(
        Service.objects.select_related('category', 'provider'),
        id=service_id,
        is_active=True
    )
    
    if request.method == 'POST':
        form = BookingForm(request.POST, user=request.user)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.service = service
            booking.provider = service.provider
            booking.total_amount = service.price
            
            # Link to user if logged in
            if request.user.is_authenticated:
                booking.user = request.user
            
            booking.save()
            
            # Create payment record automatically
            from decimal import Decimal
            from django.utils import timezone
            commission_pct = Decimal('15.00')
            provider_amt = booking.total_amount * (Decimal('100.00') - commission_pct) / Decimal('100.00')
            
            Payment.objects.create(
                booking=booking,
                user=booking.user,
                amount=booking.total_amount,
                payment_method='online',  # Default, can be updated later
                status='completed',  # Auto-complete for now, can add payment gateway later
                transaction_id=f'TXN{booking.id}',
                platform_commission=commission_pct,
                provider_amount=provider_amt,
                paid_at=timezone.now()
            )
            
            messages.success(request, 'Your booking request has been submitted successfully!')
            return redirect('booking_confirmation', booking_id=booking.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookingForm(user=request.user)
    
    context = {
        'service': service,
        'form': form,
    }
    return render(request, 'frontend/book_service.html', context)


def booking_confirmation_view(request, booking_id):
    """Booking confirmation page"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Only allow viewing own bookings (for logged-in users) or by booking ID (for guests)
    if booking.user and booking.user != request.user:
        messages.error(request, 'You do not have permission to view this booking.')
        return redirect('home')
    
    context = {
        'booking': booking,
    }
    return render(request, 'frontend/booking_confirmation.html', context)


def how_it_works_view(request):
    """How It Works page"""
    # Redirect logged-in providers to their dashboard
    if request.user.is_authenticated:
        try:
            provider = ServiceProvider.objects.get(user=request.user)
            return redirect('/provider/')
        except ServiceProvider.DoesNotExist:
            pass
    
    return render(request, 'frontend/how_it_works.html')


def provider_detail_view(request, provider_id):
    """Provider detail page"""
    # Redirect logged-in providers to their own profile
    if request.user.is_authenticated:
        try:
            own_provider = ServiceProvider.objects.get(user=request.user)
            if own_provider.id == provider_id:
                return redirect('/provider/profile/')
            else:
                messages.info(request, 'You are viewing this as a provider. Switch to customer view to see other providers.')
                return redirect('/provider/')
        except ServiceProvider.DoesNotExist:
            pass
    
    provider = get_object_or_404(ServiceProvider, id=provider_id)
    services = Service.objects.filter(provider=provider, is_active=True, approval_status='approved')
    
    context = {
        'provider': provider,
        'services': services,
    }
    return render(request, 'frontend/provider_detail.html', context)


@login_required
def dashboard_view(request):
    """Route users to the appropriate dashboard based on their role"""
    if hasattr(request.user, 'provider_profile'):
        return redirect('/provider/')  # Redirect to provider portal
    return redirect('customer_dashboard')


@login_required
def provider_dashboard_view(request):
    """Enhanced dashboard for service providers with all features"""
    if not hasattr(request.user, 'provider_profile'):
        messages.info(request, 'Create a provider profile to access provider dashboard.')
        return redirect('provider_onboarding')

    provider = request.user.provider_profile
    
    # Import all new models
    from services.models import (
        ProviderEarnings, ProviderStats, Message, Notification,
        ProviderDocument, ProviderInsurance, ProviderAvailability
    )
    from datetime import date, timedelta
    from django.db.models import Sum, Avg, Count

    # Booking metrics
    pending_count = Booking.objects.filter(provider=provider, status='pending').count()
    confirmed_count = Booking.objects.filter(provider=provider, status='confirmed').count()
    completed_count = Booking.objects.filter(provider=provider, status='completed').count()
    total_bookings = Booking.objects.filter(provider=provider).count()

    # Earnings metrics
    total_earnings = ProviderEarnings.objects.filter(
        provider=provider, 
        payout_status='paid'
    ).aggregate(total=Sum('net_amount'))['total'] or 0
    
    pending_earnings = ProviderEarnings.objects.filter(
        provider=provider, 
        payout_status='pending'
    ).aggregate(total=Sum('net_amount'))['total'] or 0
    
    # This month's earnings
    this_month_start = date.today().replace(day=1)
    monthly_earnings = ProviderEarnings.objects.filter(
        provider=provider,
        created_at__gte=this_month_start
    ).aggregate(total=Sum('net_amount'))['total'] or 0

    # Statistics - Last 30 days
    thirty_days_ago = date.today() - timedelta(days=30)
    recent_stats = ProviderStats.objects.filter(
        provider=provider,
        date__gte=thirty_days_ago
    ).aggregate(
        total_bookings=Sum('bookings_received'),
        completed=Sum('bookings_completed'),
        revenue=Sum('revenue'),
        avg_rating=Avg('average_rating_day')
    )

    # Unread messages count
    unread_messages = Message.objects.filter(
        receiver=request.user,
        is_read=False
    ).count()

    # Unread notifications
    unread_notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    # Verification status
    verified_docs = ProviderDocument.objects.filter(
        provider=provider,
        verification_status='verified'
    ).count()
    
    pending_docs = ProviderDocument.objects.filter(
        provider=provider,
        verification_status='pending'
    ).count()
    
    has_insurance = ProviderInsurance.objects.filter(
        provider=provider,
        is_active=True
    ).exists()

    # Upcoming bookings
    upcoming_bookings = (
        Booking.objects
        .filter(provider=provider, status__in=['pending', 'confirmed'])
        .order_by('booking_date', 'booking_time')[:10]
    )
    
    # Recent bookings
    recent_bookings = (
        Booking.objects
        .filter(provider=provider)
        .order_by('-created_at')[:5]
    )
    
    # My services
    my_services_query = Service.objects.filter(provider=provider).order_by('-created_at')
    active_services = my_services_query.filter(is_active=True).count()
    my_services = my_services_query[:10]
    
    # Recent reviews
    recent_reviews = provider.reviews.order_by('-created_at')[:5]

    # Recent messages
    recent_messages = Message.objects.filter(
        receiver=request.user
    ).order_by('-created_at')[:5]

    # Weekly availability
    availability = ProviderAvailability.objects.filter(
        provider=provider
    ).order_by('weekday')

    context = {
        'provider': provider,
        'metrics': {
            'pending': pending_count,
            'confirmed': confirmed_count,
            'completed': completed_count,
            'total_bookings': total_bookings,
            'active_services': active_services,
        },
        'earnings': {
            'total': total_earnings,
            'pending': pending_earnings,
            'monthly': monthly_earnings,
        },
        'stats': recent_stats,
        'verification': {
            'verified_docs': verified_docs,
            'pending_docs': pending_docs,
            'has_insurance': has_insurance,
            'status': provider.verification_status,
        },
        'unread_messages': unread_messages,
        'unread_notifications': unread_notifications,
        'upcoming_bookings': upcoming_bookings,
        'recent_bookings': recent_bookings,
        'services': my_services,
        'recent_reviews': recent_reviews,
        'recent_messages': recent_messages,
        'availability': availability,
    }
    return render(request, 'frontend/provider_dashboard.html', context)


@login_required
def customer_dashboard_view(request):
    """Enhanced dashboard for customers with all features"""
    from services.models import (
        ServiceRequest, Wallet, LoyaltyPoints, FavoriteProvider,
        CustomerAddress, Notification, Message, RecurringBooking
    )
    from django.db.models import Sum
    
    # Booking metrics
    my_bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    open_count = my_bookings.filter(status__in=['pending', 'confirmed', 'in_progress']).count()
    completed_count = my_bookings.filter(status='completed').count()
    cancelled_count = my_bookings.filter(status='cancelled').count()
    total_bookings = my_bookings.count()

    # Recent bookings
    recent_bookings = my_bookings[:10]

    # Service requests
    my_requests = ServiceRequest.objects.filter(customer=request.user).order_by('-created_at')[:10]

    # Wallet information
    wallet = Wallet.objects.filter(user=request.user).first()
    wallet_balance = wallet.balance if wallet else 0

    # Loyalty points
    loyalty = LoyaltyPoints.objects.filter(user=request.user).first()
    loyalty_points = loyalty.points if loyalty else 0
    loyalty_tier = loyalty.tier if loyalty else 'bronze'

    # Favorite providers
    favorite_providers = FavoriteProvider.objects.filter(
        customer=request.user
    ).select_related('provider')[:5]

    # Saved addresses
    saved_addresses = CustomerAddress.objects.filter(
        customer=request.user
    ).order_by('-is_default', '-created_at')[:3]

    # Unread notifications
    unread_notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    # Unread messages
    unread_messages = Message.objects.filter(
        receiver=request.user,
        is_read=False
    ).count()

    # Recent notifications
    recent_notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')[:5]

    # Recurring bookings
    recurring_bookings = RecurringBooking.objects.filter(
        customer=request.user,
        is_active=True
    )

    # Total spent
    from services.models import Payment
    total_spent = Payment.objects.filter(
        user=request.user,
        status='completed'
    ).aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'metrics': {
            'open': open_count,
            'completed': completed_count,
            'cancelled': cancelled_count,
            'total': total_bookings,
        },
        'bookings': recent_bookings,
        'requests': my_requests,
        'wallet': {
            'balance': wallet_balance,
            'object': wallet,
        },
        'loyalty': {
            'points': loyalty_points,
            'tier': loyalty_tier,
            'object': loyalty,
        },
        'favorite_providers': favorite_providers,
        'saved_addresses': saved_addresses,
        'unread_notifications': unread_notifications,
        'unread_messages': unread_messages,
        'recent_notifications': recent_notifications,
        'recurring_bookings': recurring_bookings,
        'total_spent': total_spent,
    }
    return render(request, 'frontend/customer_dashboard.html', context)


@login_required
def provider_confirm_booking_view(request, booking_id):
    """Provider action: confirm a pending booking"""
    booking = get_object_or_404(Booking, id=booking_id)
    if not hasattr(request.user, 'provider_profile') or booking.provider.user != request.user:
        messages.error(request, 'You are not authorized to confirm this booking.')
        return redirect('provider_dashboard')

    if request.method == 'POST' and booking.status == 'pending':
        booking.status = 'confirmed'
        booking.confirmed_at = timezone.now()
        booking.save()
        messages.success(request, f'Booking #{booking.id} confirmed.')
    return redirect('provider_dashboard')


@login_required
def provider_complete_booking_view(request, booking_id):
    """Provider action: mark booking as completed"""
    booking = get_object_or_404(Booking, id=booking_id)
    if not hasattr(request.user, 'provider_profile') or booking.provider.user != request.user:
        messages.error(request, 'You are not authorized to complete this booking.')
        return redirect('provider_dashboard')

    if request.method == 'POST' and booking.status in ['confirmed', 'in_progress']:
        booking.status = 'completed'
        booking.completed_at = timezone.now()
        booking.save()
        # update provider stats
        provider = request.user.provider_profile
        provider.total_bookings = Booking.objects.filter(provider=provider, status='completed').count()
        provider.save()
        messages.success(request, f'Booking #{booking.id} marked as completed.')
    return redirect('provider_dashboard')


@login_required
def customer_cancel_booking_view(request, booking_id):
    """Customer action: cancel a booking if pending/confirmed"""
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.user != request.user:
        messages.error(request, 'You are not authorized to cancel this booking.')
        return redirect('customer_dashboard')

    if request.method == 'POST' and booking.status in ['pending', 'confirmed']:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, f'Booking #{booking.id} cancelled.')
    return redirect('customer_dashboard')
