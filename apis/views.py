from rest_framework import viewsets,generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .pagination import *
from .serializers import * 
from .models import Category, SubCategory,SubSubCategory,Options,Products







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


class ProductsViewset(viewsets.ModelViewSet):
    # define queryset
    
    queryset = Products.objects.all()
    pagination_class =LargeResultsSetPagination
    # specify serializer to bce used
    serializer_class = productSerializer


class OptionsViewset(viewsets.ModelViewSet):
    # define queryset
    queryset = Options.objects.all()
    # specify serializer to bce used
    serializer_class = optionsSerializer



class OffersaleViewset(viewsets.ModelViewSet):
    # define queryset
    
    queryset = Products.objects.filter(offers__offerPrice__gt=0)
    pagination_class =LargeResultsSetPagination
    # specify serializer to bce used
    serializer_class = productSerializer