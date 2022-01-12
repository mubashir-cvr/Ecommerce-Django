import re
from rest_framework import viewsets,generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.serializers import Serializer
from .pagination import *
from .serializers import * 
from .models import Category, SubCategory,SubSubCategory,Options,Products,NewCollection
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



class OffersaleViewset(viewsets.ModelViewSet):
    # define queryset
    
    queryset = Products.objects.filter(offers__offerPrice__gt=0)
    # specify serializer to bce used
    serializer_class = productSerializer





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
    
    queryset = Products.objects.filter(offers__offerPrice__gt=0)
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


# class ContactViewSet(viewsets.ModelViewSet):
#     permission_classes = (IsAuthenticated,)
#     # define queryset
#     queryset = AddressesOfUser.objects.all()
#     # specify serializer to be used
    
#     serializer_class = ContactDetailsOfUserSerializer


#     def get_queryset(self):
#         return self.queryset.filter(user=self.request.user)
    

#     def perform_create(self,serializer):
#         serializer.save(user=self.request.user)