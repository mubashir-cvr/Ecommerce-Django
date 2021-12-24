from django.shortcuts import render
# Create your views here.


def home(request):
    return render(request,'stocks/index.html')

    
def addproduct(request):
    return render(request,'stocks/addproduct.html')

def listProduct(request):
    return render(request,'stocks/listproducts.html')

def listproductgrid(request):
    return render(request,'stocks/listproductgrid.html')


def editproduct(request):
    return render(request,'stocks/editproduct.html')

def listcategories(request):
    return render(request,'stocks/listcategories.html')

def addcategory(request):
    return render(request,'stocks/addcategory.html')

def editcategory(request):
    return render(request,'stocks/editcategory.html')


def orderlist(request):
    return render(request,'stocks/orderlist.html')

def orderdetails(request):
    return render(request,'stocks/orderdetails.html')