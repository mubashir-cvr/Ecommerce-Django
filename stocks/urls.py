from django.urls import include, path
from .views import *

app_name="stock"

urlpatterns = [
    path('',listcategories,name="listcategories"),
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
    path('editsubcategory/<int:id>',editsubcategory,name="editsubcategory"),
    path('editsubsubcategory/<int:id>',editsubsubcategory,name="editsubsubcategory"),
    path('editproducts/<int:id>',editproducts,name="editproducts"),
    path('editoptions/<int:id>',editoptions,name="editoptions"),
    path('listsizes/<int:id>',listsizes,name="listsizes"),
    path('listbrands',listbrands,name="listbrands"),
    path('paymenttest',paymenttest,name="paymenttest"),
]