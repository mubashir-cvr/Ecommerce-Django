
from asgiref.sync import sync_to_async
import json
from locale import currency
from unicodedata import category
from rest_framework import viewsets,generics
from rest_framework.views import APIView
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
import re
from django.http.response import HttpResponseNotFound, JsonResponse
from django.conf import settings
import stripe
from django.urls import reverse
from django.http import response
from rest_framework import viewsets,generics
from rest_framework import views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.utils import serializer_helpers
from rest_framework.views import APIView
from .pagination import *
from .serializers import * 
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status

from .models import Category, SubCategory,SubSubCategory,Options,Products,NewCollection,cart
from datetime import datetime,timedelta






class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


# create a viewset
class CategoryViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    # define queryset
    queryset = Category.objects.all()
    # specify serializer to be used
    
    serializer_class = CategorySerializer


class SubcategoryViewset(viewsets.ModelViewSet):
    # define queryset
    queryset = SubCategory.objects.all()
    # specify serializer to be used
    serializer_class = SubcategorySerializer


class SubSubcategoryViewset(viewsets.ModelViewSet):
    # define queryset
    queryset = SubSubCategory.objects.all()
    # specify serializer to bce used
    serializer_class = SubSubcategorySerializer


class SubSubcategoryAPIView(APIView):
    def get(self, request, format=None):
        if self.request.query_params.get('filter'):
            key=self.request.query_params.get('filter')
            filterIDs=json.loads(key)
            
            filterProducts=Products.objects.filter(subsubcategory__id__in=filterIDs)
            filterProductsSerilizer=productSerializer(filterProducts,many=True,context={"request": request})
            brandnames=[]
            colors=[]
            sizes=[]
            for product in filterProducts:
                if product.brand:
                    data={"id":product.brand.id,"name":product.brand.name}
                    if not data in brandnames:
                        brandnames.append(data)
                if Options.objects.filter(product=product).exists():
                    options=Options.objects.filter(product=product)
                    for option in options:
                        data={"color":option.color,"colorhash":option.colorhash}
                        if not data in colors:
                            colors.append(data)
                        if Sizes.objects.filter(option=option).exists():
                            sizeses=Sizes.objects.filter(option=option)
                            for size in sizeses:
                                data={"size":size.size}
                                if not data in sizes:
                                    sizes.append(data)
                
            data={
                "products":filterProductsSerilizer.data,
                "availablebrands":brandnames,
                "availabeColours":colors,
                "availableSizes":sizes

            }
            
            return Response(data)
        subsubcategories=SubSubCategory.objects.all()
        serializer=SubSubcategorySerializer(subsubcategories,many=True,context={'request': request})
        return Response(serializer.data)
        
        
        
    

