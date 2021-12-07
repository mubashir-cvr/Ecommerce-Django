from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
  
# import local data
from .serializers import CategorySerializer,SubcategorySerializer,\
    SubSubcategorySerializer,productSerializer,optionsSerializer
from .models import Category, SubCategory,SubSubCategory,Options,Products
  
# create a viewset
class CategoryViewset(viewsets.ModelViewSet):
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
    # specify serializer to bce used
    serializer_class = productSerializer


class OptionsViewset(viewsets.ModelViewSet):
    # define queryset
    queryset = Options.objects.all()
    # specify serializer to bce used
    serializer_class = optionsSerializer

