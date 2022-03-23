from django import template

register = template.Library()

@register.simple_tag
def get_quantity(product, cart):
    id = str(product.id)
    if id in cart.keys():
        return cart[id]
    else:
        return 0

@register.simple_tag
def get_price(product, cart):
    id = str(product.id)
    if id in cart.keys():
        total = product.price * cart[id]
        return f"{total:,}"
    return 0

@register.simple_tag
def get_total_price(products, cart):
    total = 0
    for product in products:
        quantity = cart.get(str(product.id))
        if quantity:
            total += product.price * quantity
            return f"{total:,}"
        else:
            return 0