from django.shortcuts import render
from product.models import Product
from .models import CartItem
# Create your views here.



# def cart_home(request):
#     cart = request.session.get('cart', {})

#     products = []
#     total = 0

#     for product_id, qty in cart.items():
#         product = Product.objects.get(id=product_id)     

#         product.qty = qty
#         product.total_price = product.offer_price * qty

#         total += product.total_price

#         products.append(product)
        
#     return render(request, 'cartt.html', {
#         'products': products,
#         'total': total
#     })

# “Take the value stored in session under key 'cart' and store it in variable cart”

from django.shortcuts import render
from product.models import Product
from .models import CartItem
def cart_home(request):
    if not request.user.is_authenticated:
        return redirect('login') 

    cart_items = CartItem.objects.filter(user=request.user)

    products = []
    total = 0

    for item in cart_items:
        product = item.product
        product.qty = item.quantity
        product.size = item.size
        product.cart_item_id = item.id
        product.total_price = item.total_price()

        total += product.total_price
        products.append(product)

    return render(request, 'cartt.html', {
        'products': products,
        'total': total
    })



from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# @login_required(login_url='users:login')
# def add_to_cart(request, id):
#     cart = request.session.get('cart', {})

#     id = str(id)

#     if id in cart:
#         cart[id] += 1
#     else:
#         cart[id] = 1

#     request.session['cart'] = cart

#     return redirect('cart:cart_home')

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from product.models import Product
from .models import CartItem

@login_required(login_url='users:login')
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    size = request.GET.get('size')

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        size=size
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart:cart_home')



# def update_qty(request, id):
#     if request.method == "POST":
#         action = request.POST.get('action')
#         cart = request.session.get('cart', {})
#         id = str(id)

#         if id in cart:
#             if action == "inc":
#                 cart[id] += 1
#             elif action == "dec":
#                 cart[id] -= 1
#                 if cart[id] <= 0:
#                     del cart[id]

#         request.session['cart'] = cart

#     return redirect('cart:cart_home')

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import CartItem

@login_required(login_url='users:login')
def update_qty(request, id):
    if request.method == "POST":
        action = request.POST.get('action')

        cart_item = get_object_or_404(
            CartItem,
            id=id,
            user=request.user
        )

        if action == "inc":
            cart_item.quantity += 1

        elif action == "dec":
            cart_item.quantity -= 1
            if cart_item.quantity <= 0:
                cart_item.delete()
                return redirect('cart:cart_home')

        cart_item.save()

    return redirect('cart:cart_home')


# def remove_item(request, id):
#     cart = request.session.get('cart', {})
#     id = str(id)

#     if id in cart:
#         del cart[id]

#     request.session['cart'] = cart

#     return redirect('cart:cart_home')
@login_required(login_url='users:login')
def remove_item(request, id):
    cart_item = get_object_or_404(
        CartItem,
        id=id,
        user=request.user
    )

    cart_item.delete()

    return redirect('cart:cart_home')


from django.shortcuts import render, redirect, get_object_or_404


@login_required(login_url='users:login')
def address_page(request, item_id=None):
    if item_id:
        cart_items = CartItem.objects.filter(user=request.user, id=item_id)
    else:
        cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items:
        return redirect('cart:cart_home')

    products = []
    total = 0

    for item in cart_items:
        product = item.product
        product.qty = item.quantity
        product.size = item.size
        product.total_price = item.total_price()
        total += product.total_price
        products.append(product)

    if request.method == "POST":
        request.session['shipping_address'] = {
            'name': request.POST.get('name'),
            'phone': request.POST.get('phone'),
            'address': request.POST.get('address'),
            'city': request.POST.get('city'),
            'pincode': request.POST.get('pincode'),
        }

        if item_id:
            return redirect('cart:payment_page_single', item_id=item_id)
        return redirect('cart:payment_page') 

    return render(request, 'address.html', {
        'products': products,
        'total': total,
        'hide_nav': True,
        'single_item_id': item_id
    })




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from product.models import Product
from .models import Order, OrderItem

@login_required(login_url='users:login')
def payment_page(request, item_id=None):
    if item_id:
        cart_items = CartItem.objects.filter(user=request.user, id=item_id)
    else:
        cart_items = CartItem.objects.filter(user=request.user)
        
    address = request.session.get('shipping_address')

    if not cart_items or not address:
        return redirect('cart:cart_home')

    products = []
    total = 0

    for item in cart_items:
        product = item.product
        product.qty = item.quantity
        product.size = item.size
        product.total_price = item.total_price()
        total += product.total_price
        products.append(product)

    if request.method == "POST":

        order = Order.objects.create(
            user=request.user,
            name=address['name'],
            phone=address['phone'],
            address=address['address'],
            city=address['city'],
            pincode=address['pincode'],
            total_amount=total,
            payment_method="COD"
        )
#     order = Order(
#     user=request.user,
#     name=address['name'],
#     phone=address['phone'],
#     address=address['address'],
#     city=address['city'],
#     pincode=address['pincode'],
#     total_amount=total,
#     payment_method="COD"
# )
# order.save()

   
        for product in products:
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=product.qty,
                price=product.offer_price,
                size=product.size
            )

        # Clear the purchased items from the cart
        cart_items.delete()
        request.session['shipping_address'] = {}

        return redirect('cart:order_success')

    return render(request, 'payment.html', {
        'products': products,
        'total': total,
        'address': address,
        'single_item_id': item_id
    })



def order_success(request):
    return render(request, 'success.html')




from django.contrib.auth.decorators import login_required
from .models import Order

@login_required(login_url='users:login')
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'order_list.html', {
        'orders': orders
    })   


from django.shortcuts import get_object_or_404
from .models import Order

@login_required(login_url='users:login')
def order_detail(request, id):
    order = get_object_or_404(Order, id=id, user=request.user)

    return render(request, 'order_detail.html', {
        'order': order
    })