from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from decimal import Decimal
from django.core.mail import send_mail
from datetime import date
from django.db.models import Q
from django.db.models import Sum, Avg
from django.db import models

from django.contrib import messages as django_messages
from .models import Message, TimeBankUser


from .models import TimeTransaction, UserProfile, ServiceOffer, ServiceRequest, Category, Review, Notification
from .forms import EditUserProfileForm

User = get_user_model()



def home_view(request):
    user_count = TimeBankUser.objects.count()
    active_services = ServiceOffer.objects.count()
    total_hours = TimeTransaction.objects.aggregate(total=Sum('hours'))['total'] or 0
    return render(request, 'mainapp/home.html', {
        'user_count': user_count,
        'active_services': active_services,
        'total_hours': total_hours,
    })

# Home Page
# def home_view(request):
#     return render(request, 'mainapp/home.html')

# User Registration
def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'mainapp/register.html', {
                'error': "Username already taken. Please choose another."
            })

        user = User.objects.create_user(username=username, password=password, hours_available=0.0)
        
        # ✅ No need for messages.success() here
        return render(request, 'mainapp/register_success.html')  # 👈 directly show alert page

    return render(request, 'mainapp/register.html')
    return render(request, 'mainapp/login.html')


@login_required
@login_required
def send_message(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)  # ✅ Fix: fetch user
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, receiver=receiver, content=content)
            messages.success(request, f"Message sent to {receiver.username}.")
    return redirect('dashboard')


@login_required
def inbox(request):
    received_msgs = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    sent_msgs = Message.objects.filter(sender=request.user).order_by('-timestamp')
    return render(request, 'mainapp/inbox.html', {'received_messages': received_msgs, 'sent_messages': sent_msgs})


# User Login
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            today = timezone.now().date()

            already_given = TimeTransaction.objects.filter(
                receiver=user,
                description="Login Bonus",
                timestamp__date=today
            ).exists()

            if not already_given:
                TimeTransaction.objects.create(
                    sender=None,
                    receiver=user,
                    hours=Decimal('2.0'),
                    description="Login Bonus"
                )

            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'mainapp/login.html')

# Dashboard View
@login_required
def dashboard(request):
    user = request.user

    # Get or create profile
    profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={
            'full_name': user.get_full_name(),
            'phone_number': '',
            'email': '',
            'time_balance': 0,
        }
    )

    # ✅ Define time_entries before using it
    time_entries = TimeTransaction.objects.filter(
        Q(sender=user) | Q(receiver=user)
    ).order_by('-timestamp')

    # ✅ Only add positive hours where user is receiver
    total_balance = sum(entry.hours for entry in time_entries if entry.receiver == user)

    my_offers = ServiceOffer.objects.filter(user=user)
    my_requests = ServiceRequest.objects.filter(requester=user).order_by('-id')
    available_offers = ServiceOffer.objects.exclude(user=user).filter(available_hours__gt=0)
    incoming_requests = ServiceRequest.objects.filter(offer__user=user, status='Pending')
    received_messages = Message.objects.filter(receiver=user).order_by('-timestamp')

    return render(request, 'mainapp/dashboard.html', {
        'user': user,
        'profile': profile,
        'time_entries': time_entries,
        'total_balance': total_balance,
        'user_hours_available': user.hours_available,
        'offer_service': my_offers,
        'service_request': my_requests,
        'available_offers': available_offers,
        'incoming_requests': incoming_requests,
        'received_messages': received_messages,  # ✅ Pass to template

    })
# Offer a service
@login_required
def offer_service(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        available_hours = Decimal(request.POST.get('available_hours'))
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)

        offer = ServiceOffer.objects.create(
            user=request.user,
            title=title,
            description=description,
            available_hours=available_hours,
            category=category
        )

        TimeTransaction.objects.create(
            sender=None,
            receiver=request.user,
            description=f"Offered service: {title}",
            hours=available_hours,
            timestamp=timezone.now()
        )

        messages.success(request, f"Service offered successfully! {available_hours} hrs added to your balance.")
        return redirect('dashboard')

    categories = Category.objects.all()
    return render(request, 'mainapp/offer_service.html', {'categories': categories})

