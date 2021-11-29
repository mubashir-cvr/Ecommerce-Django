from rest_framework import serializers
  
# import model from models.py
from .models import Category,SubCategory,SubSubCategory



class SubSubcategorySerializer(serializers.HyperlinkedModelSerializer):
    # specify model and fields
    class Meta:
        model = SubSubCategory
        fields = ('id','url', 'name','image')

class SubcategorySerializer(serializers.HyperlinkedModelSerializer):
    # specify model and fields
    subsubcategories=SubSubcategorySerializer(many=True,read_only=True)
    class Meta:
        model = SubCategory
        fields = ('url', 'name','image','subsubcategories')

# Create a model serializer 
class CategorySerializer(serializers.HyperlinkedModelSerializer):
    # specify model and fields
    subcategories=SubcategorySerializer(many=True,read_only=True)
    class Meta:
        model = Category
        fields = ('url', 'id', 'name','subcategories')


