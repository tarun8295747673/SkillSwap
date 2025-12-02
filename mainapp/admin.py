from django.contrib import admin
from .models import (
    TimeBankUser, UserProfile, TimeEntry, Category, 
    ServiceOffer, ServiceRequest, Message, TimeTransaction,
    Review, Notification
)

admin.site.register(TimeBankUser)
admin.site.register(UserProfile)
admin.site.register(TimeEntry)
admin.site.register(Category)
admin.site.register(ServiceOffer)
admin.site.register(ServiceRequest)
admin.site.register(Message)
admin.site.register(TimeTransaction)
admin.site.register(Review)
admin.site.register(Notification)
