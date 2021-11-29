
from django.db import models
  
class Category(models.Model):
    name=models.CharField(max_length = 200)
    title = models.CharField(max_length = 200)
    description = models.TextField()
  
    def __str__(self):
        return self.title


class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    order=models.IntegerField()
    image=models.CharField(max_length=100)  # char field for test
    name=name=models.CharField(max_length = 200)

    class Meta:
        unique_together = ['category', 'order']
        ordering = ['order']


class SubSubCategory(models.Model):
    subcategory = models.ForeignKey(SubCategory, related_name='subsubcategories', on_delete=models.CASCADE)
    order=models.IntegerField()
    image=models.CharField(max_length=100)  # char field for test
    name=name=models.CharField(max_length = 200)

    class Meta:
        unique_together = ['subcategory', 'order']
        ordering = ['order']

