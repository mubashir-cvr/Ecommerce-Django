
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





class OptionsViewset(viewsets.ModelViewSet):
    # define queryset
    queryset = Options.objects.all()
    # specify serializer to bce used
    serializer_class = optionsSerializer









class NewArrivalsViewset(viewsets.ModelViewSet):
    time_threshold = datetime.now() - timedelta(days=5)
    queryset = Products.objects.filter(created_date__gte=time_threshold)
    # specify serializer to bce used
    serializer_class = productSerializer




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




class OffersaleViewset(viewsets.ModelViewSet):
    # define queryset
    
    queryset = Products.objects.filter(offers__OfferEuro__gt=0)
    # specify serializer to bce used
    serializer_class = productSerializer




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
        return self.queryset.filter(user=self.request.user)

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
            products=Products.objects.filter(name__icontains=key)
            subcategories=SubCategory.objects.filter(name__icontains=key)
            categories=Category.objects.filter(name__icontains=key)
            subsubcategories=SubSubCategory.objects.filter(name__icontains=key)
            
            productserializer = ProductSearchSerializer(products,many=True)
            subcategoryserializer = SubCategorySearchSerializer(subcategories,many=True)
            categoryserializer = CategorySearchSerializer(categories,many=True)
            subSubcategorySerializer = SubSubCategorySearchSerializer(subsubcategories,many=True)
            searchdata={
            "products":productserializer.data,
            "subcategory":subcategoryserializer.data,
            "Category":categoryserializer.data,
            "subsubcategory":subSubcategorySerializer.data,
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
            first_name=request.data['first_name']
            last_name=request.data['last_name']
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
                    unitprice= Offer.objects.get(product=item.product).OfferEuro
                elif currency=='SAR':
                    unitprice= Offer.objects.get(product=item.product).OfferSAR
                elif currency=='GBP':
                    unitprice= Offer.objects.get(product=item.product).OfferSterling
                elif currency=='EUR':
                    unitprice= Offer.objects.get(product=item.product).OfferEuro
                elif currency=='AED':
                    unitprice= Offer.objects.get(product=item.product).OfferDirham
                else:
                    pass
            else:
                print("Collecting Normal Data..........")
                if currency=='USD':
                    unitprice= item.product.productpriceDollar
                elif currency=='SAR':
                    unitprice= item.product.productpriceSar
                elif currency=='GBP':
                    unitprice= item.product.productpriceSterling
                elif currency=='EUR':
                    unitprice= item.product.productpriceEuro
                elif currency=='AED':
                    unitprice= item.product.productpriceDirham
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
            order.first_name=first_name
            order.phone=phone
            order.email=email
            order.pincode=pincode
            order.last_name=last_name
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
            first_name=request.data['first_name']
            last_name=request.data['last_name']
            phone=request.data['phone']
            currency=request.data['currency']
            product=request.data['product']
            try:
                color=request.data['color']
                size=request.data['size']
            except:
                pass
            quantity=request.data['quantity']
            unitprice=0
            # cartitems=cart.objects.all()  ##Users
           
            
            if Offer.objects.filter(product_id=product).exists():
                if currency=='USD':
                    unitprice= Offer.objects.get(product_id=product).OfferEuro
                elif currency=='SAR':
                    unitprice= Offer.objects.get(product_id=product).OfferSAR
                elif currency=='GBP':
                    unitprice= Offer.objects.get(product_id=product).OfferSterling
                elif currency=='EUR':
                    unitprice= Offer.objects.get(product_id=product).OfferEuro
                elif currency=='AED':
                    unitprice= Offer.objects.get(product_id=product).OfferDirham
                else:
                    pass
            else:
                if currency=='USD':
                    unitprice= Products.objects.get(id=product).productpriceDollar
                elif currency=='SAR':
                    unitprice= Products.objects.get(id=product).productpriceSar
                elif currency=='GBP':
                    unitprice= Products.objects.get(id=product).productpriceSterling
                elif currency=='EUR':
                    unitprice= Products.objects.get(id=product).productpriceEuro
                elif currency=='AED':
                    unitprice= Products.objects.get(id=product).productpriceDirham
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
            if size!=0:
                order.selectedsize=Sizes.objects.get(id=size)
            if color!=0:
                order.selectedcolor=Options.objects.get(id=color)
            order.address=address
            order.city=city
            order.country=country
            order.first_name=first_name
            order.phone=phone
            order.email=email
            order.pincode=pincode
            order.last_name=last_name
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
        return redirect("http://localhost:4200/settings/orders")




class CustomerOrderViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = OrdersSerializer
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)