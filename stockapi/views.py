from rest_framework import viewsets,generics,mixins
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .serializers import * 
from apis.models import *
from datetime import datetime,timedelta





class AdminCategoryViewset(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    # define queryset
    queryset = Category.objects.all()
    # specify serializer to be used
    
    serializer_class = AdminCategorySerializer


class AdminSubcategoryViewset(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    # define queryset
    queryset = SubCategory.objects.all()
    # specify serializer to be used
    serializer_class = AdminSubcategorySerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.all()

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save()


class AdminSubSubcategoryViewset(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    # define queryset
    queryset = SubSubCategory.objects.all()
    # specify serializer to bce used
    serializer_class = AdminSubSubcategorySerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.all()

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save()




class AdminOptionsViewset(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    # define queryset
    queryset = Options.objects.all()
    # specify serializer to bce used
    serializer_class = AdminoptionsSerializer
    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.all()

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save()



class AdminOffersaleViewset(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    # define queryset
    
    queryset = Products.objects.filter(offers__offerPrice__gt=0)
    # specify serializer to bce used
    serializer_class = AdminproductSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.all()

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save()





class AdminNewArrivalsViewset(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    time_threshold = datetime.now() - timedelta(days=5)
    queryset = Products.objects.filter(created_date__gte=time_threshold)
    # specify serializer to bce used
    serializer_class = AdminproductSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.all()

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save()




class AdminNewCollectionViewset(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    # define queryset
    productIds=[]
    if NewCollection.objects.filter().exists():
        newcollection=NewCollection.objects.all()
        for new in newcollection:
            productIds.append(new.product_id)
    queryset = Products.objects.filter(id__in=productIds)
    # specify serializer to bce used
    serializer_class = AdminproductSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.all()

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save()


class AdminProductsViewset(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    # define queryset
    
    queryset = Products.objects.all()
    # specify serializer to bce used
    serializer_class = AdminproductSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.all()

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save()