class SubSubcategoryDetailAPIView(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return SubSubCategory.objects.get(pk=pk)
        except SubSubCategory.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        subsubcategory = self.get_object(pk)
        serializer = SubSubcategorySerializer(subsubcategory,context={'request': request})
        return Response(serializer.data)
    

class OptionsViewset(viewsets.ModelViewSet):
    # define queryset
    queryset = Options.objects.all()
    # specify serializer to bce used
    serializer_class = optionsSerializer


class NewArrivalViewset(APIView):
    def get(self, request, format=None):
        
        newCollection=NewCollection.objects.all()
        productsIDs=[]
        for new in newCollection:
            productsIDs.append(new.product.id)

        offerProducts=Products.objects.filter(id__in=productsIDs)
        offerProductsSerilizer=productSerializer(offerProducts,many=True,context={"request": request})
        brandnames=[]
        colors=[]
        sizes=[]
        for product in offerProducts:
            if product.brand:
                data={"id":product.brand.id,"name":product.brand.name}
                if not data in brandnames:
                    brandnames.append(data)
            if Options.objects.filter(product=product).exists():
                options=Options.objects.filter(product=product)
                for option in options:
                    data={"color":option.color,"colorhash":option.colorhash}
                    if not data in colors:
                        colors.append(data)
                    if Sizes.objects.filter(option=option).exists():
                        sizeses=Sizes.objects.filter(option=option)
                        for size in sizeses:
                            data={"size":size.size}
                            if not data in sizes:
                                sizes.append(data)
            
        searchdata={
            "products":offerProductsSerilizer.data,
            "availablebrands":brandnames,
            "availabeColours":colors,
            "availableSizes":sizes

        }
        
        return Response(searchdata)



class NewCollectionViewset(viewsets.ModelViewSet):
    # define queryset
    
    queryset = Products.objects.all()
    # specify serializer to bce used
    serializer_class = productSerializer
    def get_queryset(self):
        productIds=[]
        if NewCollection.objects.filter().exists():
            newcollection=NewCollection.objects.all()
            for new in newcollection:
                productIds.append(new.product_id)
        return self.queryset.filter(id__in=productIds)
class ProductsViewset(viewsets.ModelViewSet):
    # define queryset
    
    queryset = Products.objects.all()
    # specify serializer to bce used
    serializer_class = productSerializer

class BrandViewSet(viewsets.ModelViewSet):
    # define queryset
    queryset = Brand.objects.all()
    # specify serializer to be used
    
    serializer_class = BrandSerializer

class SizeViewSet(viewsets.ModelViewSet):
    # define queryset
    queryset = Sizes.objects.all()
    # specify serializer to be used
    
    serializer_class = SizesSerializer

class WhishListViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    # define queryset
    queryset = WishList.objects.all()
    # specify serializer to be used
    
    serializer_class = WishListSerializer

    def get_serializer_class(self):
        if self.action=="create":
            return WishListPostSerializer
        return self.serializer_class

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    

    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

class OffersaleViewset(APIView):
    def get(self, request, format=None):
        
        offerProducts=Products.objects.filter(offers__OfferEuro__gt=0)
        offerProductsSerilizer=productSerializer(offerProducts,many=True,context={"request": request})
        brandnames=[]
        colors=[]
        sizes=[]
        for product in offerProducts:
            if product.brand:
                data={"id":product.brand.id,"name":product.brand.name}
                if not data in brandnames:
                    brandnames.append(data)
            if Options.objects.filter(product=product).exists():
                options=Options.objects.filter(product=product)
                for option in options:
                    data={"color":option.color,"colorhash":option.colorhash}
                    if not data in colors:
                        colors.append(data)
                    if Sizes.objects.filter(option=option).exists():
                        sizeses=Sizes.objects.filter(option=option)
                        for size in sizeses:
                            data={"size":size.size}
                            if not data in sizes:
                                sizes.append(data)
            
        searchdata={
            "products":offerProductsSerilizer.data,
            "availablebrands":brandnames,
            "availabeColours":colors,
            "availableSizes":sizes

        }
        
        return Response(searchdata)




class AddressesViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    # define queryset
    queryset = AddressesOfUser.objects.all()
    
    # specify serializer to be used
    
    serializer_class = AddressesOfUserSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)


class CartViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = cart.objects.all()
    serializer_class = CartSerializer
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user,is_placed=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return GetCartSerializer
        if self.action == 'retrieve':
            return GetCartSerializer

        return CartSerializer



#     def perform_create(self,serializer):
#         serializer.save(user=self.request.user)


