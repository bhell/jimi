from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from jimi.catalog.models import Node, Product, Category


class NodeAdmin(MPTTModelAdmin):
    list_display = ('name', 'created', 'updated',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['name']
    search_fields = ['name',
                     'slug',
                     'teaser',
                     'description',
                     'meta_keywords',
                     'meta_description']
    exclude = ('kind',)
    prepopulated_fields = {'slug': ('name',)}

    class Meta:
        abstract = True


class CategoryAdmin(NodeAdmin):
    #def __init__(self):
    #self.exclude += ("fragment_in_stock", "fragment_pending_customer", "fragment_pending_supplier",)

    def queryset(self, request):
        return self.model.objects.filter(kind="C")


class ProductAdmin(NodeAdmin):
    #if not self.is_leave_node():
    #    exclude += ("fragment_in_stock", "fragment_pending_customer", "fragment_pending_supplier",)

    def queryset(self, request):
        return self.model.objects.filter(kind="P")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
