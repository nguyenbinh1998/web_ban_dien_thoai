from .models import Product
from decimal import Decimal

def cart(request):
    cart = request.session.get('cart')
    total_price = 0
    if cart:
        keys = cart.keys()
        products = Product.objects.filter(id__in=keys)
        for product in products:
            if str(product.id) in keys:
                total_price = total_price + cart[str(product.id)] * Decimal(product.price)
        return {'cart': {'total_items':len(cart), 'total_price':total_price}}
    else:
        return {'cart':{}}
