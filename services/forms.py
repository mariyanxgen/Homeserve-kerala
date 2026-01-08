from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Booking, ServiceProvider


class BookingForm(forms.ModelForm):
    """Form for booking a service (for both logged-in and guest users)"""
    
    class Meta:
        model = Booking
        fields = ['customer_name', 'customer_email', 'customer_phone', 'customer_address', 
                  'booking_date', 'booking_time', 'notes', 'is_emergency']
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            }),
            'customer_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),
            'customer_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your complete address'
            }),
            'booking_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'booking_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any special requirements or instructions? (optional)'
            }),
            'is_emergency': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'customer_name': 'Full Name',
            'customer_email': 'Email Address',
            'customer_phone': 'Phone Number',
            'customer_address': 'Service Address',
            'booking_date': 'Preferred Date',
            'booking_time': 'Preferred Time',
            'notes': 'Additional Notes',
            'is_emergency': 'This is an emergency service request'
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-fill fields for logged-in users
        if user and user.is_authenticated:
            self.fields['customer_name'].initial = user.get_full_name() or user.username
            self.fields['customer_email'].initial = user.email


class RoleRegistrationForm(UserCreationForm):
    """Registration form with role selection (customer or provider)"""
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('provider', 'Service Provider'),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
        label='Register as'
    )
    email = forms.EmailField(
        required=False,
        label='Email (optional)'
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2", "role")


class ProviderOnboardingForm(forms.ModelForm):
    """Collect required details to create a ServiceProvider profile"""

    class Meta:
        model = ServiceProvider
        fields = [
            'business_name', 'contact_number', 'email', 'address', 'city', 'state', 'pincode',
            'experience_years', 'bio', 'available_from', 'available_to', 'profile_image'
        ]
        widgets = {
            'business_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'available_from': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'available_to': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }
