from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse

from .models import (
    ServiceCategory, ServiceProvider, Service,
    Booking, Review, ProviderPortfolio, ServiceRequest
)
from .serializers import (
    ServiceCategorySerializer,
    ServiceProviderListSerializer, ServiceProviderDetailSerializer,
    ServiceListSerializer, ServiceDetailSerializer,
    BookingListSerializer, BookingDetailSerializer,
    ReviewListSerializer, ReviewDetailSerializer,
    ProviderPortfolioSerializer,
    ServiceRequestListSerializer, ServiceRequestDetailSerializer
)


def home(request):
    """Home page view with API stats"""
    stats = {
        'total_services': Service.objects.filter(is_active=True).count(),
        'total_providers': ServiceProvider.objects.filter(verification_status='verified').count(),
        'total_categories': ServiceCategory.objects.filter(is_active=True).count(),
        'total_bookings': Booking.objects.count(),
    }
    
    if request.headers.get('Accept') == 'application/json':
        return JsonResponse(stats)
    
    return render(request, 'home.html', {'stats': stats})


class ServiceCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Service Categories
    GET /api/categories/ - List all active categories
    POST /api/categories/ - Create new category (admin only)
    GET /api/categories/{id}/ - Get category details
    PUT/PATCH /api/categories/{id}/ - Update category
    DELETE /api/categories/{id}/ - Delete category
    """
    queryset = ServiceCategory.objects.filter(is_active=True)
    serializer_class = ServiceCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class ServiceProviderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Service Providers
    GET /api/providers/ - List all verified providers
    POST /api/providers/ - Register as provider
    GET /api/providers/{id}/ - Get provider details
    PUT/PATCH /api/providers/{id}/ - Update provider profile
    DELETE /api/providers/{id}/ - Delete provider
    
    Custom actions:
    GET /api/providers/{id}/services/ - Get all services by provider
    GET /api/providers/{id}/reviews/ - Get all reviews for provider
    GET /api/providers/search/ - Search providers by location/rating
    """
    queryset = ServiceProvider.objects.filter(verification_status='verified')
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['city', 'state', 'verification_status', 'is_available']
    search_fields = ['business_name', 'city', 'bio']
    ordering_fields = ['average_rating', 'total_bookings', 'created_at']
    ordering = ['-average_rating', '-total_bookings']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ServiceProviderListSerializer
        return ServiceProviderDetailSerializer
    
    @action(detail=True, methods=['get'])
    def services(self, request, pk=None):
        """Get all active services offered by this provider"""
        provider = self.get_object()
        services = provider.services.filter(is_active=True)
        serializer = ServiceListSerializer(services, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get all reviews for this provider"""
        provider = self.get_object()
        reviews = provider.reviews.all()
        serializer = ReviewListSerializer(reviews, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def portfolio(self, request, pk=None):
        """Get provider's portfolio"""
        provider = self.get_object()
        portfolio = provider.portfolio.all()
        serializer = ProviderPortfolioSerializer(portfolio, many=True)
        return Response(serializer.data)


class ServiceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Services
    GET /api/services/ - List all active services
    POST /api/services/ - Create new service
    GET /api/services/{id}/ - Get service details
    PUT/PATCH /api/services/{id}/ - Update service
    DELETE /api/services/{id}/ - Delete service
    
    Filters:
    - category: Filter by category ID
    - provider: Filter by provider ID
    - pricing_type: Filter by pricing type
    - is_emergency_available: Filter emergency services
    """
    queryset = Service.objects.filter(is_active=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'provider', 'pricing_type', 'is_emergency_available']
    search_fields = ['title', 'description', 'provider__business_name']
    ordering_fields = ['price', 'created_at', 'duration_minutes']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ServiceListSerializer
        return ServiceDetailSerializer
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Advanced search for services
        Query params: q (search term), city, max_price, category
        """
        queryset = self.get_queryset()
        
        # Search term
        search_term = request.query_params.get('q', None)
        if search_term:
            queryset = queryset.filter(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term) |
                Q(provider__business_name__icontains=search_term)
            )
        
        # Filter by city
        city = request.query_params.get('city', None)
        if city:
            queryset = queryset.filter(provider__city__iexact=city)
        
        # Filter by max price
        max_price = request.query_params.get('max_price', None)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Filter by category
        category = request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category_id=category)
        
        serializer = ServiceListSerializer(queryset, many=True)
        return Response(serializer.data)


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Bookings
    GET /api/bookings/ - List user's bookings
    POST /api/bookings/ - Create new booking
    GET /api/bookings/{id}/ - Get booking details
    PUT/PATCH /api/bookings/{id}/ - Update booking
    DELETE /api/bookings/{id}/ - Cancel booking
    
    Custom actions:
    POST /api/bookings/{id}/confirm/ - Confirm booking (provider)
    POST /api/bookings/{id}/complete/ - Mark as completed (provider)
    POST /api/bookings/{id}/cancel/ - Cancel booking
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_status', 'booking_date']
    ordering_fields = ['booking_date', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Return bookings for the current user"""
        user = self.request.user
        return Booking.objects.filter(Q(customer=user) | Q(provider__user=user))
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BookingListSerializer
        return BookingDetailSerializer
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirm a booking (provider only)"""
        booking = self.get_object()
        
        # Check if user is the provider
        if booking.provider.user != request.user:
            return Response(
                {'error': 'Only the service provider can confirm bookings'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        booking.confirm_booking()
        serializer = self.get_serializer(booking)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark booking as completed (provider only)"""
        booking = self.get_object()
        
        if booking.provider.user != request.user:
            return Response(
                {'error': 'Only the service provider can complete bookings'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        booking.complete_booking()
        serializer = self.get_serializer(booking)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a booking"""
        booking = self.get_object()
        
        # Only customer or provider can cancel
        if booking.customer != request.user and booking.provider.user != request.user:
            return Response(
                {'error': 'You do not have permission to cancel this booking'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        booking.status = 'cancelled'
        booking.save()
        serializer = self.get_serializer(booking)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Reviews
    GET /api/reviews/ - List all reviews
    POST /api/reviews/ - Create new review
    GET /api/reviews/{id}/ - Get review details
    PUT/PATCH /api/reviews/{id}/ - Update review
    DELETE /api/reviews/{id}/ - Delete review
    """
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['provider', 'rating']
    ordering_fields = ['rating', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ReviewListSerializer
        return ReviewDetailSerializer


class ProviderPortfolioViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Provider Portfolio
    GET /api/portfolio/ - List portfolio items
    POST /api/portfolio/ - Add portfolio item
    GET /api/portfolio/{id}/ - Get portfolio item
    PUT/PATCH /api/portfolio/{id}/ - Update portfolio item
    DELETE /api/portfolio/{id}/ - Delete portfolio item
    """
    queryset = ProviderPortfolio.objects.all()
    serializer_class = ProviderPortfolioSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['provider', 'service_category']


class ServiceRequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Service Requests
    GET /api/service-requests/ - List all open requests
    POST /api/service-requests/ - Create new request
    GET /api/service-requests/{id}/ - Get request details
    PUT/PATCH /api/service-requests/{id}/ - Update request
    DELETE /api/service-requests/{id}/ - Delete request
    
    Custom actions:
    POST /api/service-requests/{id}/assign/ - Assign to provider
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'urgency', 'category', 'city']
    ordering_fields = ['urgency', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Return open requests or user's own requests"""
        user = self.request.user
        if user.is_authenticated:
            return ServiceRequest.objects.filter(Q(status='open') | Q(customer=user))
        return ServiceRequest.objects.filter(status='open')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ServiceRequestListSerializer
        return ServiceRequestDetailSerializer
    
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """Assign request to a provider"""
        service_request = self.get_object()
        provider_id = request.data.get('provider_id')
        
        if not provider_id:
            return Response(
                {'error': 'provider_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            provider = ServiceProvider.objects.get(id=provider_id)
            service_request.assigned_provider = provider
            service_request.status = 'assigned'
            service_request.save()
            
            serializer = self.get_serializer(service_request)
            return Response(serializer.data)
        except ServiceProvider.DoesNotExist:
            return Response(
                {'error': 'Provider not found'},
                status=status.HTTP_404_NOT_FOUND
            )
