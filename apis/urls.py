from django.urls import include, path
# import routers
from rest_framework import routers, views


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
  
# import everything from views
from .views import *
  
# define the router
router = routers.DefaultRouter()
  
# define the router path and viewset to be used
router.register('categories', CategoryViewset)
router.register('subcategories', SubcategoryViewset)
router.register('subsubcategories', SubSubcategoryViewset)
router.register('subsubcategories', SubSubcategoryViewset)
router.register('products', ProductsViewset)
router.register('options', OptionsViewset)
router.register('offersale', OffersaleViewset)
router.register('newcollection', NewCollectionViewset)
router.register('newarrivals', NewArrivalsViewset)
router.register('brandlist', BrandViewSet)
router.register('sizeslist', SizeViewSet)
router.register('wishlists', WhishListViewSet)
router.register('adressofuser', AddressesViewSet)
router.register('cart',CartViewSet)
router.register('get-user',UserDetails)
  
# specify URL Path for rest_framework
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('createuser/', CreateUserView.as_view(), name='createuser'),
    path('search/', SearchView.as_view(), name='search'),
]