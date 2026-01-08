from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class ServiceCategory(models.Model):
    """Categories for home services like Plumbing, Electrical, Cleaning, etc."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True, help_text="Icon class name or emoji")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Service Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class ServiceProvider(models.Model):
    """Service providers who offer home services"""
    VERIFICATION_STATUS = [
        ('pending', 'Pending Verification'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='provider_profile')
    business_name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=15)
    alternate_contact = models.CharField(max_length=15, blank=True)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    
    # Business details
    experience_years = models.PositiveIntegerField(default=0, help_text="Years of experience")
    bio = models.TextField(help_text="Brief description about the service provider")
    profile_image = models.ImageField(upload_to='providers/', blank=True, null=True)
    
    # Verification
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS, default='pending')
    verification_document = models.FileField(upload_to='verification_docs/', blank=True, null=True)
    verified_at = models.DateTimeField(blank=True, null=True)
    
    # Ratings
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.PositiveIntegerField(default=0)
    total_bookings = models.PositiveIntegerField(default=0)
    
    # Availability
    is_available = models.BooleanField(default=True)
    available_from = models.TimeField(default='09:00')
    available_to = models.TimeField(default='18:00')
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-average_rating', '-total_bookings']

    def __str__(self):
        return f"{self.business_name} ({self.user.username})"

    def update_rating(self):
        """Recalculate average rating from all reviews"""
        reviews = self.reviews.all()
        if reviews.exists():
            self.total_reviews = reviews.count()
            self.average_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
            self.save()


class Service(models.Model):
    """Individual services offered by providers"""
    PRICING_TYPE = [
        ('fixed', 'Fixed Price'),
        ('hourly', 'Hourly Rate'),
        ('negotiable', 'Negotiable'),
    ]
    
    APPROVAL_STATUS = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='services')
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    pricing_type = models.CharField(max_length=20, choices=PRICING_TYPE, default='fixed')
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Base price")
    
    # Service details
    duration_minutes = models.PositiveIntegerField(default=60, help_text="Estimated duration in minutes")
    service_image = models.ImageField(upload_to='services/', blank=True, null=True)
    
    # Approval status
    approval_status = models.CharField(max_length=20, choices=APPROVAL_STATUS, default='pending', help_text="Admin approval status")
    rejection_reason = models.TextField(blank=True, help_text="Reason for rejection (if rejected)")
    
    # Availability
    is_active = models.BooleanField(default=True)
    is_emergency_available = models.BooleanField(default=False, help_text="Available for emergency requests")
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.provider.business_name}"



class Review(models.Model):
    """Customer reviews for service providers"""
    booking = models.OneToOneField('Booking', on_delete=models.CASCADE, related_name='review')
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5"
    )
    review_text = models.TextField(blank=True)
    
    # Review images (before/after photos)
    image1 = models.ImageField(upload_to='reviews/', blank=True, null=True)
    image2 = models.ImageField(upload_to='reviews/', blank=True, null=True)
    image3 = models.ImageField(upload_to='reviews/', blank=True, null=True)
    
    # Provider response
    provider_response = models.TextField(blank=True, help_text="Provider's response to review")
    responded_at = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.customer.username} for {self.provider.business_name} - {self.rating}★"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update provider's average rating
        self.provider.update_rating()


class ProviderPortfolio(models.Model):
    """Portfolio/gallery images for service providers"""
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='portfolio')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='portfolio/')
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Provider Portfolios"

    def __str__(self):
        return f"{self.provider.business_name} - {self.title}"


class ServiceRequest(models.Model):
    """Emergency or custom service requests from customers"""
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('assigned', 'Assigned to Provider'),
        ('closed', 'Closed'),
    ]

    URGENCY_LEVEL = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('emergency', 'Emergency'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_requests')
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    urgency = models.CharField(max_length=20, choices=URGENCY_LEVEL, default='medium')
    
    # Location
    address = models.TextField()
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    
    # Budget
    budget_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    budget_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    assigned_provider = models.ForeignKey(
        ServiceProvider, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assigned_requests'
    )
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Request #{self.id} - {self.title} ({self.urgency})"


class Booking(models.Model):
    """Bookings made by customers for services"""
    BOOKING_STATUS = [
        ('pending', 'Pending Confirmation'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Service and provider
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='bookings')
    
    # Customer info (can be registered user or guest)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=15)
    customer_address = models.TextField()
    
    # Booking details
    booking_date = models.DateField()
    booking_time = models.TimeField()
    notes = models.TextField(blank=True, help_text="Additional requirements or notes")
    
    # Status and tracking
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_emergency = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Booking #{self.id} - {self.service.title} by {self.customer_name}"


# ====================== PAYMENT & WALLET SYSTEM ======================

class Wallet(models.Model):
    """Digital wallet for users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=3, default='INR')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - ₹{self.balance}"

    def add_funds(self, amount):
        """Add money to wallet"""
        self.balance += amount
        self.save()

    def deduct_funds(self, amount):
        """Deduct money from wallet"""
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False


