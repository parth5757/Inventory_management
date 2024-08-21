from django.db import models
from UserServices.models import Users

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
    capacity = models.CharField(max_length=255, choices=[('LOW','LOW'),('MEDIUM', 'MEDIUM'),('HIGH','HIGH')])
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