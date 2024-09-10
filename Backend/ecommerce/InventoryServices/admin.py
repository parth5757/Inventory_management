from django.contrib import admin
from .models import Warehouse, RackAndShelvesAndFloor, Inventory, InventoryLog

# Register your models here
admin.site.register(Warehouse)
admin.site.register(RackAndShelvesAndFloor)
admin.site.register(Inventory)
admin.site.register(InventoryLog)
