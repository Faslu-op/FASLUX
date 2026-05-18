from django.shortcuts import render
from .models import *



def Index(request):
    product=Product.objects.all()
    trending=New.objects.all()
    return render(request,'home.html', {'dtls': product, 'dt':trending})


def Hoodie(request):
    category=Category.objects.get(name='HOODIES SWEATSHIRTS')
    product=Product.objects.filter(category=category)
    
    query = request.GET.get('q')
    if query:
        product = product.filter(name__icontains=query) | product.filter(description__icontains=query)
        
    return render(request,'hoodie.html',{'dtls':product, 'query': query})



def Five_sleeve(request):
    category=Category.objects.get(name='FIVE-SLEEVE TEES')
    product=Product.objects.filter(category=category)
    
    query = request.GET.get('q')
    if query:
        product = product.filter(name__icontains=query) | product.filter(description__icontains=query)
        
    return render(request,'five_sleeve.html',{'dtls':product, 'query': query})


def Regular_fit(request):
    category=Category.objects.get(name='Regular Fit')
    product=Product.objects.filter(category=category)
    
    query = request.GET.get('q')
    if query:
        product = product.filter(name__icontains=query) | product.filter(description__icontains=query)
        
    return render(request,'regular.html',{'dtls':product, 'query': query})

def Sleevless(request):
    category=Category.objects.get(name='Sleeveless')
    product=Product.objects.filter(category=category)
    
    query = request.GET.get('q')
    if query:
        product = product.filter(name__icontains=query) | product.filter(description__icontains=query)
        
    return render(request,'sleevless.html',{'dtls':product, 'query': query})

# def New_collection(request):
#     product=New.objects.all()
#     return render(request, 'new-collection.html', {'dtls': product})


def One_product(request,id):
    product=Product.objects.get(pk=id) 
    similar_products = Product.objects.filter(
    category=product.category).exclude(pk=id)
    return render(request,'product_main.html',{'dtls':product, 'dtlss':similar_products})



def One_products(request, id):
    new_item = New.objects.get(pk=id)

    product = new_item.product   

    similar_products = Product.objects.filter(
        category=product.category).exclude(pk=product.id)

    return render(request, 'product_main.html', {
        'dtls': product,
        'dtlss': similar_products
    })