class Payment(models.Model):
    """Payment records for bookings"""
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    PAYMENT_METHOD = [
        ('card', 'Credit/Debit Card'),
        ('upi', 'UPI'),
        ('netbanking', 'Net Banking'),
        ('wallet', 'Wallet'),
        ('cash', 'Cash on Service'),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='payments')
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    
    # Payment gateway details
    transaction_id = models.CharField(max_length=100, unique=True, blank=True)
    gateway_order_id = models.CharField(max_length=100, blank=True)
    gateway_payment_id = models.CharField(max_length=100, blank=True)
    gateway_signature = models.CharField(max_length=200, blank=True)
    
    # Commission
    platform_commission = models.DecimalField(max_digits=5, decimal_places=2, default=15.00, help_text="Commission percentage")
    provider_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount paid to provider")
    
    # Refund
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    refund_reason = models.TextField(blank=True)
    refunded_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Payment #{self.id} - ₹{self.amount} ({self.status})"

    def calculate_provider_amount(self):
        """Calculate provider's share after commission"""
        commission_amount = (self.amount * self.platform_commission) / 100
        self.provider_amount = self.amount - commission_amount
        self.save()


class Transaction(models.Model):
    """Transaction history for wallet"""
    TRANSACTION_TYPE = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
        ('refund', 'Refund'),
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    description = models.CharField(max_length=200)
    reference_id = models.CharField(max_length=100, blank=True)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transaction_type} - ₹{self.amount} - {self.wallet.user.username}"


# ====================== MESSAGING SYSTEM ======================

class Message(models.Model):
    """Chat messages between customers and providers"""
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    
    message_text = models.TextField()
    attachment = models.FileField(upload_to='messages/', blank=True, null=True)
    
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"


# ====================== PROVIDER ANALYTICS & EARNINGS ======================

class ProviderEarnings(models.Model):
    """Track provider earnings"""
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='earnings')
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='provider_earning')
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='provider_earning')
    
    gross_amount = models.DecimalField(max_digits=10, decimal_places=2)
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    commission_amount = models.DecimalField(max_digits=10, decimal_places=2)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount provider receives")
    
    # Payout status
    PAYOUT_STATUS = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('paid', 'Paid'),
        ('hold', 'On Hold'),
    ]
    payout_status = models.CharField(max_length=20, choices=PAYOUT_STATUS, default='pending')
    paid_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Provider Earnings"

    def __str__(self):
        return f"{self.provider.business_name} - ₹{self.net_amount}"


class ProviderStats(models.Model):
    """Daily/monthly statistics for providers"""
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='stats')
    date = models.DateField()
    
    # Performance metrics
    bookings_received = models.PositiveIntegerField(default=0)
    bookings_completed = models.PositiveIntegerField(default=0)
    bookings_cancelled = models.PositiveIntegerField(default=0)
    
    # Earnings
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Ratings
    reviews_received = models.PositiveIntegerField(default=0)
    average_rating_day = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    
    # Response time (in minutes)
    average_response_time = models.PositiveIntegerField(default=0, help_text="Average response time in minutes")
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        unique_together = ['provider', 'date']
        verbose_name_plural = "Provider Stats"

    def __str__(self):
        return f"{self.provider.business_name} - {self.date}"


# ====================== PROMOTION & MARKETING ======================