# Request a service
@login_required
def request_service(request, offer_id):
    offer = get_object_or_404(ServiceOffer, id=offer_id)
    if request.method == 'POST':
        requested_hours = Decimal(request.POST.get('requested_hours'))
        if requested_hours > offer.available_hours:
            messages.error(request, "Not enough hours available.")
            return redirect('dashboard')

        ServiceRequest.objects.create(
            offer=offer,
            requester=request.user,
            requested_hours=requested_hours,
            status='Pending'
        )

        offer.available_hours -= requested_hours
        offer.save()

        TimeTransaction.objects.create(
            sender=request.user,
            receiver=offer.user,
            description=f"Requested service: {offer.title}",
            hours=-requested_hours,
            timestamp=timezone.now()
        )

        TimeTransaction.objects.create(
            sender=request.user,
            receiver=offer.user,
            description=f"Provided service to {request.user.username}",
            hours=requested_hours,
            timestamp=timezone.now()
        )

        messages.success(request, "Service requested successfully!")
        return redirect('dashboard')
    return redirect('dashboard')


# View list of services to request
@login_required
def request_service_list(request):
    offers = ServiceOffer.objects.exclude(user=request.user)
    return render(request, 'mainapp/all_requests.html', {'offers': offers})

# View available services
@login_required
def available_services(request):
    offers = ServiceOffer.objects.exclude(user=request.user).filter(available_hours__gt=0)
    return render(request, 'mainapp/service.html', {'offers': offers})

# Respond to a request (Accept/Reject)
@login_required
def respond_request(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id)
    if service_request.offer.user != request.user:
        return HttpResponse("Unauthorized", status=403)

    if request.method == "POST":
        action = request.POST.get("response")
        if action == "accept" and service_request.status == "Pending":
            service_request.status = "Accepted"
            service_request.save()

            TimeTransaction.objects.create(
                sender=service_request.offer.user,
                receiver=service_request.requester,
                description=f"Provided service to {service_request.requester.username}",
                hours=service_request.requested_hours,
                timestamp=timezone.now()
            )

            TimeTransaction.objects.create(
                sender=service_request.requester,
                receiver=service_request.offer.user,
                description=f"Accepted request for: {service_request.offer.title}",
                hours=-service_request.requested_hours,
                timestamp=timezone.now()
            )

            messages.success(request, "Request accepted and time exchanged.")
        elif action == "reject":
            service_request.status = "Rejected"
            service_request.save()
            messages.info(request, "Request rejected.")

        return redirect('dashboard')

# Delete a service request
@login_required
def delete_request(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id, requester=request.user)
    offer = service_request.offer
    offer.available_hours += Decimal(service_request.requested_hours)
    offer.save()
    service_request.delete()
    return redirect('dashboard')

# View User Profile
@login_required
def user_profile_view(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={
            'full_name': user.get_full_name(),
            'phone_number': '',
            'Email': '',
            'time_balance': 0,
        }
    )
    return render(request, 'mainapp/user_profile.html', {'profile': profile})

# Edit Profile
@login_required
def edit_profile_view(request):
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)

    if request.method == 'POST':
        form = EditUserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('user_profile')
    else:
        form = EditUserProfileForm(instance=profile)

    return render(request, 'mainapp/edit_profile.html', {'form': form})

# View Request Detail
@login_required
def view_request_detail(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id)

    if service_request.offer.user != request.user:
        return HttpResponse("Unauthorized", status=403)

    requester_profile = get_object_or_404(UserProfile, user=service_request.requester)

    return render(request, 'mainapp/view_request_detail.html', {
        'service_request': service_request,
        'requester_profile': requester_profile,
    })

# ========== NEW FEATURE PAGES ==========

