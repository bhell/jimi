from django.conf.urls.defaults import patterns

urlpatterns = patterns("jimi.lists.views",
    (r"^/?$", "cart", {}, "cart"),
)
