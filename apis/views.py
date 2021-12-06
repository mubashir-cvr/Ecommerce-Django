from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
  
# import local data
from .serializers import CategorySerializer,SubcategorySerializer,SubSubcategorySerializer
from .models import Category, SubCategory,SubSubCategory
  
# create a viewset
class CategoryViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
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

