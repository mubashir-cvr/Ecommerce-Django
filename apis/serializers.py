from rest_framework import serializers
from django.contrib.auth import get_user_model
  
# import model from models.py
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


class optionsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Options
        fields = ('id','url','color','size','product')
class productSerializer(serializers.HyperlinkedModelSerializer):
    options=optionsSerializer(many=True,read_only=True)
    offerPrice=serializers.SerializerMethodField()
    offerPercentage=serializers.SerializerMethodField()
    class Meta:
        model = Products
        fields = ('id','url', 'subsubcategory','name','image','price','offerPrice','offerPercentage','options')
    
    def get_offerPrice(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            return offer.first().offerPrice
        return 0
    def get_offerPercentage(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            offPrice=obj.price-offer.first().offerPrice
            percentage=offPrice*100/obj.price
            return str(int(percentage))+'%'
        return 0

class SubSubcategorySerializer(serializers.HyperlinkedModelSerializer):
    # specify model and fields
    products=productSerializer(many=True,read_only=True)
    class Meta:
        model = SubSubCategory
        fields = ('id','url','subcategory','name','image','products')

class SubcategorySerializer(serializers.HyperlinkedModelSerializer):
    # specify model and fields
    subsubcategories=SubSubcategorySerializer(many=True,read_only=True)
    image = VersatileImageFieldSerializer(
        sizes=[
            ('medium_square_crop', 'crop__400x600'),
        ])
    class Meta:
        model = SubCategory
        fields = ('url','category','name','image','subsubcategories')

# Create a model serializer 
class CategorySerializer(serializers.HyperlinkedModelSerializer):
    # specify model and fields
    subcategories=SubcategorySerializer(many=True,read_only=True)
    class Meta:
        model = Category
        fields = ('url', 'id', 'name','subcategories')


