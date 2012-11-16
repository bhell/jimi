from django.shortcuts import get_object_or_404, render_to_response
from jimi.catalog.models import Node


def node(request, slug):
    node = get_object_or_404(Node, slug=slug)
    if node.kind == "C":
        t = "category.html"
    else:
        t = "product.html"
    return render_to_response(t, {"node": node})