class SearchView(APIView):
    """Create a new user in the system"""
    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        searchdata=[]
        if self.request.query_params.get('key'):
            key=self.request.query_params.get('key')
            secondKey=' '+key

            products=Products.objects.filter(Q(name__startswith=key.upper())|Q(name__startswith=key.lower))
            if not products.exists():
                products=Products.objects.filter(Q(name__icontains=secondKey.upper())|Q(name__icontains=secondKey.lower()))
            if not products.exists():
                if key != 'MEN' or 'men':
                    products=Products.objects.filter(Q(name__icontains=key.upper())|Q(name__icontains=key.lower()))
            if not products.exists():
                subsubcategoryIDs=[]
                subcategories=SubCategory.objects.filter(Q(name__startswith=key.upper())|Q(name__startswith=key.lower()))
                if not subcategories.exists:
                    subcategories=SubCategory.objects.filter(Q(name__icontains=secondKey.upper())|Q(name__icontains=secondKey.lower()))
                if not subcategories.exists:
                    subcategories=SubCategory.objects.filter(Q(name__icontains=key.upper())|Q(name__icontains=key.lower()))
                if subcategories.exists():
                    for subcategory in subcategories:
                        subsubcategories=SubSubCategory.objects.filter(subcategory=subcategory)
                        if subsubcategories.exists():
                            for subsubcategory in subsubcategories:
                                subsubcategoryIDs.append(subsubcategory.id)
                products=Products.objects.filter(subsubcategory__id__in=subsubcategoryIDs)
                                
            if not products.exists():
                subsubcategories=SubSubCategory.objects.filter(Q(name__startswith=key.upper())|Q(name__startswith=key.lower()))
                if not subsubcategories.exists():
                    subsubcategories=SubSubCategory.objects.filter(Q(name__icontains=secondKey.upper())|Q(name__icontains=secondKey.lower()))
                if not subsubcategories.exists():
                    subsubcategories=SubSubCategory.objects.filter(Q(name__icontains=key.upper())|Q(name__icontains=key.lower()))
                
                subsubcategoryIDs=[]
                if subsubcategories.exists():
                    for subsubcategory in subsubcategories:
                        subsubcategoryIDs.append(subsubcategory.id)
                
                products=Products.objects.filter(subsubcategory__id__in=subsubcategoryIDs)


                    
            # categories=Category.objects.filter(name__startswith=key)
            if products.exists():
                brandnames=[]
                colors=[]
                sizes=[]
                for product in products:
                    if product.brand:
                        data={"id":product.brand.id,"name":product.brand.name}
                        if not data in brandnames:
                            brandnames.append(data)
                    if Options.objects.filter(product=product).exists():
                        options=Options.objects.filter(product=product)
                        for option in options:
                            data={"color":option.color}
                            if not data in colors:
                                colors.append(data)
                            if Sizes.objects.filter(option=option).exists():
                                sizeses=Sizes.objects.filter(option=option)
                                for size in sizeses:
                                    data={"size":size.size}
                                    if not data in sizes:
                                        sizes.append(data)
            

            productserializer = productLessSerializer(products,many=True,context={"request": request})
            # subcategoryserializer = SubCategorySearchSerializer(subcategories,many=True,context={"request": request})
            # categoryserializer = CategorySearchSerializer(categories,many=True,context={"request": request})
            # subSubcategorySerializer = SubSubCategorySearchSerializer(subsubcategories,many=True,context={"request": request})
            searchdata={
            "products":productserializer.data,
            "availablebrands":brandnames,
            "availabeColours":colors,
            "availableSizes":sizes
            }
            
        return Response(searchdata)

class UserDetails(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = GetUserSerailizer
    queryset = get_user_model().objects.all()

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)

