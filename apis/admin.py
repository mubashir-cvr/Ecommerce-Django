from django.contrib import admin
from .models import Category,SubCategory,SubSubCategory,Options,Products,Offer
# Register your models here.


admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(SubSubCategory)
admin.site.register(Products)
admin.site.register(Options)
admin.site.register(Offer)


