
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from versatileimagefield.fields import VersatileImageField, \
    PPOIField



class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create Save a User"""
        if not email:
            raise ValueError('User must have a Email')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        if user:
            return user

    def create_superuser(self, email, password):
        """Create and Save a super User"""
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self.db)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """"Custom Model"""
    email = models.EmailField(max_length=225, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return str(self.email)



class Category(models.Model):
    name=models.CharField(max_length = 200)
    title = models.CharField(max_length = 200)
    description = models.TextField()
  
    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    order=models.IntegerField()
    image=VersatileImageField(blank=True,null=True,upload_to="Subcategory/",ppoi_field='image_ppoi')
    image_ppoi = PPOIField()    
    name=models.CharField(max_length = 200)

    def __str__(self):
        return self.name
    class Meta:
        unique_together = ['category', 'order']
        ordering = ['order']


class SubSubCategory(models.Model):
    subcategory = models.ForeignKey(SubCategory, related_name='subsubcategories', on_delete=models.CASCADE)
    order=models.IntegerField()
    image=VersatileImageField(blank=True,null=True,upload_to="Subcategory/",ppoi_field='image_ppoi')
    image_ppoi = PPOIField()
    name=models.CharField(max_length = 200)
    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['subcategory', 'order']
        ordering = ['order']




class Products(models.Model):
    subsubcategory = models.ForeignKey(SubSubCategory, related_name='products', on_delete=models.CASCADE)
    order=models.IntegerField()
    image=VersatileImageField(blank=True,null=True,upload_to="Subcategory/",ppoi_field='image_ppoi')
    image_ppoi = PPOIField()
    name=models.CharField(max_length = 200,default='Product Name')
    price=models.BigIntegerField()
    created_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['subsubcategory', 'order']
        ordering = ['order']


class Options(models.Model):
    product = models.ForeignKey(Products, related_name='options', on_delete=models.CASCADE)
    order=models.IntegerField()
    image=VersatileImageField(blank=True,null=True,upload_to="Subcategory/",ppoi_field='image_ppoi')
    image_ppoi = PPOIField()
    color=models.CharField(max_length = 200)
    size=models.CharField(max_length = 200,null=True,blank=True)
    stock=models.IntegerField()
    def __str__(self):
        return self.color

    class Meta:
        ordering = ['order']




class Offer(models.Model):
    product = models.OneToOneField(Products, related_name='offers', on_delete=models.CASCADE)
    offerPrice = models.BigIntegerField()
    endDate = models.DateTimeField(auto_now=True)




class NewCollection(models.Model):
    product = models.OneToOneField(Products, on_delete=models.CASCADE)
    endDate=models.DateTimeField(auto_now=True)