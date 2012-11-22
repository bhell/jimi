from django.conf.urls.defaults import patterns

urlpatterns = patterns("jimi.cart.views",
    (r"^/?$", "cart", {}, "cart"),
)
