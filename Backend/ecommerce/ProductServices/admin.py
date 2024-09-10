from django.contrib import admin
from .models import Categories, Products, ProductQuestions, ProductReviews

admin.site.register(Categories)
admin.site.register(Products)
admin.site.register(ProductQuestions)
admin.site.register(ProductReviews)