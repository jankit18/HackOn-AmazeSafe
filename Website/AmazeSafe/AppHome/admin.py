from django.contrib import admin
from .models import UserInfo, AmazeUsersOrders, AmazeWarriorsOrders

# Register your models here.

admin.site.register(UserInfo) #Registered ContentImage
admin.site.register(AmazeWarriorsOrders)
admin.site.register(AmazeUsersOrders)