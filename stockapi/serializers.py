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
    
    offerID=serializers.SerializerMethodField()

    options=AdminoptionsSerializer(many=True,read_only=True)
    image = VersatileImageFieldSerializer(
        sizes=[
            ('medium_square_crop', 'crop__400x400'),
            ('extrsmall_square_crop', 'crop__50x50'),
            ('medium_rectangle_crop', 'crop__400x600'),
            ('original', 'url'),
        ])
    

    class Meta:
        model = Products
        fields = ('id','name','image',
        'offerID',
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
        'options',
        'created_date',
        'order',
        'subsubcategory',
        'brand',
        
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
    
    def get_offerID(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            return offer.first().id
        return 0
   

class AdminNewCollectionSerializer(serializers.ModelSerializer):
    product =AdminproductSerializer()

    class Meta:
        model = NewCollection
        fields ='__all__' 

class AdminNewCollectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewCollection
        fields ='__all__' 
class AdminTrendingProductSerializer(serializers.ModelSerializer):
    product =AdminproductSerializer()

    class Meta:
        model = BottomProductDisplay
        fields ='__all__' 

class AdminTrendingProductCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BottomProductDisplay
        fields ='__all__' 
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
    class Meta:
        model=Brand
        fields = ('id','url','name','is_popular')



class AdminproductOrderSerializer(serializers.ModelSerializer):
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
    
    offerID=serializers.SerializerMethodField()

    image = VersatileImageFieldSerializer(
        sizes=[
            ('medium_square_crop', 'crop__400x400'),
            ('extrsmall_square_crop', 'crop__50x50'),
            ('medium_rectangle_crop', 'crop__400x600'),
            ('original', 'url'),
        ])
    

    class Meta:
        model = Products
        fields = ('id','name','image',
        'offerID',
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
        'order',
        'subsubcategory',
        'brand',
        
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
    
    def get_offerID(self, obj):
        offer=Offer.objects.filter(product=obj)
        if offer.exists():
            return offer.first().id
        return 0
   



class AdminAddOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields ='__all__' 

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields ='__all__' 
    
class OrderListSerializer(serializers.ModelSerializer):
    product=AdminproductOrderSerializer()
    selectedsize=AdminSizesSerializer()
    selectedcolor=AdminoptionsSerializer()
    class Meta:
        model = Order
        fields ='__all__' 
    


class ProductsNameIdserializer(serializers.ModelSerializer):
    class Meta:
        model=Products
        fields=('id','name')