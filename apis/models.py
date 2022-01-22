
from locale import currency
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey
from django.utils import tree
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
        user.name="admin"
        user.save(using=self.db)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """"Custom Model"""
    email = models.EmailField(max_length=225, unique=True)
    name=models.CharField(max_length=225)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return str(self.email)

class AddressesOfUser(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=225)
    city = models.CharField(max_length=225)
    country = models.CharField(max_length=225)
    pincode = models.CharField(max_length=225)
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    phone = models.CharField(max_length=225)
    email = models.EmailField(null=True,blank=True)

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
    image=VersatileImageField(blank=True,null=True,upload_to="SubSubcategory/",ppoi_field='image_ppoi')
    image_ppoi = PPOIField()
    name=models.CharField(max_length = 200)
    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['subcategory', 'order']
        ordering = ['order']

class Brand(models.Model):
    name = models.CharField(max_length = 225)
    is_popular =models.BooleanField(default=False)

class Products(models.Model):
    subsubcategory = models.ForeignKey(SubSubCategory, related_name='products', on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.CASCADE,null=True)
    order=models.IntegerField()
    image=VersatileImageField(blank=True,null=True,upload_to="Products/",ppoi_field='image_ppoi')
    image_ppoi = PPOIField()
    name=models.CharField(max_length = 200,default='Product Name')
    productpriceEuro=models.BigIntegerField(default=0)
    productpriceDollar=models.BigIntegerField(default=0)
    productpriceSterling=models.BigIntegerField(default=0)
    productpriceDirham=models.BigIntegerField(default=0)
    productpriceSar=models.BigIntegerField(default=0)
    created_date=models.DateTimeField(auto_now=True)
    stock=models.IntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['subsubcategory', 'order']
        ordering = ['order']


class Options(models.Model):
    product = models.ForeignKey(Products, related_name='options', on_delete=models.CASCADE)
    order=models.IntegerField()
    image_one=VersatileImageField(blank=True,null=True,upload_to="Options/",ppoi_field='image_one_ppoi')
    image_one_ppoi = PPOIField()
    image_two=VersatileImageField(blank=True,null=True,upload_to="Options/",ppoi_field='image_two_ppoi')
    image_two_ppoi = PPOIField()
    image_three=VersatileImageField(blank=True,null=True,upload_to="Options/",ppoi_field='image_three_ppoi')
    image_three_ppoi = PPOIField()
    color=models.CharField(max_length = 200)
    colorhash=models.CharField(max_length = 200)
    stock=models.IntegerField(null=True)
    def __str__(self):
        return self.color

    class Meta:
        ordering = ['order']

class Sizes(models.Model):
    option = models.ForeignKey(Options, related_name='sizes', on_delete=models.CASCADE)
    size=models.CharField(max_length = 200,null=True,blank=True)
    stock=models.IntegerField(null=True)


class Offer(models.Model):
    product = models.OneToOneField(Products, related_name='offers', on_delete=models.CASCADE)
    OfferEuro = models.BigIntegerField(default=0)
    OfferDollar = models.BigIntegerField(default=0)
    OfferSterling = models.BigIntegerField(default=0)
    OfferDirham = models.BigIntegerField(default=0)
    OfferSAR = models.BigIntegerField(default=0)
    endDate = models.DateTimeField(auto_now=True)




class NewCollection(models.Model):
    product = models.OneToOneField(Products, on_delete=models.CASCADE)
    endDate=models.DateTimeField(auto_now=True)




class WishList(models.Model):
    user = models.ForeignKey(User,related_name='users', on_delete=models.CASCADE)
    product = models.ForeignKey(Products,related_name='users', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'product']


class cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    size = models.ForeignKey(Sizes,on_delete=models.CASCADE,null=True,blank=True)
    color = models.ForeignKey(Options,on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    is_placed=models.BooleanField(
        default=False,
        verbose_name='Cart Status'
    )

    class Meta:
        unique_together = ['user', 'product','size']


class Order(models.Model):
    product = models.ForeignKey(Products,related_name="orderedproducts", on_delete=models.CASCADE)
    selectedsize = models.ForeignKey(Sizes,related_name="orderedsize",on_delete=models.CASCADE,null=True,blank=True)
    selectedcolor = models.ForeignKey(Options,related_name="orderedcolor",on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.IntegerField()
    parentcart=models.ForeignKey(cart, on_delete=models.PROTECT,null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.PROTECT,null=True,blank=True)
    address = models.CharField(max_length=225,null=True,blank=True)
    city = models.CharField(max_length=225,null=True,blank=True)
    country = models.CharField(max_length=225,null=True,blank=True)
    pincode = models.CharField(max_length=225,null=True,blank=True)
    first_name = models.CharField(max_length=225,null=True,blank=True)
    last_name = models.CharField(max_length=225,null=True,blank=True)
    phone = models.CharField(max_length=225,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    stripe_payment_intent=models.CharField(
        max_length=200,null=True,blank=True
    )
    has_paid = models.BooleanField(
        default=False,
        verbose_name='Payment Status',null=True,blank=True
    )
    created_on = models.DateTimeField(
        auto_now_add=True,null=True,blank=True
    )

    updated_on = models.DateTimeField(
        auto_now_add=True,null=True,blank=True
    )
    status=models.CharField(max_length=50,default='Open',null=True,blank=True)
    amount = models.IntegerField(
        verbose_name='Amount'
    )
    currency=models.CharField(max_length=225,null=True,blank=True)