class CheckoutCart(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        cartitems=cart.objects.filter(is_placed=False,user=self.request.user)
        
        if not cartitems.exists():
            raise Http404
        print("Cart Item Exist")
        itemsPriceDetails=[]
        try :
            address=request.data['address']
            email=request.data['email']
            city=request.data['city']
            pincode=request.data['pincode']
            country=request.data['country']
            firstName=request.data['firstName']
            lastName=request.data['lastName']
            phone=request.data['phone']
            currency=request.data['currency']
            print("Data Good")
        except:
            print("Data Fail")
            pass
        for item in cartitems:
            unitprice=0
            print("Collecting  Data..........")
            
            if Offer.objects.filter(product=item.product).exists():
                print("Collecting Offer Data..........")
                if currency=='USD':
                    unitprice= Offer.objects.get(product=item.product).OfferEuro*100
                elif currency=='SAR':
                    unitprice= Offer.objects.get(product=item.product).OfferSAR*100
                elif currency=='GBP':
                    unitprice= Offer.objects.get(product=item.product).OfferSterling*100
                elif currency=='EUR':
                    unitprice= Offer.objects.get(product=item.product).OfferEuro*100
                elif currency=='AED':
                    unitprice= Offer.objects.get(product=item.product).OfferDirham*100
                else:
                    pass
            else:
                print("Collecting Normal Data..........")
                if currency=='USD':
                    unitprice= item.product.productpriceDollar*100
                elif currency=='SAR':
                    unitprice= item.product.productpriceSar*100
                elif currency=='GBP':
                    unitprice= item.product.productpriceSterling*100
                elif currency=='EUR':
                    unitprice= item.product.productpriceEuro*100
                elif currency=='AED':
                    unitprice= item.product.productpriceDirham*100
            pricedict= {
                    'price_data': {
                        'currency': currency,
                        'product_data': {
                        'name': item.product.name,
                        },
                        'unit_amount': unitprice,
                    },
                    'quantity': item.quantity,
                }
            itemsPriceDetails.append(pricedict)
        print(itemsPriceDetails)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        checkout_session = stripe.checkout.Session.create(
            customer_email = request.data['email'],
            payment_method_types=['card'],
                shipping_options=[],
                            
            line_items=itemsPriceDetails,
            mode='payment',
            success_url=request.build_absolute_uri(
                reverse('success')
            ) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse('failed')),)
        
        for item in cartitems:
            order=Order()
            order.product=item.product
            order.quantity=item.quantity
            order.parentcart=item
            if item.size:
                order.selectedsize=item.size
            if item.color:
                order.selectedcolor=item.color
            order.address=address
            order.city=city
            order.country=country
            order.firstName=firstName
            order.phone=phone
            order.email=email
            order.pincode=pincode
            order.lastName=lastName
            order.stripe_payment_intent=checkout_session['payment_intent']
            order.amount=unitprice*item.quantity
            order.currency=currency
            order.user=self.request.user
            order.status="Attempted"
            order.save()
        return JsonResponse({'sessionId': checkout_session.id,'url':checkout_session.url})
         
class PayementView(APIView):
       permission_classes = (IsAuthenticated,)
       def get(self, request, format=None):
           pass
       def post(self, request, format=None):
            color=0
            size=0
            address=request.data['address']
            email=request.data['email']
            city=request.data['city']
            pincode=request.data['pincode']
            country=request.data['country']
            firstName=request.data['firstName']
            lastName=request.data['lastName']
            phone=request.data['phone']
            currency=request.data['currency']
            product=request.data['product']
            color=request.data['color']
            size=request.data['size']
            quantity=request.data['quantity']
            unitprice=0
            # cartitems=cart.objects.all()  ##Users
           
            
            if Offer.objects.filter(product_id=product).exists():
                if currency=='USD':
                    unitprice= (Offer.objects.get(product_id=product).OfferEuro)*100
                elif currency=='SAR':
                    unitprice= (Offer.objects.get(product_id=product).OfferSAR)*100
                elif currency=='GBP':
                    unitprice= (Offer.objects.get(product_id=product).OfferSterling)*100
                elif currency=='EUR':
                    unitprice= (Offer.objects.get(product_id=product).OfferEuro)*100
                elif currency=='AED':
                    unitprice= (Offer.objects.get(product_id=product).OfferDirham)*100
                else:
                    pass
            else:
                if currency=='USD':
                    unitprice= (Products.objects.get(id=product).productpriceDollar)*100
                elif currency=='SAR':
                    unitprice= (Products.objects.get(id=product).productpriceSar)*100
                elif currency=='GBP':
                    unitprice= (Products.objects.get(id=product).productpriceSterling)*100
                elif currency=='EUR':
                    unitprice= (Products.objects.get(id=product).productpriceEuro)*100
                elif currency=='AED':
                    unitprice= (Products.objects.get(id=product).productpriceDirham)*100
            productobj=Products.objects.get(id=product)
            itemsPriceDetails=[]
            pricedict=   {
                        'price_data': {
                            'currency': currency,
                            'product_data': {
                            'name': productobj.name,
                            },
                            'unit_amount': unitprice,
                        },
                        'quantity': quantity,
                    }
            itemsPriceDetails.append(pricedict)
            stripe.api_key = settings.STRIPE_SECRET_KEY
            checkout_session = stripe.checkout.Session.create(
                customer_email = request.data['email'],
                payment_method_types=['card'],
                 shipping_options=[],
                                
                line_items=itemsPriceDetails,
                mode='payment',
                success_url=request.build_absolute_uri(
                    reverse('success')
                ) + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=request.build_absolute_uri(reverse('failed')),)
            order=Order()
            order.product=productobj
            order.quantity=quantity
            order.user=self.request.user
            if size!=0:
                order.selectedsize=Sizes.objects.get(id=size)
            if color!=0:
                order.selectedcolor=Options.objects.get(id=color)
            order.address=address
            order.city=city
            order.country=country
            order.firstName=firstName
            order.phone=phone
            order.email=email
            order.pincode=pincode
            order.lastName=lastName
            order.stripe_payment_intent=checkout_session['payment_intent']
            order.amount=unitprice*quantity
            order.currency=currency
            order.status="Attempted"
            order.save()
            
            return JsonResponse({'sessionId': checkout_session.id,'url':checkout_session.url})