class Coupon(models.Model):
    """Discount coupons"""
    COUPON_TYPE = [
        ('percentage', 'Percentage Discount'),
        ('fixed', 'Fixed Amount'),
        ('first_booking', 'First Booking Offer'),
    ]

    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    coupon_type = models.CharField(max_length=20, choices=COUPON_TYPE)
    
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, help_text="Percentage or fixed amount")
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    min_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Usage limits
    usage_limit = models.PositiveIntegerField(help_text="Total number of times coupon can be used", blank=True, null=True)
    used_count = models.PositiveIntegerField(default=0)
    per_user_limit = models.PositiveIntegerField(default=1, help_text="Times per user")
    
    # Validity
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    # Applicability
    applicable_categories = models.ManyToManyField(ServiceCategory, blank=True)
    applicable_services = models.ManyToManyField(Service, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.code} - {self.discount_value}% off"

    def is_valid(self):
        """Check if coupon is currently valid"""
        now = timezone.now()
        return (self.is_active and 
                self.valid_from <= now <= self.valid_to and
                (self.usage_limit is None or self.used_count < self.usage_limit))


class ServicePackage(models.Model):
    """Service bundles/packages for better pricing"""
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='packages')
    title = models.CharField(max_length=200)
    description = models.TextField()
    services = models.ManyToManyField(Service, related_name='packages')
    
    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    package_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Discounted bundle price")
    savings = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount saved")
    
    duration_months = models.PositiveIntegerField(default=1, help_text="Package validity in months")
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - ₹{self.package_price}"


class Referral(models.Model):
    """Referral program tracking"""
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals_made')
    referred = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referred_by')
    referral_code = models.CharField(max_length=20, unique=True)
    
    # Rewards
    referrer_reward = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    referred_reward = models.DecimalField(max_digits=10, decimal_places=2, default=50.00)
    
    # Status
    is_completed = models.BooleanField(default=False, help_text="Referral completed when referred user makes first booking")
    completed_at = models.DateTimeField(null=True, blank=True)
    rewards_credited = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.referrer.username} → {self.referred.username}"


class LoyaltyPoints(models.Model):
    """Loyalty points system for customers"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='loyalty_points')
    points = models.PositiveIntegerField(default=0)
    tier = models.CharField(max_length=20, default='bronze', help_text="bronze, silver, gold, platinum")
    
    total_earned = models.PositiveIntegerField(default=0)
    total_redeemed = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Loyalty Points"

    def __str__(self):
        return f"{self.user.username} - {self.points} points ({self.tier})"

    def add_points(self, points, description=""):
        """Add loyalty points"""
        self.points += points
        self.total_earned += points
        self.update_tier()
        self.save()

    def redeem_points(self, points):
        """Redeem loyalty points"""
        if self.points >= points:
            self.points -= points
            self.total_redeemed += points
            self.save()
            return True
        return False

    def update_tier(self):
        """Update loyalty tier based on total earned"""
        if self.total_earned >= 10000:
            self.tier = 'platinum'
        elif self.total_earned >= 5000:
            self.tier = 'gold'
        elif self.total_earned >= 2000:
            self.tier = 'silver'
        else:
            self.tier = 'bronze'


# ====================== CUSTOMER FEATURES ======================

class FavoriteProvider(models.Model):
    """Customer's favorite/saved providers"""
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_providers')
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['customer', 'provider']

    def __str__(self):
        return f"{self.customer.username} → {self.provider.business_name}"


