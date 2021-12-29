from django.urls import include, path
from .views import *

app_name="stock"

urlpatterns = [
    path('',home,name="home"),
    path('addproduct',addproduct,name="addproduct"),
    path('listProducts',listProduct,name="listProduct"),
    path('listproductgrid',listproductgrid,name="listproductgrid"),
    path('editproduct',editproduct,name="editproduct"),
    path('listcategories',listcategories,name="listcategories"),
    path('addcategory',addcategory,name="addcategory"),
    path('editcategory',editcategory,name="editcategory"),
    path('orderdetails',orderdetails,name="orderdetails"),
    path('orderlist',orderlist,name="orderlist"),
    path('listsubcategories/<int:id>/<str:category>',listsubcategories,name="listsubcategories"),
    path('listsubsubcategories/<int:id>',listsubsubcategories,name="listsubsubcategories"),
    path('listproducts/<int:id>',listproductsone,name="listproducts"),
    path('listoptions/<int:id>',listoptions,name="listoptions"),
]