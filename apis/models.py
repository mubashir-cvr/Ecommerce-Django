
from django.db import models
  
class Category(models.Model):
    name=models.CharField(max_length = 200)
    title = models.CharField(max_length = 200)
    description = models.TextField()
  
    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    order=models.IntegerField()
    image=models.CharField(max_length=100)  # char field for test
    name=name=models.CharField(max_length = 200)

    def __str__(self):
        return self.name
    class Meta:
        unique_together = ['category', 'order']
        ordering = ['order']


class SubSubCategory(models.Model):
    subcategory = models.ForeignKey(SubCategory, related_name='subsubcategories', on_delete=models.CASCADE)
    order=models.IntegerField()
    image=models.CharField(max_length=100)  # char field for test
    name=name=models.CharField(max_length = 200)
    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['subcategory', 'order']
        ordering = ['order']




class Products(models.Model):
    subsubcategory = models.ForeignKey(SubSubCategory, related_name='products', on_delete=models.CASCADE)
    order=models.IntegerField()
    image=models.CharField(max_length=100)  # char field for test
    name=models.CharField(max_length = 200)
    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['subsubcategory', 'order']
        ordering = ['order']


class Options(models.Model):
    product = models.ForeignKey(Products, related_name='options', on_delete=models.CASCADE)
    order=models.IntegerField()
    image=models.CharField(max_length=100)  # char field for test
    color=models.CharField(max_length = 200)
    size=models.CharField(max_length = 200,null=True,blank=True)
    def __str__(self):
        return self.color

    class Meta:
        ordering = ['order']


