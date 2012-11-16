from django.conf.urls.defaults import patterns

urlpatterns = patterns("jimi.catalog.views",
    (r"^(?P<slug>[-\w]+)/?$", "node"),
)
