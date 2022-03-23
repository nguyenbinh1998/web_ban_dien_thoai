from django.shortcuts import redirect, render, get_object_or_404
from .models import Category, Product, Order
from django.contrib import messages
from decimal import Decimal

def store(request, category_slug=None):
    products = Product.objects.all()
    categories = Category.objects.all()
    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = category.products.all()

    context = {'category':category, 'products':products, 'categories':categories}
    return render(request, 'store/store.html', context)

def product_detail(request, product_id, product_slug):
    if request.user.is_authenticated:
        customer = request.user.customer
        if request.method == "POST":
            id = request.POST['product_id']
            product = get_object_or_404(Product, id=id, avaiable=True)
            if customer.can_purchase(product):
                cart = request.session.get('cart')
                if cart:
                    quantity = cart.get(id)
                    if quantity:
                        cart[id] += 1
                    else:
                        cart[id] = 1
                else:
                    cart = {}
                    cart[id] = 1
                request.session['cart'] = cart
            else:
                messages.warning(request, f"Unfortunately, you don't have enough money to purchase {product.name}!!!")
    else:
        pass    
    product = get_object_or_404(Product, id=product_id, slug=product_slug, avaiable=True)
    context = {'product':product}
    return render(request, 'store/product_detail.html', context)

def cart(request):
    try:
        ids = request.session.get('cart').keys()
    except:
        products = []
        return render(request, 'store/cart.html', {'products':products})
    else:
        products = Product.objects.filter(id__in=ids).all()
        customer = request.user.customer
        cart = request.session.get('cart')
        total_price = 0
        if request.method == "POST":
            address = request.POST['address']
            phone = request.POST['phone']
            for product in products:
                if str(product.id) in cart:
                    total_price += cart[str(product.id)] * Decimal(product.price)
            if customer.budget >= total_price:
                for product in products:
                    new_order = Order(customer=customer, product=product, quantity=cart[str(product.id)], price=product.price, address=address, phone=phone)
                    new_order.save()
                    customer.budget -= total_price
                    customer.save()
                    request.session['cart'] = {}
                    return redirect('cart')
            else:
                messages.warning(request, "You don't have enough money to pay this order!!!")
        return render(request, 'store/cart.html', {'products':products})

def remove(request, product_id):
    cart = request.session.get('cart')
    keys = cart.keys()
    product = Product.objects.get(id=product_id)
    if str(product.id) in keys:
        del cart[str(product.id)]
    request.session['cart'] = cart
    return redirect('cart')
