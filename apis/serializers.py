from rest_framework import serializers
from django.contrib.auth import get_user_model
from .serializerhelper import *
from .models import Category, Offer,SubCategory,SubSubCategory,Products,Options
from versatileimagefield.serializers import VersatileImageFieldSerializer





class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('id','email','password')
        read_only_fields = ('id',)
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)



class BrandSerializerforProduct(serializers.ModelSerializer):
    class Meta:
        model=Brand
        fields = ('id','name')
class SizesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sizes
        fields = ('id','url','stock','size')
class optionsSerializer(serializers.HyperlinkedModelSerializer):
    sizes=SizesSerializer(many=True,read_only=True)
    image_one = VersatileImageFieldSerializer(
        sizes=[
            ('medium_square_crop', 'crop__400x400'),
            ('medium_rectangle_crop', 'crop__400x600'),
            ('original', 'url'),
        ])
    class Meta:
        model = Options
        fields = ('id','url','color','stock','image_one','sizes')
class productSerializer(serializers.HyperlinkedModelSerializer):
    options=optionsSerializer(many=True,read_only=True)
    offerPrice=serializers.SerializerMethodField()
    offerPercentage=serializers.SerializerMethodField()
    brand=BrandSerializerforProduct()
    image = VersatileImageFieldSerializer(
        sizes=[
            ('medium_square_crop', 'crop__400x400'),
            ('medium_rectangle_crop', 'crop__400x600'),
            ('original', 'url'),
        ])
    class Meta:
        model = Products
        fields = ('id','name','image','brand','price','offerPrice','offerPercentage','options','created_date')
    
    def get_offerPrice(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            return offer.first().offerPrice
        return 0
    def get_offerPercentage(self, obj):
        product=obj
        return CalculateOfferPercentage(product)

class SubSubcategorySerializer(serializers.HyperlinkedModelSerializer):
    products=productSerializer(many=True,read_only=True)
    image = VersatileImageFieldSerializer(
        sizes=[
            ('medium_square_crop', 'crop__400x400'),
            ('medium_rectangle_crop', 'crop__400x600'),
            ('original', 'url'),
        ])
    class Meta:
        model = SubSubCategory
        fields = ('id','url','name','image','products')

class SubcategorySerializer(serializers.HyperlinkedModelSerializer):
    subsubcategories=SubSubcategorySerializer(many=True,read_only=True)
    image = VersatileImageFieldSerializer(
        sizes=[
            ('medium_square_crop', 'crop__400x400'),
            ('medium_rectangle_crop', 'crop__400x600'),
            ('original', 'url'),
        ])
    class Meta:
        model = SubCategory
        fields = ('id','url','name','image','subsubcategories')
class CategorySerializer(serializers.HyperlinkedModelSerializer):
    subcategories=SubcategorySerializer(many=True,read_only=True)
    class Meta:
        model = Category
        fields = ('url', 'id', 'name','subcategories')



class BrandSerializer(serializers.HyperlinkedModelSerializer):
    products=productSerializer(many=True,read_only=True)
    class Meta:
        model=Brand
        fields = ('id','url','name','products')