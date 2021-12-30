from rest_framework import viewsets,generics,mixins
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from .serializers import * 
from apis.models import *
from django.http.response import Http404
from rest_framework.response import Response
from datetime import datetime,timedelta





class AdminCategoryViewset(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = AdminCategorySerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.all()

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save()
    
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class AdminSubcategoryViewset(viewsets.ModelViewSet):

    queryset = SubCategory.objects.all()
    serializer_class = AdminSubcategorySerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.all()

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save()
    
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

class AdminSubSubcategoryViewset(viewsets.ModelViewSet):
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
                            mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin):
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
                            mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin):
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
                            mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin):
    time_threshold = datetime.now() - timedelta(days=5)
    queryset = Products.objects.filter(created_date__gte=time_threshold)
    serializer_class = AdminproductSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.all()

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save()
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)




class AdminNewCollectionViewset(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin):
    
    queryset = Products.objects.all()
    serializer_class = AdminproductSerializer
    def get_queryset(self):
        productIds=[]
        if NewCollection.objects.filter().exists():
            newcollection=NewCollection.objects.all()
            for new in newcollection:
                productIds.append(new.product_id)
        return self.queryset.filter(id__in=productIds)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.all()

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save()


class AdminProductsViewset(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin):
    
    queryset = Products.objects.all()
    serializer_class = AdminproductSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.all()

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save()
    


class DeleteCategory(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404
    def delete(self, request, pk, format=None):
        category = self.get_object(pk)
        category.delete()
        return Response({"msg":"success"})



class DeleteSubCategory(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return SubCategory.objects.get(pk=pk)
        except SubCategory.DoesNotExist:
            raise Http404
    def delete(self, request, pk, format=None):
        subcategory = self.get_object(pk)
        subcategory.delete()
        return Response({"msg":"success"})


class DeleteSubSubCategory(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return SubSubCategory.objects.get(pk=pk)
        except SubSubCategory.DoesNotExist:
            raise Http404
    def delete(self, request, pk, format=None):
        subsubcategory = self.get_object(pk)
        subsubcategory.delete()
        return Response({"msg":"success"})
    


class DeleteProduct(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            raise Http404
    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        product.delete()
        return Response({"msg":"success"})

class DeleteOption(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Options.objects.get(pk=pk)
        except Options.DoesNotExist:
            raise Http404
    def delete(self, request, pk, format=None):
        option = self.get_object(pk)
        option.delete()
        return Response({"msg":"success"})