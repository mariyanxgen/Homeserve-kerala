from django.contrib import admin
from django.utils.html import format_html
from .models import (
    ServiceCategory, ServiceProvider, Service, 
    Booking, Review, ProviderPortfolio, ServiceRequest,
    # Payment & Wallet
    Wallet, Payment, Transaction,
    # Messaging
    Message,
    # Provider Analytics
    ProviderEarnings, ProviderStats,
    # Promotions
    Coupon, ServicePackage, Referral, LoyaltyPoints,
    # Customer Features
    FavoriteProvider, CustomerAddress, Notification,
    # Verification
    ProviderDocument, ProviderInsurance,
    # Advanced Booking
    RecurringBooking, BookingExtension,
    # Scheduling
    ProviderAvailability, ProviderLeave
)


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'is_active', 'total_services', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']
    
    def total_services(self, obj):
        return obj.services.count()
    total_services.short_description = 'Total Services'


@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = [
        'business_name', 'user', 'city', 'verification_badge', 
        'average_rating', 'total_bookings', 'is_available', 'created_at'
    ]
    list_filter = ['verification_status', 'is_available', 'city', 'state', 'created_at']
    search_fields = ['business_name', 'user__username', 'email', 'contact_number', 'city']
    readonly_fields = ['average_rating', 'total_reviews', 'total_bookings', 'created_at', 'updated_at']
    ordering = ['-average_rating', '-total_bookings']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'business_name', 'bio', 'profile_image')
        }),
        ('Contact Details', {
            'fields': ('email', 'contact_number', 'alternate_contact')
        }),
        ('Location', {
            'fields': ('address', 'city', 'state', 'pincode')
        }),
        ('Business Details', {
            'fields': ('experience_years', 'is_available', 'available_from', 'available_to')
        }),
        ('Verification', {
            'fields': ('verification_status', 'verification_document', 'verified_at')
        }),
        ('Statistics', {
            'fields': ('average_rating', 'total_reviews', 'total_bookings'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def verification_badge(self, obj):
        colors = {
            'verified': 'green',
            'pending': 'orange',
            'rejected': 'red'
        }
        color = colors.get(obj.verification_status, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold;">●</span> {}',
            color, obj.get_verification_status_display()
        )
    verification_badge.short_description = 'Verification Status'
    
    actions = ['verify_providers', 'reject_providers']
    
    def verify_providers(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(verification_status='verified', verified_at=timezone.now())
        self.message_user(request, f'{updated} provider(s) verified successfully.')
    verify_providers.short_description = 'Verify selected providers'
    
    def reject_providers(self, request, queryset):
        updated = queryset.update(verification_status='rejected')
        self.message_user(request, f'{updated} provider(s) rejected.')
    reject_providers.short_description = 'Reject selected providers'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'provider', 'category', 'price', 'pricing_type', 
        'approval_badge', 'duration_minutes', 'is_active', 'is_emergency_available', 'created_at'
    ]
    list_filter = ['approval_status', 'category', 'pricing_type', 'is_active', 'is_emergency_available', 'created_at']
    search_fields = ['title', 'description', 'provider__business_name']
    ordering = ['-created_at']
    actions = ['approve_services', 'reject_services']
    
    fieldsets = (
        ('Service Information', {
            'fields': ('provider', 'category', 'title', 'description', 'service_image')
        }),
        ('Pricing', {
            'fields': ('pricing_type', 'price', 'duration_minutes')
        }),
        ('Approval', {
            'fields': ('approval_status', 'rejection_reason'),
            'description': 'Approve or reject service submissions'
        }),
        ('Availability', {
            'fields': ('is_active', 'is_emergency_available')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def approval_badge(self, obj):
        colors = {
            'pending': '#fbbf24',
            'approved': '#10b981',
            'rejected': '#ef4444'
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 5px 12px; border-radius: 4px; font-weight: 600;">{}</span>',
            colors.get(obj.approval_status, '#6b7280'),
            obj.get_approval_status_display()
        )
    approval_badge.short_description = 'Approval Status'
    
    def approve_services(self, request, queryset):
        updated = queryset.update(approval_status='approved')
        self.message_user(request, f'{updated} service(s) approved successfully.')
    approve_services.short_description = 'Approve selected services'
    
    def reject_services(self, request, queryset):
        updated = queryset.update(approval_status='rejected')
        self.message_user(request, f'{updated} service(s) rejected.')
    reject_services.short_description = 'Reject selected services'


class BookingInline(admin.TabularInline):
    model = Booking
    extra = 0
    fields = ['customer', 'service', 'booking_date', 'booking_time', 'status', 'total_amount']
    readonly_fields = ['customer', 'service', 'total_amount']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'customer_name', 'service', 'provider', 'booking_date', 
        'booking_time', 'status_badge', 'total_amount', 'is_emergency', 'created_at'
    ]
    list_filter = ['status', 'booking_date', 'is_emergency', 'created_at']
    search_fields = [
        'customer_name', 'customer_email', 'customer_phone',
        'service__title', 'provider__business_name', 'customer_address'
    ]
    ordering = ['-created_at']
    date_hierarchy = 'booking_date'
    
    readonly_fields = ['created_at', 'updated_at', 'confirmed_at', 'completed_at']
    
    fieldsets = (
        ('Booking Details', {
            'fields': ('user', 'service', 'provider', 'status')
        }),
        ('Customer Information', {
            'fields': ('customer_name', 'customer_email', 'customer_phone', 'customer_address')
        }),
        ('Schedule', {
            'fields': ('booking_date', 'booking_time', 'is_emergency')
        }),
        ('Additional Information', {
            'fields': ('notes', 'total_amount')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'pending': '#FFA500',
            'confirmed': '#4169E1',
            'in_progress': '#9370DB',
            'completed': '#32CD32',
            'cancelled': '#DC143C',
        }
        color = colors.get(obj.status, '#000000')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    actions = ['confirm_bookings', 'mark_completed', 'cancel_bookings']
    
    def confirm_bookings(self, request, queryset):
        updated = queryset.update(status='confirmed', confirmed_at=timezone.now())
        self.message_user(request, f'{updated} booking(s) confirmed.')
    confirm_bookings.short_description = 'Confirm selected bookings'
    
    def mark_completed(self, request, queryset):
        updated = queryset.update(status='completed', completed_at=timezone.now())
        self.message_user(request, f'{updated} booking(s) marked as completed.')
    mark_completed.short_description = 'Mark as completed'
    
    def cancel_bookings(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} booking(s) cancelled.')
    cancel_bookings.short_description = 'Cancel selected bookings'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'customer', 'provider', 'rating_stars', 'booking', 
        'has_images', 'has_response', 'created_at'
    ]
    list_filter = ['rating', 'created_at']
    search_fields = ['customer__username', 'provider__business_name', 'review_text']
    ordering = ['-created_at']
    
    readonly_fields = ['booking', 'provider', 'customer', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Review Details', {
            'fields': ('booking', 'provider', 'customer', 'rating')
        }),
        ('Review Content', {
            'fields': ('review_text',)
        }),
        ('Images', {
            'fields': ('image1', 'image2', 'image3')
        }),
        ('Provider Response', {
            'fields': ('provider_response', 'responded_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def rating_stars(self, obj):
        stars = '⭐' * obj.rating
        return format_html('<span style="font-size: 16px;">{}</span>', stars)
    rating_stars.short_description = 'Rating'
    
    def has_images(self, obj):
        count = sum([1 for img in [obj.image1, obj.image2, obj.image3] if img])
        if count > 0:
            return format_html('<span style="color: green;">✓ {} image(s)</span>', count)
        return format_html('<span style="color: gray;">No images</span>')
    has_images.short_description = 'Images'
    
    def has_response(self, obj):
        if obj.provider_response:
            return format_html('<span style="color: green;">✓ Responded</span>')
        return format_html('<span style="color: orange;">● Pending</span>')
    has_response.short_description = 'Provider Response'


@admin.register(ProviderPortfolio)
class ProviderPortfolioAdmin(admin.ModelAdmin):
    list_display = ['provider', 'title', 'service_category', 'created_at']
    list_filter = ['service_category', 'created_at']
    search_fields = ['provider__business_name', 'title', 'description']
    ordering = ['-created_at']


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'customer', 'title', 'category', 'urgency_badge', 
        'status_badge', 'assigned_provider', 'created_at'
    ]
    list_filter = ['status', 'urgency', 'category', 'created_at']
    search_fields = ['customer__username', 'title', 'description', 'city']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Request Details', {
            'fields': ('customer', 'category', 'title', 'description', 'urgency')
        }),
        ('Location', {
            'fields': ('address', 'city', 'pincode')
        }),
        ('Budget', {
            'fields': ('budget_min', 'budget_max')
        }),
        ('Status', {
            'fields': ('status', 'assigned_provider')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def urgency_badge(self, obj):
        colors = {
            'low': '#90EE90',
            'medium': '#FFD700',
            'high': '#FFA500',
            'emergency': '#FF0000'
        }
        color = colors.get(obj.urgency, '#808080')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color, obj.get_urgency_display().upper()
        )
    urgency_badge.short_description = 'Urgency'
    
    def status_badge(self, obj):
        colors = {
            'open': '#4169E1',
            'assigned': '#32CD32',
            'closed': '#696969'
        }
        color = colors.get(obj.status, '#000000')
        return format_html(
            '<span style="color: {}; font-weight: bold;">● {}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'


# ====================== PAYMENT & WALLET ADMIN ======================

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance_display', 'currency', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    
    def balance_display(self, obj):
        color = 'green' if obj.balance > 0 else 'red'
        return format_html('<span style="color: {}; font-weight: bold;">₹{}</span>', color, obj.balance)
    balance_display.short_description = 'Balance'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'booking', 'user', 'amount_display', 'payment_method', 'status_badge', 'paid_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['transaction_id', 'user__username', 'booking__id']
    readonly_fields = ['created_at', 'updated_at', 'transaction_id']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Payment Details', {
            'fields': ('booking', 'user', 'amount', 'payment_method', 'status')
        }),
        ('Gateway Details', {
            'fields': ('transaction_id', 'gateway_order_id', 'gateway_payment_id', 'gateway_signature')
        }),
        ('Commission', {
            'fields': ('platform_commission', 'provider_amount')
        }),
        ('Refund', {
            'fields': ('refund_amount', 'refund_reason', 'refunded_at'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'paid_at'),
            'classes': ('collapse',)
        }),
    )
    
    def amount_display(self, obj):
        return format_html('<span style="font-weight: bold;">₹{}</span>', obj.amount)
    amount_display.short_description = 'Amount'
    
    def status_badge(self, obj):
        colors = {'pending': 'orange', 'processing': 'blue', 'completed': 'green', 'failed': 'red', 'refunded': 'purple'}
        color = colors.get(obj.status, 'gray')
        return format_html('<span style="color: {}; font-weight: bold;">● {}</span>', color, obj.get_status_display())
    status_badge.short_description = 'Status'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['wallet', 'amount_display', 'transaction_type', 'description', 'balance_after', 'created_at']
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['wallet__user__username', 'description', 'reference_id']
    ordering = ['-created_at']
    
    def amount_display(self, obj):
        color = 'green' if obj.transaction_type == 'credit' else 'red'
        return format_html('<span style="color: {}; font-weight: bold;">₹{}</span>', color, obj.amount)
    amount_display.short_description = 'Amount'


# ====================== MESSAGING ADMIN ======================

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'message_preview', 'booking', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['sender__username', 'receiver__username', 'message_text']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    def message_preview(self, obj):
        return obj.message_text[:50] + '...' if len(obj.message_text) > 50 else obj.message_text
    message_preview.short_description = 'Message'


# ====================== PROVIDER ANALYTICS ADMIN ======================

@admin.register(ProviderEarnings)
class ProviderEarningsAdmin(admin.ModelAdmin):
    list_display = ['provider', 'booking', 'gross_amount', 'commission_amount', 'net_amount', 'payout_status', 'created_at']
    list_filter = ['payout_status', 'created_at']
    search_fields = ['provider__business_name', 'booking__id']
    readonly_fields = ['created_at']
    ordering = ['-created_at']


@admin.register(ProviderStats)
class ProviderStatsAdmin(admin.ModelAdmin):
    list_display = ['provider', 'date', 'bookings_received', 'bookings_completed', 'revenue', 'average_rating_day']
    list_filter = ['date', 'provider']
    search_fields = ['provider__business_name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-date']
    date_hierarchy = 'date'


# ====================== PROMOTIONS ADMIN ======================

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'coupon_type', 'discount_value', 'usage_stats', 'validity_badge', 'is_active']
    list_filter = ['coupon_type', 'is_active', 'valid_from', 'valid_to']
    search_fields = ['code', 'description']
    filter_horizontal = ['applicable_categories', 'applicable_services']
    readonly_fields = ['used_count', 'created_at']
    
    fieldsets = (
        ('Coupon Details', {
            'fields': ('code', 'description', 'coupon_type', 'is_active')
        }),
        ('Discount', {
            'fields': ('discount_value', 'max_discount', 'min_order_value')
        }),
        ('Usage Limits', {
            'fields': ('usage_limit', 'used_count', 'per_user_limit')
        }),
        ('Validity', {
            'fields': ('valid_from', 'valid_to')
        }),
        ('Applicability', {
            'fields': ('applicable_categories', 'applicable_services'),
            'classes': ('collapse',)
        }),
    )
    
    def usage_stats(self, obj):
        if obj.usage_limit:
            percentage = (obj.used_count / obj.usage_limit) * 100
            return format_html('{} / {} ({}%)', obj.used_count, obj.usage_limit, int(percentage))
        return f'{obj.used_count} / ∞'
    usage_stats.short_description = 'Usage'
    
    def validity_badge(self, obj):
        if obj.is_valid():
            return format_html('<span style="color: green;">✓ Valid</span>')
        return format_html('<span style="color: red;">✗ Expired</span>')
    validity_badge.short_description = 'Validity'


@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display = ['title', 'provider', 'package_price', 'savings', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'provider__business_name']
    filter_horizontal = ['services']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ['referrer', 'referred', 'referral_code', 'is_completed', 'rewards_credited', 'created_at']
    list_filter = ['is_completed', 'rewards_credited', 'created_at']
    search_fields = ['referrer__username', 'referred__username', 'referral_code']
    readonly_fields = ['created_at', 'completed_at']
    ordering = ['-created_at']


@admin.register(LoyaltyPoints)
class LoyaltyPointsAdmin(admin.ModelAdmin):
    list_display = ['user', 'points', 'tier_badge', 'total_earned', 'total_redeemed', 'updated_at']
    list_filter = ['tier', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'updated_at']
    
    def tier_badge(self, obj):
        colors = {'bronze': '#CD7F32', 'silver': '#C0C0C0', 'gold': '#FFD700', 'platinum': '#E5E4E2'}
        color = colors.get(obj.tier, 'gray')
        return format_html('<span style="color: {}; font-weight: bold;">★ {}</span>', color, obj.tier.upper())
    tier_badge.short_description = 'Tier'


# ====================== CUSTOMER FEATURES ADMIN ======================

@admin.register(FavoriteProvider)
class FavoriteProviderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'provider', 'created_at']
    list_filter = ['created_at']
    search_fields = ['customer__username', 'provider__business_name']
    ordering = ['-created_at']


@admin.register(CustomerAddress)
class CustomerAddressAdmin(admin.ModelAdmin):
    list_display = ['customer', 'label', 'address_type', 'city', 'is_default', 'created_at']
    list_filter = ['address_type', 'is_default', 'city', 'state']
    search_fields = ['customer__username', 'label', 'city', 'pincode']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    actions = ['mark_as_read']
    
    def mark_as_read(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(is_read=True, read_at=timezone.now())
        self.message_user(request, f'{updated} notification(s) marked as read.')
    mark_as_read.short_description = 'Mark selected as read'


# ====================== VERIFICATION ADMIN ======================

@admin.register(ProviderDocument)
class ProviderDocumentAdmin(admin.ModelAdmin):
    list_display = ['provider', 'document_type', 'document_number', 'verification_badge', 'expires_at', 'created_at']
    list_filter = ['verification_status', 'document_type', 'created_at']
    search_fields = ['provider__business_name', 'document_number']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Document Details', {
            'fields': ('provider', 'document_type', 'document_file', 'document_number', 'expires_at')
        }),
        ('Verification', {
            'fields': ('verification_status', 'verified_by', 'verification_notes', 'verified_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def verification_badge(self, obj):
        colors = {'pending': 'orange', 'verified': 'green', 'rejected': 'red'}
        color = colors.get(obj.verification_status, 'gray')
        return format_html('<span style="color: {}; font-weight: bold;">● {}</span>', color, obj.get_verification_status_display())
    verification_badge.short_description = 'Status'
    
    actions = ['verify_documents', 'reject_documents']
    
    def verify_documents(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(verification_status='verified', verified_by=request.user, verified_at=timezone.now())
        self.message_user(request, f'{updated} document(s) verified successfully.')
    verify_documents.short_description = 'Verify selected documents'
    
    def reject_documents(self, request, queryset):
        updated = queryset.update(verification_status='rejected', verified_by=request.user)
        self.message_user(request, f'{updated} document(s) rejected.')
    reject_documents.short_description = 'Reject selected documents'


@admin.register(ProviderInsurance)
class ProviderInsuranceAdmin(admin.ModelAdmin):
    list_display = ['provider', 'insurance_company', 'policy_number', 'coverage_amount', 'valid_from', 'valid_to', 'is_active']
    list_filter = ['is_active', 'insurance_company', 'valid_from', 'valid_to']
    search_fields = ['provider__business_name', 'policy_number', 'insurance_company']
    readonly_fields = ['created_at', 'updated_at']


# ====================== ADVANCED BOOKING ADMIN ======================

@admin.register(RecurringBooking)
class RecurringBookingAdmin(admin.ModelAdmin):
    list_display = ['customer', 'service', 'frequency', 'next_booking_date', 'is_active', 'created_at']
    list_filter = ['frequency', 'is_active', 'created_at']
    search_fields = ['customer__username', 'service__title', 'provider__business_name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(BookingExtension)
class BookingExtensionAdmin(admin.ModelAdmin):
    list_display = ['booking', 'has_photos', 'has_signatures', 'warranty_period_days', 'created_at']
    list_filter = ['created_at']
    search_fields = ['booking__id', 'booking__customer_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Service Photos', {
            'fields': ('before_photo1', 'before_photo2', 'after_photo1', 'after_photo2')
        }),
        ('Signatures', {
            'fields': ('customer_signature', 'provider_signature')
        }),
        ('Timing', {
            'fields': ('estimated_arrival_time', 'actual_arrival_time', 'service_started_at', 'service_ended_at')
        }),
        ('Work Details', {
            'fields': ('materials_used', 'work_description')
        }),
        ('Warranty', {
            'fields': ('warranty_period_days', 'warranty_terms')
        }),
    )
    
    def has_photos(self, obj):
        photos = [obj.before_photo1, obj.before_photo2, obj.after_photo1, obj.after_photo2]
        count = sum(1 for p in photos if p)
        return format_html('{}/ 4 photos', count)
    has_photos.short_description = 'Photos'
    
    def has_signatures(self, obj):
        sigs = [obj.customer_signature, obj.provider_signature]
        count = sum(1 for s in sigs if s)
        return format_html('{} / 2', count)
    has_signatures.short_description = 'Signatures'


# ====================== SCHEDULING ADMIN ======================

@admin.register(ProviderAvailability)
class ProviderAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['provider', 'weekday_display', 'is_available', 'start_time', 'end_time', 'break_time']
    list_filter = ['is_available', 'weekday']
    search_fields = ['provider__business_name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['provider', 'weekday']
    
    def weekday_display(self, obj):
        return obj.get_weekday_display()
    weekday_display.short_description = 'Day'
    
    def break_time(self, obj):
        if obj.break_start and obj.break_end:
            return f'{obj.break_start} - {obj.break_end}'
        return '-'
    break_time.short_description = 'Break'


@admin.register(ProviderLeave)
class ProviderLeaveAdmin(admin.ModelAdmin):
    list_display = ['provider', 'leave_type', 'start_date', 'end_date', 'is_approved', 'created_at']
    list_filter = ['leave_type', 'is_approved', 'start_date']
    search_fields = ['provider__business_name', 'reason']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-start_date']
    date_hierarchy = 'start_date'

