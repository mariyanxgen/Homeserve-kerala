from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .forms import RoleRegistrationForm, ProviderOnboardingForm
from .models import ServiceProvider


def register_view(request):
    """User registration with role selection (customer or provider)"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RoleRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Save optional email if provided
            email = form.cleaned_data.get('email')
            if email:
                user.email = email
                user.save()

            role = form.cleaned_data.get('role')
            login(request, user)

            if role == 'provider':
                messages.success(request, f'Account created! Please complete your provider profile.')
                return redirect('provider_onboarding')
            else:
                messages.success(request, f'Welcome {user.username}! Your account has been created successfully.')
                return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RoleRegistrationForm()

    return render(request, 'frontend/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'frontend/login.html', {'form': form})


@login_required
@require_http_methods(["POST", "GET"])
def logout_view(request):
    """User logout view"""
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('home')
    # Allow GET requests to logout as well (fallback)
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile_view(request):
    """User profile view"""
    return render(request, 'frontend/profile.html', {
        'user': request.user
    })


@login_required
def provider_onboarding_view(request):
    """Create a ServiceProvider profile for the logged-in user"""
    # If provider profile already exists, skip onboarding
    if hasattr(request.user, 'provider_profile'):
        messages.info(request, 'Your provider profile already exists.')
        return redirect('profile')

    if request.method == 'POST':
        form = ProviderOnboardingForm(request.POST, request.FILES)
        if form.is_valid():
            provider = form.save(commit=False)
            provider.user = request.user
            provider.verification_status = 'pending'
            provider.save()
            messages.success(request, 'Provider profile created! Verification pending.')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Pre-fill email if user has one
        initial = {}
        if request.user.email:
            initial['email'] = request.user.email
        form = ProviderOnboardingForm(initial=initial)

    return render(request, 'frontend/provider_onboarding.html', {'form': form})
