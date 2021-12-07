from rest_framework import serializers
  
# import model from models.py
from .models import Category,SubCategory,SubSubCategory,Products,Options


class optionsSerializer(serializers.HyperlinkedModelSerializer):
     class Meta:
        model = Options
        fields = ('id','url','color','size')
class productSerializer(serializers.HyperlinkedModelSerializer):
    options=optionsSerializer(many=True,read_only=True)
    class Meta:
        model = Products
        fields = ('id','url', 'name','image','options')


class SubSubcategorySerializer(serializers.HyperlinkedModelSerializer):
    # specify model and fields
    products=productSerializer(many=True,read_only=True)
    class Meta:
        model = SubSubCategory
        fields = ('id','url', 'name','image','products')

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


