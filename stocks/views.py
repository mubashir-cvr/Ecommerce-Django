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
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            response_data = {
                "status" : "true",
                "title" : "Successfully Submitted",
                "message" : "Message successfully updated"
            }
        else:
            print (form.errors)
            response_data = {
                "status" : "false",
                "title" : "Form validation error",
            }
            return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    context={
        'cateregories':Category.objects.all(),
        'form':form
        }
    return render(request,'stocks/listcategories.html',context)

def addcategory(request):
    return render(request,'stocks/addcategory.html')

def editcategory(request):
    return render(request,'stocks/editcategory.html')


def orderlist(request):
    return render(request,'stocks/orderlist.html')

def orderdetails(request):
    return render(request,'stocks/orderdetails.html')