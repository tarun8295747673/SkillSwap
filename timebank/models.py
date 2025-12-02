from django.db import models
from .models import TimeEntry


# User Profile Table
class UserProfile(models.Model):
    username = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return self.username

# Category Table
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.category_name

# Service Offer Table
class ServiceOffer(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    available_hours = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Service Request Table
class ServiceRequest(models.Model):
    requester = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    offer = models.ForeignKey(ServiceOffer, on_delete=models.CASCADE)
    requested_hours = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=[
            ('Pending', 'Pending'),
            ('Accepted', 'Accepted'),
            ('Completed', 'Completed'),
            ('Cancelled', 'Cancelled')
        ],
        default='Pending'
    )
    request_date = models.DateTimeField(auto_now_add=True)

# Time Transaction Table
class TimeTransaction(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_transactions')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_transactions')
    service = models.ForeignKey(ServiceOffer, on_delete=models.CASCADE)
    hours_transferred = models.DecimalField(max_digits=5, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)

# Reviews Table
class Reviews(models.Model):
    reviewer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='given_reviews')
    reviewee = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_reviews')
    service = models.ForeignKey(ServiceOffer, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    review_date = models.DateTimeField(auto_now_add=True)