class PaymentSuccessView(APIView):

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()
        
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)

        order = Order.objects.filter(stripe_payment_intent=session.payment_intent)
        for o in order:
            o.has_paid=True
            o.status="Ordered"
            if o.parentcart: 
                o.parentcart.is_placed=True
                o.parentcart.save()         
            o.save()
        return redirect("http://voui.fr/settings/orders")




class CustomerOrderViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = OrdersSerializer
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)




class BottomProductViewset(viewsets.ModelViewSet):
    queryset = BottomProductDisplay.objects.all()
    # specify serializer to bce used
    serializer_class = BottomProductDisplaySerializer

class BottomProductAPIView(APIView):
    def get(self, request, format=None):
        bproducts=BottomProductDisplay.objects.all()
        if bproducts.exists():
            productIDs=[]
            for product in bproducts:
                productIDs.append(product.product.id)
                
            
            bottomProducts=Products.objects.filter(id__in=productIDs)
            bottomProductsSerilizer=productSerializer(bottomProducts,many=True,context={"request": request})
            brandnames=[]
            colors=[]
            sizes=[]
            for product in bottomProducts:
                if product.brand:
                    data={"id":product.brand.id,"name":product.brand.name}
                    if not data in brandnames:
                        brandnames.append(data)
                if Options.objects.filter(product=product).exists():
                    options=Options.objects.filter(product=product)
                    for option in options:
                        data={"color":option.color,"colorhash":option.colorhash}
                        if not data in colors:
                            colors.append(data)
                        if Sizes.objects.filter(option=option).exists():
                            sizeses=Sizes.objects.filter(option=option)
                            for size in sizeses:
                                data={"size":size.size}
                                if not data in sizes:
                                    sizes.append(data)
                
            data={
                "products":bottomProductsSerilizer.data,
                "availablebrands":brandnames,
                "availabeColours":colors,
                "availableSizes":sizes

            }
            
            return Response(data)
        return Response({"message":"Not Found"},status=status.HTTP_404_NOT_FOUND)
        

class ProductReviewCreateViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    # define queryset
    queryset = ProductReview.objects.all()
    # specify serializer to be used
    
    serializer_class = ProductReviewSerializer

    def get_serializer_class(self):
        if self.action=="create":
            return ProductReviewSerializer
        return self.serializer_class
    

    def perform_create(self,serializer):
        serializer.save(customer=self.request.user)
    
