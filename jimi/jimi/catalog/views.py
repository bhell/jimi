from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
#from django.template.loader import get_template
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from jimi.catalog.models import Node
from jimi.lists.models import Item, Cart, CART_ID_SESSION_KEY
from jimi.catalog.forms import ProductAddToCartForm


def _add_to_cart(request):
    """
    Add leaf node to cart.

    Use already existing cart in session. Make a new one if there
    is no cart yet or if it cannot be found. The latter should only
    happen when the cart got deleted in the database while the session
    is still valid. This should not happen on production systems, but
    the error will be cought anyways.
    """
    postdata = request.POST.copy()
    slug = postdata.get('product', '')
    quantity = postdata.get('quantity', 1)
    product = get_object_or_404(Node, slug=slug)
    _cart_found = False
    if request.session.get(CART_ID_SESSION_KEY):
        try:
            cart = Cart.objects.get(pk=request.session[CART_ID_SESSION_KEY])
            _cart_found = True
        except Cart.DoesNotExist:
            pass  # We'll make a new one.
    if not _cart_found:
        cart = Cart()
        cart.kind = cart.CART
        cart.save()
        request.session[CART_ID_SESSION_KEY] = cart.ident
    # TODO if user is logged in, set user

    cart_items = Item.objects.filter(itemlist=cart)
    already_in_cart = False
    for item in cart_items:  # TODO more elegant "if item in cart"
        if item.product == product:
            item.augment_quantity(quantity)
            already_in_cart = True
    if not already_in_cart:
        item = Item()
        item.product = product
        item.quantity = quantity
        item.itemlist = cart
        item.save()


def node(request, slug):
    """
    View node and it's decendants.

    Depending on whether the node is a category or a product,
    different responses with different templates are generated.
    """
    node = get_object_or_404(Node, slug=slug)
    # In case of product variation, get parent instead
    if node.kind == node.VARIATION:
        node = node.get_ancestors(ascending=True)[0]
    c = {"node": node,
         "ancestors": node.get_ancestors()}
    if node.kind == node.CATEGORY:
        t = "category.html"
        c["categories"] = []
        c["products"] = []
        children = node.get_children()
        for child in children:
            if child.kind == node.CATEGORY:
                c["categories"].append(child)
            elif child.kind == node.PRODUCT:
                c["products"].append(child)
    elif node.kind == node.PRODUCT:
        c.update(csrf(request))
        t = "product.html"
        c["variations"] = []
        children = node.get_children()
        for child in children:
            c["variations"].append(child)
        if request.method == 'POST':  # coming from the add to cart form
            postdata = request.POST.copy()
            form = ProductAddToCartForm(request, postdata)
            if form.is_valid():
                _add_to_cart(request)
                # remove test cookie if necessary
                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()
                url = urlresolvers.reverse('cart')
                return HttpResponseRedirect(url)
        else:  # request.method == 'GET'
            form = ProductAddToCartForm(request=request, label_suffix=":")
            form.fields['product'].widget.attrs['value'] = node.slug
            c['form'] = form
            # When loading the product page, set a test cookie
            request.session.set_test_cookie()
#    C = RequestContext(request, c)
#    return t.render(C)
    return render_to_response(t, c, context_instance=RequestContext(request))


def all_categories(request, slug=None):
    """
    View all categories.

    Go through the categories and present them as tree(s).
    """
    c = {"categories": Node.objects.filter(kind="C")}
    return render_to_response("categories.html", c)
