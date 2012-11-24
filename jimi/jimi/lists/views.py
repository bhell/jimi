from models import Cart, Item, CART_ID_SESSION_KEY
from django.shortcuts import get_object_or_404, render_to_response


def cart(request):
    """View the cart"""
    c = {'cart': None,
         'items': [],
         'msg': ''}
    t = 'cart.html'
    if request.session.get(CART_ID_SESSION_KEY):
        cart = get_object_or_404(Cart, ident=request.session[CART_ID_SESSION_KEY])
        c['cart'] = cart
        items = Item.objects.filter(itemlist=cart)
        c['items'] = [i for i in items]
    return render_to_response(t, c)
