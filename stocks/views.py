from django.shortcuts import render
from apis.models import *
from .froms import *
from django.http import HttpResponse
import json
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
    form = CategoryForm(request.POST or None)
    context={
        'form':form
        }
    return render(request,'stocks/listcategories.html',context)

def addcategory(request):
    return render(request,'stocks/editsubcategory.html')

def editcategory(request):
    return render(request,'stocks/editcategory.html')


def orderlist(request):
    return render(request,'stocks/orderlist.html')

def orderdetails(request):
    return render(request,'stocks/orderdetails.html')

def listsubcategories(request,**args):
    
    return render(request,'stocks/listsubcategories.html')

def listsubsubcategories(request,**args):
    
    return render(request,'stocks/listsubsubcategories.html')



def listproductsone(request,**args):
    
    return render(request,'stocks/listproductsone.html')



def listoptions(request,**args):
    
    return render(request,'stocks/listoptions.html')



def editsubcategory(request,id):
    return render(request,'stocks/editsubcategory.html')


def editsubsubcategory(request,id):
    return render(request,'stocks/editsubsubcategory.html')



def editproducts(request,id):
    return render(request,'stocks/editproducts.html')


def editoptions(request,id):
    return render(request,'stocks/editoptions.html')


def listsizes(request,id):
    return render(request,'stocks/listsizes.html')



def listbrands(request):
    return render(request,'stocks/listbrands.html')


def paymenttest(request):
    return render(request,'stocks/stripe.html')

