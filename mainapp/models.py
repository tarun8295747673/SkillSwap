from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# ✅ Custom User Model
class TimeBankUser(AbstractUser):
    hours_available = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return self.username


# ✅ User Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    time_balance = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.full_name


# ✅ Time Entry Model (for tracking logs)
class TimeEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='time_entries')
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.hours} hours"


# ✅ Service Category Model
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.category_name


# ✅ Service Offer Model
class ServiceOffer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    available_hours = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ✅ Service Request Model
class ServiceRequest(models.Model):
    offer = models.ForeignKey(ServiceOffer, on_delete=models.CASCADE)
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    requested_hours = models.FloatField()
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"{self.requester.username} requested {self.requested_hours}h from {self.offer.title}"


# ✅ Messaging System
class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"


# ✅ Time Transaction Model
class TimeTransaction(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_transactions', null=True)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_transactions', null=True)
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.sender and self.receiver:
            return f"{self.sender.username} → {self.receiver.username} : {self.hours}h"
        elif self.receiver:
            return f"System → {self.receiver.username} : {self.hours}h"
        elif self.sender:
            return f"{self.sender.username} → System : {self.hours}h"
        else:
            return f"Anonymous transaction of {self.hours}h"


# ✅ Review/Rating Model
class Review(models.Model):
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='given_reviews')
    reviewee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('service_request', 'reviewer')

    def __str__(self):
        return f"{self.reviewer.username} rated {self.reviewee.username} - {self.rating} stars"


# ✅ Notification Model
class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('service_request', 'Service Request'),
        ('request_accepted', 'Request Accepted'),
        ('request_rejected', 'Request Rejected'),
        ('new_message', 'New Message'),
        ('new_review', 'New Review'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=200, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"
