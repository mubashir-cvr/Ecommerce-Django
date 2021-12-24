from django.urls import include, path
# import routers
from rest_framework import routers


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
  
# import everything from views
from .views import *
  
# define the router
router = routers.DefaultRouter()
  
# define the router path and viewset to be used
router.register(    'categories', CategoryViewset)
router.register('subcategories', SubcategoryViewset)
router.register('subsubcategories', SubSubcategoryViewset)
router.register('subsubcategories', SubSubcategoryViewset)
router.register('products', ProductsViewset)
router.register('options', OptionsViewset)
router.register('offersale', OffersaleViewset)
router.register('newcollection', NewCollectionViewset)
router.register('newarrivals', NewArrivalsViewset)
  
# specify URL Path for rest_framework
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('createuser/', CreateUserView.as_view(), name='createuser'),
]