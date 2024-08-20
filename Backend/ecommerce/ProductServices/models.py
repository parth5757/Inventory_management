from django.db import models
from UserServices.models import Users
# Create your models here.

class Categories (models.Model):
    id=models.AutoField (primary_key=True)
    name=models.CharField(max_length=255, blank=True, null=True)
    image=models.TextField()
    description=models.TextField()
    display_order=models.IntegerField(default=0)
    parent_id=models. ForeignKey('self', on_delete=models. CASCADE, blank=True, null=True)
    domain_user_id=models.ForeignKey(Users, on_delete=models. CASCADE, blank=True, null=True, related_name='domain_user_id')
    added_by_user_id=models.ForeignKey(Users, on_delete=models. CASCADE, blank=True, null=True, related_name='added_by_user_id')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.name)
    
    class Meta:
        ordering = ('-created_at')


class Products(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255,blank=True,null=True)
    image=models.JSONField()
    description=models.TextField()
    specifications=models.JSONField()
    html_description=models.TextField()
    highlights=models.JSONField()
    sku=models.CharField(max_length=255)
    initial_buying_price=models.FloatField()
    initial_selling_price=models.FloatField()
    weight=models.FloatField()
    dimensions=models.CharField(default='0x0x0',max_length=255)
    uom=models.CharField(max_length=255)
    color=models.CharField(max_length=255)
    tax_percentage=models.FloatField()
    brand=models.CharField(max_length=255)
    brand_model=models.CharField(max_length=255)
    status=models.CharField(max_length=255,choices=[('ACTIVE','ACTIVE'),('INACTIVE','INACTIVE')],default='ACTIVE')
    seo_title=models.CharField(max_length=255)
    seo_description=models.TextField()
    seo_keywords=models.JSONField()
    addition_details=models.JSONField()
    category_id=models.ForeignKey(Categories,on_delete=models.CASCADE,blank=True,null=True,related_name='category_id_products')
    domain_user_id=models.ForeignKey(Users,on_delete=models.CASCADE,blank=True,null=True,related_name='domain_user_id_products')
    added_by_user_id=models.ForeignKey(Users,on_delete=models.CASCADE,blank=True,null=True,related_name='added_by_user_id_products')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.name)
    
    class Meta:
        ordering = ('-created_at')