# Categories Page - Browse services by category
@login_required
def categories_view(request):
    categories = Category.objects.all()
    category_data = []
    
    for category in categories:
        service_count = ServiceOffer.objects.filter(category=category, available_hours__gt=0).count()
        category_data.append({
            'category': category,
            'service_count': service_count
        })
    
    return render(request, 'mainapp/categories.html', {
        'category_data': category_data
    })


# Category Detail - View services in a specific category
@login_required
def category_detail_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    services = ServiceOffer.objects.filter(category=category, available_hours__gt=0).exclude(user=request.user)
    
    return render(request, 'mainapp/category_detail.html', {
        'category': category,
        'services': services
    })


# Transaction History Page
@login_required
def transaction_history_view(request):
    transactions = TimeTransaction.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('-timestamp')
    
    # Calculate totals
    earned = TimeTransaction.objects.filter(receiver=request.user).aggregate(
        total=Sum('hours'))['total'] or Decimal('0')
    spent = TimeTransaction.objects.filter(sender=request.user).aggregate(
        total=Sum('hours'))['total'] or Decimal('0')
    
    return render(request, 'mainapp/transaction_history.html', {
        'transactions': transactions,
        'total_earned': earned,
        'total_spent': spent,
        'balance': earned - spent
    })


# User Directory - Browse all users
@login_required
def user_directory_view(request):
    search_query = request.GET.get('search', '')
    
    users = TimeBankUser.objects.exclude(id=request.user.id)
    
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(userprofile__full_name__icontains=search_query)
        )
    
    user_data = []
    for user in users:
        profile = UserProfile.objects.filter(user=user).first()
        services_count = ServiceOffer.objects.filter(user=user, available_hours__gt=0).count()
        avg_rating = Review.objects.filter(reviewee=user).aggregate(
            avg=models.Avg('rating'))['avg'] or 0
        
        user_data.append({
            'user': user,
            'profile': profile,
            'services_count': services_count,
            'avg_rating': round(avg_rating, 1) if avg_rating else 0
        })
    
    return render(request, 'mainapp/user_directory.html', {
        'user_data': user_data,
        'search_query': search_query
    })


# Service Detail Page
@login_required
def service_detail_view(request, service_id):
    service = get_object_or_404(ServiceOffer, id=service_id)
    provider_profile = UserProfile.objects.filter(user=service.user).first()
    
    # Get provider's reviews
    reviews = Review.objects.filter(reviewee=service.user).order_by('-created_at')[:5]
    avg_rating = Review.objects.filter(reviewee=service.user).aggregate(
        avg=models.Avg('rating'))['avg'] or 0
    
    return render(request, 'mainapp/service_detail.html', {
        'service': service,
        'provider_profile': provider_profile,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1) if avg_rating else 0
    })


