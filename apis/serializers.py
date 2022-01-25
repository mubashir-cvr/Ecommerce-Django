

from gettext import NullTranslations
from optparse import Option
import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.utils import field_mapping
from .serializerhelper import *
from .models import Category, Offer,SubCategory,SubSubCategory,Products,Options,cart
from versatileimagefield.serializers import VersatileImageFieldSerializer
from django.forms.models import model_to_dict
from django.db.models import Count




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

class ColorSerializerforProduct(serializers.ModelSerializer):
    class Meta:
        model=Options
        fields = ('color',)


class SizeSerializerforProduct(serializers.ModelSerializer):
    class Meta:
        model=Sizes
        fields = ('size',)
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

    OfferEuro=serializers.SerializerMethodField()
    OfferPecentageEuro=serializers.SerializerMethodField()

    OfferDollar=serializers.SerializerMethodField()
    OfferPecentageDollar=serializers.SerializerMethodField()

    OfferSterling=serializers.SerializerMethodField()
    OfferPecentageSterling=serializers.SerializerMethodField()

    OfferDirham=serializers.SerializerMethodField()
    OfferPecentageDirham=serializers.SerializerMethodField()

    OfferSAR=serializers.SerializerMethodField()
    OfferPecentageSAR=serializers.SerializerMethodField()


    brand=BrandSerializerforProduct()
    image = VersatileImageFieldSerializer(
        sizes=[
            
            ('original', 'url'),
        ])
    class Meta:
        model = Products
        fields = ('id','name','image','brand',
            'productpriceEuro',
            'OfferEuro',
            'OfferPecentageEuro',
            'productpriceDollar',
            'OfferDollar',
            'OfferPecentageDollar',
            'productpriceSterling',
            'OfferSterling',
            'OfferPecentageSterling',
            'productpriceDirham',
            'OfferDirham',
            'OfferPecentageDirham',
            'productpriceSar',
            'OfferSAR',
            'OfferPecentageSAR',
            'options','created_date',
            )
    
    def get_OfferEuro(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            return offer.first().OfferEuro
        return 0
    def get_OfferPecentageEuro(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            euroOffPrice=offer.first().OfferEuro
            return CalculateOfferPercentage(euroOffPrice,obj.productpriceEuro)
        return 0
    def get_OfferDollar(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            return offer.first().OfferDollar
        return 0
    def get_OfferPecentageDollar(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            euroOffPrice=offer.first().OfferDollar
            return CalculateOfferPercentage(euroOffPrice,obj.productpriceEuro)
        return 0
    def get_OfferSterling(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            return offer.first().OfferSterling
        return 0
    def get_OfferPecentageSterling(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            euroOffPrice=offer.first().OfferSterling
            return CalculateOfferPercentage(euroOffPrice,obj.productpriceEuro)
        return 0
    def get_OfferDirham(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            return offer.first().OfferDirham
        return 0
    def get_OfferPecentageDirham(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            euroOffPrice=offer.first().OfferDirham
            return CalculateOfferPercentage(euroOffPrice,obj.productpriceEuro)
        return 0
    def get_OfferSAR(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            return offer.first().OfferSAR
        return 0
    def get_OfferPecentageSAR(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            euroOffPrice=offer.first().OfferSAR
            return CalculateOfferPercentage(euroOffPrice,obj.productpriceEuro)
        return 0
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
    OfferEuro=serializers.SerializerMethodField()
    OfferPecentageEuro=serializers.SerializerMethodField()

    OfferDollar=serializers.SerializerMethodField()
    OfferPecentageDollar=serializers.SerializerMethodField()

    OfferSterling=serializers.SerializerMethodField()
    OfferPecentageSterling=serializers.SerializerMethodField()

    OfferDirham=serializers.SerializerMethodField()
    OfferPecentageDirham=serializers.SerializerMethodField()

    OfferSAR=serializers.SerializerMethodField()
    OfferPecentageSAR=serializers.SerializerMethodField()

    brand=BrandSerializerforProduct()
    image = VersatileImageFieldSerializer(
        sizes=[
            
            ('original', 'url'),
        ])
    class Meta:
        model = Products
        fields = ('id','name','image','brand',
            'productpriceEuro',
            'OfferEuro',
            'OfferPecentageEuro',
            'productpriceDollar',
            'OfferDollar',
            'OfferPecentageDollar',
            'productpriceSterling',
            'OfferSterling',
            'OfferPecentageSterling',
            'productpriceDirham',
            'OfferDirham',
            'OfferPecentageDirham',
            'productpriceSar',
            'OfferSAR',
            'OfferPecentageSAR',
            'options','created_date')
    
    def get_OfferEuro(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            return offer.first().OfferEuro
        return 0
    def get_OfferPecentageEuro(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            euroOffPrice=offer.first().OfferEuro
            return CalculateOfferPercentage(euroOffPrice,obj.productpriceEuro)
        return 0
    def get_OfferDollar(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            return offer.first().OfferDollar
        return 0
    def get_OfferPecentageDollar(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            euroOffPrice=offer.first().OfferDollar
            return CalculateOfferPercentage(euroOffPrice,obj.productpriceEuro)
        return 0
    def get_OfferSterling(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            return offer.first().OfferSterling
        return 0
    def get_OfferPecentageSterling(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            euroOffPrice=offer.first().OfferSterling
            return CalculateOfferPercentage(euroOffPrice,obj.productpriceEuro)
        return 0
    def get_OfferDirham(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            return offer.first().OfferDirham
        return 0
    def get_OfferPecentageDirham(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            euroOffPrice=offer.first().OfferDirham
            return CalculateOfferPercentage(euroOffPrice,obj.productpriceEuro)
        return 0
    def get_OfferSAR(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            return offer.first().OfferSAR
        return 0
    def get_OfferPecentageSAR(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            euroOffPrice=offer.first().OfferSAR
            return CalculateOfferPercentage(euroOffPrice,obj.productpriceEuro)
        return 0

class SubSubcategorySerializer(serializers.HyperlinkedModelSerializer):
    products=productLessSerializer(many=True,read_only=True)
    availablebrands=serializers.SerializerMethodField()
    availabeColours=serializers.SerializerMethodField()
    availableSizes=serializers.SerializerMethodField()
    image = VersatileImageFieldSerializer(
        sizes=[
            
            ('original', 'url'),
        ])
    class Meta:
        model = SubSubCategory
        fields = ('id','url','name','image','products','availablebrands','availabeColours','availableSizes')
    def get_availablebrands(self,subsubcategory):
        products=Products.objects.filter(subsubcategory=subsubcategory)
        brands=Brand.objects.filter(products__in=products)
        serializer = BrandSerializerforProduct(brands,many=True)
        return serializer.data
    def get_availabeColours(self,subsubcategory):
        products=Products.objects.filter(subsubcategory=subsubcategory)
        if Options.objects.filter(product__in=products).exists():

            colors=Options.objects.filter(product__in=products).order_by('color').distinct('color')
            
            serializer = ColorSerializerforProduct(colors,many=True)
            return serializer.data
        return None
    def get_availableSizes(self,subsubcategory):
        products=Products.objects.filter(subsubcategory=subsubcategory)
        if products.exists():
            colors=Options.objects.filter(product__in=products)
            if colors.exists():

                sizes=Sizes.objects.filter(option__in=colors).order_by('size').distinct('size')
        
                serializer = SizeSerializerforProduct(sizes,many=True)
                return serializer.data
            return None
        return None
class SubSubcategoryLessoneSerializer(serializers.HyperlinkedModelSerializer):
    availablebrands=serializers.SerializerMethodField()
    availabeColours=serializers.SerializerMethodField()
    availableSizes=serializers.SerializerMethodField()
    image = VersatileImageFieldSerializer(
        sizes=[
            
            ('original', 'url'),
        ])
    class Meta:
        model = SubSubCategory
        fields = ('id','url','name','image','availablebrands','availabeColours','availableSizes')
    def get_availablebrands(self,subsubcategory):
        products=Products.objects.filter(subsubcategory=subsubcategory)
        brands=Brand.objects.filter(products__in=products)
        serializer = BrandSerializerforProduct(brands,many=True)
        return serializer.data
    def get_availabeColours(self,subsubcategory):
        products=Products.objects.filter(subsubcategory=subsubcategory)
        if Options.objects.filter(product__in=products).exists():

            colors=Options.objects.filter(product__in=products).order_by('color').distinct('color')
            
            serializer = ColorSerializerforProduct(colors,many=True)
            return serializer.data
        return None
    def get_availableSizes(self,subsubcategory):
        products=Products.objects.filter(subsubcategory=subsubcategory)
        if products.exists():
            colors=Options.objects.filter(product__in=products)
            if colors.exists():

                sizes=Sizes.objects.filter(option__in=colors).order_by('size').distinct('size')
        
                serializer = SizeSerializerforProduct(sizes,many=True)
                return serializer.data
            return None
        return None

class SubSubcategoryLessSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SubSubCategory
        fields = ('id','name')
    

class SubcategorySerializer(serializers.HyperlinkedModelSerializer):
    subsubcategories=SubSubcategoryLessoneSerializer(many=True,read_only=True)
    availablebrands=serializers.SerializerMethodField()
    availabeColours=serializers.SerializerMethodField()
    availableSizes=serializers.SerializerMethodField()
    image = VersatileImageFieldSerializer(
        sizes=[
            
            ('original', 'url'),
        ])
    class Meta:
        model = SubCategory
        fields = ('id','url','name','image','subsubcategories','availablebrands','availabeColours','availableSizes')
    def get_availablebrands(self,subcategory):
        subsubcategories=SubSubCategory.objects.filter(subcategory=subcategory)
        products=Products.objects.filter(subsubcategory__in=subsubcategories)
        brands=Brand.objects.filter(products__in=products)
        serializer = BrandSerializerforProduct(brands,many=True)
        return serializer.data
    
    def get_availabeColours(self,subcategory):
        subsubcategories=SubSubCategory.objects.filter(subcategory=subcategory)
        products=Products.objects.filter(subsubcategory__in=subsubcategories)
        if Options.objects.filter(product__in=products).exists():

            colors=Options.objects.filter(product__in=products).order_by('color').distinct('color')
            
            serializer = ColorSerializerforProduct(colors,many=True)
            return serializer.data
        return None
    def get_availableSizes(self,subcategory):
        subsubcategories=SubSubCategory.objects.filter(subcategory=subcategory)
        products=Products.objects.filter(subsubcategory__in=subsubcategories)
        if products.exists():
            colors=Options.objects.filter(product__in=products)
            if colors.exists():

                sizes=Sizes.objects.filter(option__in=colors).order_by('size').distinct('size')
        
                serializer = SizeSerializerforProduct(sizes,many=True)
                return serializer.data
            return None
        return None
    

class SubcategoryLessSerializer(serializers.HyperlinkedModelSerializer):
    
    subsubcategories=SubSubcategoryLessSerializer(many=True,read_only=True)
    availablebrands=serializers.SerializerMethodField()
    availabeColours=serializers.SerializerMethodField()
    availableSizes=serializers.SerializerMethodField()
    image = VersatileImageFieldSerializer(
        sizes=[
            ('original', 'url'),
        ])
    class Meta:
        model = SubCategory
        fields = ('id','url','name','image','subsubcategories','availablebrands','availabeColours','availableSizes')

    def get_availablebrands(self,subcategory):
        subsubcategories=SubSubCategory.objects.filter(subcategory=subcategory)
        products=Products.objects.filter(subsubcategory__in=subsubcategories)
        brands=Brand.objects.filter(products__in=products)
        serializer = BrandSerializerforProduct(brands,many=True)
        return serializer.data
    
    def get_availabeColours(self,subcategory):
        subsubcategories=SubSubCategory.objects.filter(subcategory=subcategory)
        products=Products.objects.filter(subsubcategory__in=subsubcategories)
        if Options.objects.filter(product__in=products).exists():

            colors=Options.objects.filter(product__in=products).order_by('color').distinct('color')
            
            serializer = ColorSerializerforProduct(colors,many=True)
            return serializer.data
        return None
    def get_availableSizes(self,subcategory):
        subsubcategories=SubSubCategory.objects.filter(subcategory=subcategory)
        products=Products.objects.filter(subsubcategory__in=subsubcategories)
        if products.exists():
            colors=Options.objects.filter(product__in=products)
            if colors.exists():

                sizes=Sizes.objects.filter(option__in=colors).order_by('size').distinct('size')
        
                serializer = SizeSerializerforProduct(sizes,many=True)
                return serializer.data
            return None
        return None

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
        read_only_fields = ('user','is_placed')    






class ProductSearchSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ('original', 'url'),
        ])
    class Meta:
        model = Products
        fields = ('id','name','image','subsubcategory')
    

class SubCategorySearchSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ('original', 'url'),
        ])
    class Meta:
        model = SubCategory
        fields = ('id','name','image','category')



class SubSubCategorySearchSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ('original', 'url'),
        ])
    class Meta:
        model = SubSubCategory
        fields = ('id','name','image','subcategory')
    
class CategorySearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name')



class GetCartSerializer(serializers.ModelSerializer):
    product = productSerializer(read_only=True)
    size = SizesSerializer(read_only=True)
    color = optionsSerializer(read_only=True)
    class Meta:
        model = cart
        fields = '__all__'




class CheckoutCartSerilizer(serializers.Serializer):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=225)
    city = models.CharField(max_length=225)
    country = models.CharField(max_length=225)
    pincode = models.CharField(max_length=225)
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    phone = models.CharField(max_length=225)
    email = models.EmailField(null=True,blank=True)


class optionsOrderSerializer(serializers.HyperlinkedModelSerializer):
    image_one = VersatileImageFieldSerializer(
        sizes=[
            
            ('original', 'url'),
        ])
    class Meta:
        model = Options
        fields = ('id','url','stock','image_one')
class productToOrderSerializer(serializers.HyperlinkedModelSerializer):

    OfferEuro=serializers.SerializerMethodField()
    OfferPecentageEuro=serializers.SerializerMethodField()

    OfferDollar=serializers.SerializerMethodField()
    OfferPecentageDollar=serializers.SerializerMethodField()

    OfferSterling=serializers.SerializerMethodField()
    OfferPecentageSterling=serializers.SerializerMethodField()

    OfferDirham=serializers.SerializerMethodField()
    OfferPecentageDirham=serializers.SerializerMethodField()

    OfferSAR=serializers.SerializerMethodField()
    OfferPecentageSAR=serializers.SerializerMethodField()


    brand=BrandSerializerforProduct()
    image = VersatileImageFieldSerializer(
        sizes=[
            
            ('original', 'url'),
        ])
    class Meta:
        model = Products
        fields = ('id','name','image','brand',
            'productpriceEuro',
            'OfferEuro',
            'OfferPecentageEuro',
            'productpriceDollar',
            'OfferDollar',
            'OfferPecentageDollar',
            'productpriceSterling',
            'OfferSterling',
            'OfferPecentageSterling',
            'productpriceDirham',
            'OfferDirham',
            'OfferPecentageDirham',
            'productpriceSar',
            'OfferSAR',
            'OfferPecentageSAR',
            'created_date',
            )
    
    def get_OfferEuro(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            return offer.first().OfferEuro
        return 0
    def get_OfferPecentageEuro(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            euroOffPrice=offer.first().OfferEuro
            return CalculateOfferPercentage(euroOffPrice,obj.productpriceEuro)
        return 0
    def get_OfferDollar(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            return offer.first().OfferDollar
        return 0
    def get_OfferPecentageDollar(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            euroOffPrice=offer.first().OfferDollar
            return CalculateOfferPercentage(euroOffPrice,obj.productpriceEuro)
        return 0
    def get_OfferSterling(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            return offer.first().OfferSterling
        return 0
    def get_OfferPecentageSterling(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            euroOffPrice=offer.first().OfferSterling
            return CalculateOfferPercentage(euroOffPrice,obj.productpriceEuro)
        return 0
    def get_OfferDirham(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            return offer.first().OfferDirham
        return 0
    def get_OfferPecentageDirham(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            euroOffPrice=offer.first().OfferDirham
            return CalculateOfferPercentage(euroOffPrice,obj.productpriceEuro)
        return 0
    def get_OfferSAR(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            return offer.first().OfferSAR
        return 0
    def get_OfferPecentageSAR(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            euroOffPrice=offer.first().OfferSAR
            return CalculateOfferPercentage(euroOffPrice,obj.productpriceEuro)
        return 0

class OrdersSerializer(serializers.ModelSerializer):
    product=productToOrderSerializer()
    selectedsize=SizesSerializer()
    selectedcolor=optionsOrderSerializer()
    class Meta:
        model = Order
        fields ='__all__' 
