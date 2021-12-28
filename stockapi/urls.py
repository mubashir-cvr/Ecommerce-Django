from django.urls import include, path
# import routers
from rest_framework import routers
from rest_framework.routers import DefaultRouter



# import everything from views
from .views import *
  
# define the router
  
# define the router path and viewset to be used
router = DefaultRouter()
router.register('admincategories', AdminCategoryViewset)
router.register('subcategories', AdminSubcategoryViewset)
router.register('adminsubsubcategories', AdminSubSubcategoryViewset)
router.register('adminproducts', AdminProductsViewset)
router.register('adminoptions', AdminOptionsViewset)
router.register('adminoffersale', AdminOffersaleViewset)
router.register('adminnewcollection', AdminNewCollectionViewset)
router.register('adminnewarrivals', AdminNewArrivalsViewset)
app_name = 'stockapi'
  
# specify URL Path for rest_framework
urlpatterns = [
    path('', include(router.urls)),
    path('deletecategory/<int:pk>',DeleteCategory.as_view()),
     path('deletesubcategory/<int:pk>',DeleteSubCategory.as_view()),
     path('deletesubsubcategory/<int:pk>',DeleteSubSubCategory.as_view())
]