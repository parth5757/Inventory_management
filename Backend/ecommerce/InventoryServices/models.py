from django.db import models
from UserServices.models import Users
from ProductServices.models import Products
from OrderServices.models import PurchaseOrder, PurchaseOrderItems, PurchaseOrderItemInwardedLog, SalesOrder

class Warehouse(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    pincode = models.IntegerField(max_length=10)
    Warehouse_manager = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name='warehouse_manager')
    phone = models.CharField(max_length=255)
    email = models.EmailField()
    status = models.CharField(max_length=255, choices=[('ACTIVE', 'ACTIVE'), ('INACTIVE', 'INACTIVE')], default='ACTIVE')
    size = models.CharField(max_length=255, choices=[('SMALL', 'SMALL'),('MEDIUM', 'MEDIUM'),('LARGE', 'LARGE')], default='SMALL')
    capacity = models.CharField(max_length=255, choices=[('LOW','LOW'),('MEDIUM', 'MEDIUM'),('HIGH','HIGH')], default='LOw')
    Warehouse_type = models.CharField(max_length=255, choices=[('OWNED', 'OWNED'),('LEASED','LEASED')])
    additional_details = models.JSONField()
    domain_user_id=models.ForeignKey(Users,on_delete=models.CASCADE,blank=True,null=True,related_name='domain_user_id_products')
    added_by_user_id=models.ForeignKey(Users,on_delete=models.CASCADE,blank=True,null=True,related_name='added_by_user_id_products')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.name)
    
    class Meta:
        ordering = ('-created_at')

class RackAndShelvesAndFloor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    warehouse_id = models.ForeignKey(Warehouse, on_delete=models.CASCADE, blank=True, null=True, related_name='warehouse_id')
    rack = models.CharField(max_length=255, blank=True, null=True)
    shelf = models.CharField(max_length=255, blank=True, null=True)
    floor = models.CharField(max_length=255, blank=True, null=True)
    additional_details = models.JSONField()
    domain_user_id=models.ForeignKey(Users,on_delete=models.CASCADE,blank=True,null=True,related_name='domain_user_id_products')
    added_by_user_id=models.ForeignKey(Users,on_delete=models.CASCADE,blank=True,null=True,related_name='added_by_user_id_products')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return str(self.so_id)

    class Meta:
        ordering = ('-created_date')   

class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    purchase_order_id = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, blank=True, null=True, related_name='purchase_order_id')
    purchase_order_item_id = models.ForeignKey(PurchaseOrderItems, on_delete=models.CASCADE, blank=True, null=True, related_name='purchase_order_item_id')
    purchase_order_item_inwarded_item_id = models.ForeignKey(PurchaseOrderItemInwardedLog, on_delete=models.CASCADE, blank=True, null=True, related_name='purchase_order_item_id')
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE, blank=True, null=True, related_name='product_id')
    warehouse_id = models.ForeignKey(Warehouse,on_delete=models.CASCADE, blank=True, null=True, related_name='warhouse_id')
    rack_shelf_floor_id = models.ForeignKey(RackAndShelvesAndFloor, on_delete=models.CASCADE, blank=True, null=True, related_name='rack_shelf_floor_id')
    quantity = models.IntegerField()
    mrp = models.CharField(max_length=255, blank=True, null=True)
    discount_type = models.CharField(max_length=255, choices=[('PERCENTAGE', 'PERCENTAGE'), ('AMOUNT', 'AMOUNT'), ('NO DISCOUNT', 'NO DISCOUNT')], default='PERCENTAGE')
    discount_value = models.FloatField()
    sr_no = models.CharField(max_length=255, null=True, blank=True)
    mfg_date = models.DateTimeField(blank=True, null=True)
    uom = models.CharField(max_length=255)
    received_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)
    quantity_inwarded = models.IntegerField()
    buy_price = models.DecimalField(max_digits=2, decimal_places=3)
    sell_price = models.DecimalField(max_digits=2, decimal_places=3)
    tax_percentage = models.DecimalField(max_digits=2, decimal_places=2)
    stock_status = models.CharField(max_length=255, choices=[('IN_STOCK', 'IN_STOCK'), ('OUT_OF_STOCK', 'OUT_OF_STOCK'),('DAMAGED', 'DAMAGED'),('LOST', 'LOST')], default='IN_STOCK')
    inward_time = models.CharField(max_length=255, choices=[('PURCHASE', 'PURCHASE'), ('RETURN', 'RETURN'), ('REPLACEMENT', 'REPLACEMENT'), ('WAREHOUSE TRANSFER', 'WAREHOUSE TRANSFER')], default='PURCHASE')

    additional_details = models.JSONField()
    domain_user_id=models.ForeignKey(Users,on_delete=models.CASCADE,blank=True,null=True,related_name='domain_user_id_products')
    added_by_user_id=models.ForeignKey(Users,on_delete=models.CASCADE,blank=True,null=True,related_name='added_by_user_id_products')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class InventoryLog(models.Model):
    id=models.AutoField(primary_key=True)
    po_id=models.ForeignKey(PurchaseOrder,on_delete=models.CASCADE,blank=True,null=True,related_name='po_id_inventory_log')
    so_id=models.ForeignKey(SalesOrder,on_delete=models.CASCADE,blank=True,null=True,related_name='so_id_inventory_log')
    inventory_id=models.ForeignKey(Inventory,on_delete=models.CASCADE,blank=True,null=True,related_name='inventory_id_inventory_log')
    warehouse_id=models.ForeignKey(Warehouse,on_delete=models.CASCADE,blank=True,null=True,related_name='warehouse_id_inventory_log')
    rack_shelf_floor_id=models.ForeignKey(RackAndShelvesAndFloor,on_delete=models.CASCADE,blank=True,null=True,related_name='rack_shelf_floor_id_inventory_log')
    quantity=models.IntegerField()
    status=models.CharField(max_length=255,choices=[('INWARD','INWARD'),('OUTWARD','OUTWARD'),('DAMAGED','DAMAGED'),('LOST','LOST'),('EXPIRED','EXPIRED'),('RETURNED','RETURNED'),('ADJUSTMENT','ADJUSTMENT'),('WAREHOUSE TRANSFER','WAREHOUSE TRANSFER')],default='IN_STOCK')
    additional_details=models.JSONField()
    domain_user_id=models.ForeignKey(Users,on_delete=models.CASCADE,blank=True,null=True,related_name='domain_user_id_inventory_log')
    added_by_user_id=models.ForeignKey(Users,on_delete=models.CASCADE,blank=True,null=True,related_name='added_by_user_id_inventory_log')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)