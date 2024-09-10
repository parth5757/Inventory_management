from django.contrib import admin
from .models import Users, UserShippingAddress, Modules, UserPermission, ActivityLog

# Register your models here
admin.site.register(Users)
admin.site.register(UserShippingAddress)
admin.site.register(Modules)
admin.site.register(UserPermission)
admin.site.register(ActivityLog)
