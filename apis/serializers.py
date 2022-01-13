import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.utils import field_mapping
from .serializerhelper import *
from .models import Category, Offer,SubCategory,SubSubCategory,Products,Options,cart
from versatileimagefield.serializers import VersatileImageFieldSerializer
from django.forms.models import model_to_dict





class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('id','name','email','password')
        read_only_fields = ('id',)
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)


class GetUserSerailizer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    class Meta:
        model = get_user_model()
        fields = ('id','name','address')
        read_only_fields = ('address',)

    def get_address(self,obj):
        if AddressesOfUser.objects.filter(user=obj).exists():
            queryset = AddressesOfUser.objects.filter(user = obj.id)
            serializer = AddressesOfUserSerializer(queryset,many=True)
            return serializer.data
        else:
            return False


class BrandSerializerforProduct(serializers.ModelSerializer):
    class Meta:
        model=Brand
        fields = ('id','name','is_popular')
class SizesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sizes
        fields = ('id','stock','size')
class optionsSerializer(serializers.HyperlinkedModelSerializer):
    sizes=SizesSerializer(many=True,read_only=True)
    image_one = VersatileImageFieldSerializer(
        sizes=[
            
            ('original', 'url'),
        ])
    image_two = VersatileImageFieldSerializer(
        sizes=[
            
            ('original', 'url'),
        ])
    image_three = VersatileImageFieldSerializer(
        sizes=[
            
            ('original', 'url'),
        ])
    class Meta:
        model = Options
        fields = ('id','url','color','colorhash','stock','image_one','image_two','image_three','sizes')
class productSerializer(serializers.HyperlinkedModelSerializer):
    options=optionsSerializer(many=True,read_only=True)
    offerPrice=serializers.SerializerMethodField()
    offerPercentage=serializers.SerializerMethodField()
    brand=BrandSerializerforProduct()
    image = VersatileImageFieldSerializer(
        sizes=[
            
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

class optionsLessSerializer(serializers.HyperlinkedModelSerializer):
    sizes=SizesSerializer(many=True,read_only=True)
    image_one = VersatileImageFieldSerializer(
        sizes=[
            
            ('original', 'url'),
        ])
    class Meta:
        model = Options
        fields = ('id','url','stock','image_one','sizes')
class productLessSerializer(serializers.HyperlinkedModelSerializer):
    options=optionsLessSerializer(many=True,read_only=True)
    offerPrice=serializers.SerializerMethodField()
    offerPercentage=serializers.SerializerMethodField()
    brand=BrandSerializerforProduct()
    image = VersatileImageFieldSerializer(
        sizes=[
            
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
    products=productLessSerializer(many=True,read_only=True)
    availablebrands=serializers.SerializerMethodField()
    image = VersatileImageFieldSerializer(
        sizes=[
            
            ('original', 'url'),
        ])
    class Meta:
        model = SubSubCategory
        fields = ('id','url','name','image','products','availablebrands')
    def get_availablebrands(self,subsubcategory):
        products=Products.objects.filter(subsubcategory=subsubcategory)
        brands=Brand.objects.filter(products__in=products)
        serializer = BrandSerializerforProduct(brands,many=True)
        return serializer.data
class SubSubcategoryLessoneSerializer(serializers.HyperlinkedModelSerializer):
    availablebrands=serializers.SerializerMethodField()
    image = VersatileImageFieldSerializer(
        sizes=[
            
            ('original', 'url'),
        ])
    class Meta:
        model = SubSubCategory
        fields = ('id','url','name','image','availablebrands')
    def get_availablebrands(self,subsubcategory):
        products=Products.objects.filter(subsubcategory=subsubcategory)
        brands=Brand.objects.filter(products__in=products)
        serializer = BrandSerializerforProduct(brands,many=True)
        return serializer.data
class SubSubcategoryLessSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SubSubCategory
        fields = ('id','name')
    

class SubcategorySerializer(serializers.HyperlinkedModelSerializer):
    subsubcategories=SubSubcategoryLessoneSerializer(many=True,read_only=True)
    availablebrands=serializers.SerializerMethodField()
    image = VersatileImageFieldSerializer(
        sizes=[
            
            ('original', 'url'),
        ])
    class Meta:
        model = SubCategory
        fields = ('id','url','name','availablebrands','image','subsubcategories')
    def get_availablebrands(self,subcategory):
        subsubcategories=SubSubCategory.objects.filter(subcategory=subcategory)
        products=Products.objects.filter(subsubcategory__in=subsubcategories)
        brands=Brand.objects.filter(products__in=products)
        serializer = BrandSerializerforProduct(brands,many=True)
        return serializer.data

class SubcategoryLessSerializer(serializers.HyperlinkedModelSerializer):
    
    subsubcategories=SubSubcategoryLessSerializer(many=True,read_only=True)
    image = VersatileImageFieldSerializer(
        sizes=[
            ('original', 'url'),
        ])
    class Meta:
        model = SubCategory
        fields = ('id','url','name','image','subsubcategories')

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    subcategories=SubcategoryLessSerializer(many=True,read_only=True)
    class Meta:
        model = Category
        fields = ('url', 'id', 'name','subcategories')



class BrandSerializer(serializers.HyperlinkedModelSerializer):
    products=productSerializer(many=True,read_only=True)
    class Meta:
        model=Brand
        fields = ('id','url','name','products')
    

class WishListSerializer(serializers.HyperlinkedModelSerializer):
    product=productSerializer()
    user=UserSerializer(read_only=True)
    class Meta:
        model = WishList
        fields = ('id','user','product','date')


class WishListPostSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = WishList
        fields = ('id','user','product','date')

class AddressesOfUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressesOfUser
        fields = '__all__'
        read_only_fields = ('user',)

class GetAddressesOfUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = AddressesOfUser
        fields = '__all__'
        read_only_fields = ('user',)


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = cart
        fields = '__all__'
        read_only_fields = ('user',)    

class GetCartSerializer(serializers.ModelSerializer):
    product = productSerializer(read_only=True)
    size = SizesSerializer(read_only=True)
    color = optionsSerializer(read_only=True)
    class Meta:
        model = cart
        fields = '__all__'