# Notifications Center
@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user)
    unread_count = notifications.filter(is_read=False).count()
    
    return render(request, 'mainapp/notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })


# Mark notification as read
@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    
    if notification.link:
        return redirect(notification.link)
    return redirect('notifications')


# Add Review for a completed service
@login_required
def add_review_view(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id)
    
    # Only requester can review the provider
    if service_request.requester != request.user:
        messages.error(request, "You can only review services you requested.")
        return redirect('dashboard')
    
    if service_request.status != 'Accepted':
        messages.error(request, "You can only review accepted services.")
        return redirect('dashboard')
    
    # Check if already reviewed
    existing_review = Review.objects.filter(
        service_request=service_request,
        reviewer=request.user
    ).first()
    
    if existing_review:
        messages.info(request, "You have already reviewed this service.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment', '')
        
        Review.objects.create(
            service_request=service_request,
            reviewer=request.user,
            reviewee=service_request.offer.user,
            rating=rating,
            comment=comment
        )
        
        # Create notification for the reviewee
        Notification.objects.create(
            user=service_request.offer.user,
            notification_type='new_review',
            title='New Review Received',
            message=f"{request.user.username} left you a {rating}-star review!",
            link=f'/profile/user/{service_request.offer.user.id}/'
        )
        
        messages.success(request, "Review submitted successfully!")
        return redirect('dashboard')
    
    return render(request, 'mainapp/add_review.html', {
        'service_request': service_request
    })


# My Services Management Page
@login_required
def my_services_view(request):
    my_services = ServiceOffer.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'mainapp/my_services.html', {
        'my_services': my_services
    })


# Edit Service
@login_required
def edit_service_view(request, service_id):
    service = get_object_or_404(ServiceOffer, id=service_id, user=request.user)
    
    if request.method == 'POST':
        service.title = request.POST.get('title')
        service.description = request.POST.get('description')
        service.available_hours = Decimal(request.POST.get('available_hours'))
        category_id = request.POST.get('category')
        service.category = Category.objects.get(id=category_id)
        service.save()
        
        messages.success(request, "Service updated successfully!")
        return redirect('my_services')
    
    categories = Category.objects.all()
    return render(request, 'mainapp/edit_service.html', {
        'service': service,
        'categories': categories
    })


# Delete Service
@login_required
def delete_service_view(request, service_id):
    service = get_object_or_404(ServiceOffer, id=service_id, user=request.user)
    
    if request.method == 'POST':
        service.delete()
        messages.success(request, "Service deleted successfully!")
        return redirect('my_services')
    
    return redirect('my_services')


# Statistics/Analytics Page
@login_required
def statistics_view(request):
    user = request.user
    
    # Transaction statistics
    total_earned = TimeTransaction.objects.filter(receiver=user).aggregate(
        total=Sum('hours'))['total'] or Decimal('0')
    total_spent = TimeTransaction.objects.filter(sender=user).aggregate(
        total=Sum('hours'))['total'] or Decimal('0')
    
    # Service statistics
    services_offered = ServiceOffer.objects.filter(user=user).count()
    services_requested = ServiceRequest.objects.filter(requester=user).count()
    
    # Request statistics
    pending_requests = ServiceRequest.objects.filter(offer__user=user, status='Pending').count()
    accepted_requests = ServiceRequest.objects.filter(offer__user=user, status='Accepted').count()
    rejected_requests = ServiceRequest.objects.filter(offer__user=user, status='Rejected').count()
    
    # Rating statistics
    avg_rating = Review.objects.filter(reviewee=user).aggregate(
        avg=models.Avg('rating'))['avg'] or 0
    total_reviews = Review.objects.filter(reviewee=user).count()
    
    # Recent activity
    recent_transactions = TimeTransaction.objects.filter(
        Q(sender=user) | Q(receiver=user)
    ).order_by('-timestamp')[:10]
    
    return render(request, 'mainapp/statistics.html', {
        'total_earned': total_earned,
        'total_spent': total_spent,
        'current_balance': total_earned - total_spent,
        'services_offered': services_offered,
        'services_requested': services_requested,
        'pending_requests': pending_requests,
        'accepted_requests': accepted_requests,
        'rejected_requests': rejected_requests,
        'avg_rating': round(avg_rating, 1) if avg_rating else 0,
        'total_reviews': total_reviews,
        'recent_transactions': recent_transactions
    })


# Help/FAQ Page
@login_required
def help_faq_view(request):
    return render(request, 'mainapp/help_faq.html')


# Public User Profile
@login_required
def public_user_profile_view(request, user_id):
    viewed_user = get_object_or_404(TimeBankUser, id=user_id)
    profile = UserProfile.objects.filter(user=viewed_user).first()
    
    # Get user's services
    services = ServiceOffer.objects.filter(user=viewed_user, available_hours__gt=0)
    
    # Get user's reviews
    reviews = Review.objects.filter(reviewee=viewed_user).order_by('-created_at')
    avg_rating = reviews.aggregate(avg=models.Avg('rating'))['avg'] or 0
    
    return render(request, 'mainapp/public_user_profile.html', {
        'viewed_user': viewed_user,
        'profile': profile,
        'services': services,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1) if avg_rating else 0,
        'total_reviews': reviews.count()
    })


# Custom error pages
def page_not_found(request, exception):
    return render(request, '404.html', status=404)

def server_error(request):
    return render(request, '500.html', status=500)
