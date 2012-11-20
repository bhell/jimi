from django.conf.urls.defaults import patterns

urlpatterns = patterns("jimi.catalog.views",
    (r"^/?$", "all_categories"),
    (r"^(?P<slug>[-\w]+)/$", "node", {}, "node"),
)
