from django.contrib import admin
from .models import TimeBankUser, Category, ServiceOffer, ServiceRequest, TimeTransaction

admin.site.register(TimeBankUser)
admin.site.register(Category)
admin.site.register(ServiceOffer)
admin.site.register(ServiceRequest)
admin.site.register(TimeTransaction)