class CustomerAddress(models.Model):
    """Multiple address management for customers"""
    ADDRESS_TYPE = [
        ('home', 'Home'),
        ('work', 'Work'),
        ('other', 'Other'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE)
    label = models.CharField(max_length=50, help_text="e.g., Home, Office, Parents House")
    
    address_line1 = models.CharField(max_length=200)
    address_line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    landmark = models.CharField(max_length=200, blank=True)
    
    # Location coordinates
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Customer Addresses"
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        return f"{self.customer.username} - {self.label}"


class Notification(models.Model):
    """Push notifications for users"""
    NOTIFICATION_TYPE = [
        ('booking', 'Booking Update'),
        ('payment', 'Payment Update'),
        ('review', 'New Review'),
        ('message', 'New Message'),
        ('promotion', 'Promotion/Offer'),
        ('system', 'System Notification'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    # Link to relevant object
    related_booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    action_url = models.CharField(max_length=200, blank=True)
    
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"


# ====================== PROVIDER VERIFICATION ======================

class ProviderDocument(models.Model):
    """Documents uploaded by providers for verification"""
    DOCUMENT_TYPE = [
        ('id_proof', 'Government ID (Aadhar/PAN/Driving License)'),
        ('business_license', 'Business License'),
        ('certificate', 'Professional Certificate'),
        ('insurance', 'Insurance Document'),
        ('police_clearance', 'Police Clearance Certificate'),
        ('address_proof', 'Address Proof'),
    ]

    VERIFICATION_STATUS = [
        ('pending', 'Pending Verification'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]

    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPE)
    document_file = models.FileField(upload_to='provider_documents/')
    document_number = models.CharField(max_length=100, blank=True, help_text="ID/License number")
    
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS, default='pending')
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_documents')
    verification_notes = models.TextField(blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    
    expires_at = models.DateField(null=True, blank=True, help_text="Document expiry date")
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.provider.business_name} - {self.get_document_type_display()}"


class ProviderInsurance(models.Model):
    """Insurance details for service providers"""
    provider = models.OneToOneField(ServiceProvider, on_delete=models.CASCADE, related_name='insurance')
    
    insurance_company = models.CharField(max_length=200)
    policy_number = models.CharField(max_length=100)
    coverage_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    policy_document = models.FileField(upload_to='insurance/')
    
    valid_from = models.DateField()
    valid_to = models.DateField()
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.provider.business_name} - {self.insurance_company}"


# ====================== ADVANCED BOOKING FEATURES ======================

class RecurringBooking(models.Model):
    """Recurring/subscription bookings"""
    FREQUENCY = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('biweekly', 'Bi-Weekly'),
        ('monthly', 'Monthly'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recurring_bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='recurring_bookings')
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='recurring_bookings')
    
    frequency = models.CharField(max_length=10, choices=FREQUENCY)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text="Leave blank for indefinite")
    
    preferred_time = models.TimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    is_active = models.BooleanField(default=True)
    next_booking_date = models.DateField()
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.username} - {self.service.title} ({self.frequency})"


class BookingExtension(models.Model):
    """Extended booking details - photos, signatures, ETA"""
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='extension')
    
    # Service completion photos
    before_photo1 = models.ImageField(upload_to='service_photos/', null=True, blank=True)
    before_photo2 = models.ImageField(upload_to='service_photos/', null=True, blank=True)
    after_photo1 = models.ImageField(upload_to='service_photos/', null=True, blank=True)
    after_photo2 = models.ImageField(upload_to='service_photos/', null=True, blank=True)
    
    # Digital signature
    customer_signature = models.ImageField(upload_to='signatures/', null=True, blank=True)
    provider_signature = models.ImageField(upload_to='signatures/', null=True, blank=True)
    
    # ETA and tracking
    estimated_arrival_time = models.DateTimeField(null=True, blank=True)
    actual_arrival_time = models.DateTimeField(null=True, blank=True)
    service_started_at = models.DateTimeField(null=True, blank=True)
    service_ended_at = models.DateTimeField(null=True, blank=True)
    
    # Additional details
    materials_used = models.TextField(blank=True, help_text="Materials/parts used during service")
    work_description = models.TextField(blank=True, help_text="Detailed work description")
    
    # Warranty
    warranty_period_days = models.PositiveIntegerField(default=0, help_text="Warranty period in days")
    warranty_terms = models.TextField(blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Extension for Booking #{self.booking.id}"


# ====================== PROVIDER SCHEDULING ======================

class ProviderAvailability(models.Model):
    """Provider's weekly availability schedule"""
    WEEKDAYS = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='availability_schedule')
    weekday = models.IntegerField(choices=WEEKDAYS)
    
    is_available = models.BooleanField(default=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    # Break time
    break_start = models.TimeField(null=True, blank=True)
    break_end = models.TimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['provider', 'weekday']
        ordering = ['weekday']
        verbose_name_plural = "Provider Availabilities"

    def __str__(self):
        return f"{self.provider.business_name} - {self.get_weekday_display()}"


class ProviderLeave(models.Model):
    """Provider leave/unavailable dates"""
    LEAVE_TYPE = [
        ('vacation', 'Vacation'),
        ('sick', 'Sick Leave'),
        ('personal', 'Personal'),
        ('maintenance', 'Maintenance'),
        ('other', 'Other'),
    ]

    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='leaves')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE)
    
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(blank=True)
    
    is_approved = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.provider.business_name} - {self.start_date} to {self.end_date}"
