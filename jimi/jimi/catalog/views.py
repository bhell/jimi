from django.shortcuts import get_object_or_404, render_to_response
from jimi.catalog.models import Node


def node(request, slug):
    """Get node and it's decendants"""
    node = get_object_or_404(Node, slug=slug)
    # In case of product variation, get parent instead
    if node.kind == "V":
        node = node.get_ancestors(ascending=True)[0]
    c = {"node": node,
         "ancestors": node.get_ancestors()}
    if node.kind == "C":
        t = "category.html"
        c["categories"] = []
        c["products"] = []
        children = node.get_children()
        for child in children:
            if child.kind == "C":
                c["categories"].append(child)
            elif child.kind == "P":
                c["products"].append(child)
    elif node.kind == "P":
        t = "product.html"
        c["variations"] = []
        children = node.get_children()
        for child in children:
            c["variations"].append(child)
    return render_to_response(t, c)


def all_categories(request, slug=None):
    """Get all gategories as trees"""
    c = {"categories": Node.objects.filter(kind="C")}
    return render_to_response("categories.html", c)
