from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    ServiceCategory, ServiceProvider, Service,
    Booking, Review, ProviderPortfolio, ServiceRequest
)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class ServiceCategorySerializer(serializers.ModelSerializer):
    """Serializer for ServiceCategory"""
    total_services = serializers.SerializerMethodField()
    
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'description', 'icon', 'is_active', 'total_services', 'created_at']
    
    def get_total_services(self, obj):
        return obj.services.filter(is_active=True).count()


class ServiceProviderListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for provider lists"""
    user = UserSerializer(read_only=True)
    verification_status_display = serializers.CharField(source='get_verification_status_display', read_only=True)
    
    class Meta:
        model = ServiceProvider
        fields = [
            'id', 'user', 'business_name', 'city', 'state', 
            'verification_status', 'verification_status_display',
            'average_rating', 'total_reviews', 'total_bookings',
            'is_available', 'profile_image'
        ]


class ServiceProviderDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for provider profile"""
    user = UserSerializer(read_only=True)
    verification_status_display = serializers.CharField(source='get_verification_status_display', read_only=True)
    services_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ServiceProvider
        fields = [
            'id', 'user', 'business_name', 'contact_number', 'alternate_contact',
            'email', 'address', 'city', 'state', 'pincode',
            'experience_years', 'bio', 'profile_image',
            'verification_status', 'verification_status_display', 'verified_at',
            'average_rating', 'total_reviews', 'total_bookings',
            'is_available', 'available_from', 'available_to',
            'services_count', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'average_rating', 'total_reviews', 'total_bookings', 
            'verification_status', 'verified_at', 'created_at', 'updated_at'
        ]
    
    def get_services_count(self, obj):
        return obj.services.filter(is_active=True).count()


class ServiceListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for service lists"""
    provider = ServiceProviderListSerializer(read_only=True)
    category = ServiceCategorySerializer(read_only=True)
    pricing_type_display = serializers.CharField(source='get_pricing_type_display', read_only=True)
    
    class Meta:
        model = Service
        fields = [
            'id', 'provider', 'category', 'title', 
            'pricing_type', 'pricing_type_display', 'price',
            'duration_minutes', 'service_image', 'is_active',
            'is_emergency_available', 'created_at'
        ]


class ServiceDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for service"""
    provider = ServiceProviderDetailSerializer(read_only=True)
    category = ServiceCategorySerializer(read_only=True)
    pricing_type_display = serializers.CharField(source='get_pricing_type_display', read_only=True)
    provider_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceProvider.objects.all(),
        source='provider',
        write_only=True
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceCategory.objects.all(),
        source='category',
        write_only=True
    )
    
    class Meta:
        model = Service
        fields = [
            'id', 'provider', 'provider_id', 'category', 'category_id',
            'title', 'description', 'pricing_type', 'pricing_type_display',
            'price', 'duration_minutes', 'service_image',
            'is_active', 'is_emergency_available',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class BookingListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for booking lists"""
    customer = UserSerializer(read_only=True)
    service = ServiceListSerializer(read_only=True)
    provider = ServiceProviderListSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'customer', 'service', 'provider',
            'booking_date', 'booking_time', 'city',
            'status', 'status_display',
            'payment_status', 'payment_status_display',
            'total_amount', 'created_at'
        ]


class BookingDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for booking"""
    customer = UserSerializer(read_only=True)
    service = ServiceDetailSerializer(read_only=True)
    provider = ServiceProviderDetailSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)
    
    # Write-only fields for creation
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        source='service',
        write_only=True
    )
    
    class Meta:
        model = Booking
        fields = [
            'id', 'customer', 'service', 'service_id', 'provider',
            'booking_date', 'booking_time', 'address', 'city', 'pincode',
            'customer_notes', 'estimated_duration',
            'status', 'status_display',
            'total_amount', 'payment_status', 'payment_status_display', 'payment_method',
            'created_at', 'updated_at', 'confirmed_at', 'completed_at'
        ]
        read_only_fields = [
            'customer', 'provider', 'status', 'payment_status',
            'created_at', 'updated_at', 'confirmed_at', 'completed_at'
        ]
    
    def create(self, validated_data):
        # Automatically set provider from service
        service = validated_data.get('service')
        validated_data['provider'] = service.provider
        
        # Set customer from request context
        validated_data['customer'] = self.context['request'].user
        
        # Calculate total amount from service price
        if 'total_amount' not in validated_data:
            validated_data['total_amount'] = service.price
        
        return super().create(validated_data)


class ReviewListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for review lists"""
    customer = UserSerializer(read_only=True)
    provider = ServiceProviderListSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'customer', 'provider', 'rating',
            'review_text', 'image1', 'image2', 'image3',
            'provider_response', 'created_at'
        ]


class ReviewDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for review"""
    customer = UserSerializer(read_only=True)
    provider = ServiceProviderDetailSerializer(read_only=True)
    booking_id = serializers.PrimaryKeyRelatedField(
        queryset=Booking.objects.all(),
        source='booking',
        write_only=True
    )
    
    class Meta:
        model = Review
        fields = [
            'id', 'booking_id', 'provider', 'customer',
            'rating', 'review_text',
            'image1', 'image2', 'image3',
            'provider_response', 'responded_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['customer', 'provider', 'responded_at', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        booking = validated_data.get('booking')
        validated_data['customer'] = booking.customer
        validated_data['provider'] = booking.provider
        return super().create(validated_data)


class ProviderPortfolioSerializer(serializers.ModelSerializer):
    """Serializer for provider portfolio"""
    provider = ServiceProviderListSerializer(read_only=True)
    service_category = ServiceCategorySerializer(read_only=True)
    provider_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceProvider.objects.all(),
        source='provider',
        write_only=True
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceCategory.objects.all(),
        source='service_category',
        write_only=True,
        required=False
    )
    
    class Meta:
        model = ProviderPortfolio
        fields = [
            'id', 'provider', 'provider_id', 'title', 'description',
            'image', 'service_category', 'category_id', 'created_at'
        ]
        read_only_fields = ['created_at']


class ServiceRequestListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for service request lists"""
    customer = UserSerializer(read_only=True)
    category = ServiceCategorySerializer(read_only=True)
    assigned_provider = ServiceProviderListSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    urgency_display = serializers.CharField(source='get_urgency_display', read_only=True)
    
    class Meta:
        model = ServiceRequest
        fields = [
            'id', 'customer', 'category', 'title',
            'urgency', 'urgency_display', 'city',
            'status', 'status_display', 'assigned_provider',
            'created_at'
        ]


class ServiceRequestDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for service request"""
    customer = UserSerializer(read_only=True)
    category = ServiceCategorySerializer(read_only=True)
    assigned_provider = ServiceProviderDetailSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    urgency_display = serializers.CharField(source='get_urgency_display', read_only=True)
    
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceCategory.objects.all(),
        source='category',
        write_only=True
    )
    
    class Meta:
        model = ServiceRequest
        fields = [
            'id', 'customer', 'category', 'category_id',
            'title', 'description', 'urgency', 'urgency_display',
            'address', 'city', 'pincode',
            'budget_min', 'budget_max',
            'status', 'status_display', 'assigned_provider',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['customer', 'status', 'assigned_provider', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['customer'] = self.context['request'].user
        return super().create(validated_data)
