from rest_framework import serializers
from apis.serializerhelper import *
from django.contrib.auth import get_user_model
from apis.models import Category, Offer,SubCategory,SubSubCategory,Products,Options
from versatileimagefield.serializers import VersatileImageFieldSerializer




class AdminSizesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sizes
        fields = ('id','stock','size',"option")
class AdminoptionsSerializer(serializers.ModelSerializer):
    sizes=AdminSizesSerializer(many=True,read_only=True)
    image_one = VersatileImageFieldSerializer(
        sizes=[
            ('medium_square_crop', 'crop__400x400'),
            ('extrsmall_square_crop', 'crop__50x50'),
            ('medium_rectangle_crop', 'crop__400x600'),
            ('original', 'url'),
        ])
    image_two = VersatileImageFieldSerializer(
        sizes=[
            ('medium_square_crop', 'crop__400x400'),
            ('extrsmall_square_crop', 'crop__50x50'),
            ('medium_rectangle_crop', 'crop__400x600'),
            ('original', 'url'),
        ])
    image_three = VersatileImageFieldSerializer(
        sizes=[
            ('medium_square_crop', 'crop__400x400'),
            ('extrsmall_square_crop', 'crop__50x50'),
            ('medium_rectangle_crop', 'crop__400x600'),
            ('original', 'url'),
        ])
    class Meta:
        model = Options
        fields = '__all__'
class AdminproductSerializer(serializers.ModelSerializer):
    offerPrice=serializers.SerializerMethodField()
    offerPercentage=serializers.SerializerMethodField()
    options=AdminoptionsSerializer(many=True,read_only=True)
    image = VersatileImageFieldSerializer(
        sizes=[
            ('medium_square_crop', 'crop__400x400'),
            ('extrsmall_square_crop', 'crop__50x50'),
            ('medium_rectangle_crop', 'crop__400x600'),
            ('original', 'url'),
        ])
    def get_offerPrice(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            return offer.first().offerPrice
        return 0
    def get_offerPercentage(self, obj):
        product=obj
        return CalculateOfferPercentage(product)
    class Meta:
        model = Products
        fields = ('id','name','image','price','offerPrice','offerPercentage','options','created_date','order','subsubcategory')



class AdminSubSubcategorySerializer(serializers.ModelSerializer):
    products=AdminproductSerializer(many=True,read_only=True)
    image = VersatileImageFieldSerializer(
        sizes=[
            ('medium_square_crop', 'crop__400x400'),
            ('extrsmall_square_crop', 'crop__50x50'),
            ('medium_rectangle_crop', 'crop__400x600'),
            ('original', 'url'),
        ])
    class Meta:
        model = SubSubCategory
        fields = '__all__'

class AdminSubcategorySerializer(serializers.ModelSerializer):
    subsubcategories=AdminSubSubcategorySerializer(many=True,read_only=True)
    image = VersatileImageFieldSerializer(
        sizes=[
            ('medium_square_crop', 'crop__400x400'),
            ('extrsmall_square_crop', 'crop__50x50'),
            ('medium_rectangle_crop', 'crop__400x600'),
            ('original', 'url'),
        ])
    class Meta:
        model = SubCategory
        fields = '__all__'


class AdminCategorySerializer(serializers.ModelSerializer):
    subcategories=AdminSubcategorySerializer(many=True,read_only=True)
    class Meta:
        model = Category
        fields = '__all__'



class AdminBrandSerializer(serializers.HyperlinkedModelSerializer):
    products=AdminproductSerializer(many=True,read_only=True)
    class Meta:
        model=Brand
        fields = ('id','url','name','products')


    


class AdminAddOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields ='__all__'