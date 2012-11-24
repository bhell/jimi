from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from jimi.catalog.models import Node, Product, Category, Variance, Variant


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
        return self.model.objects.filter(kind=Node.CATEGORY)


class ProductAdmin(NodeAdmin):
    #if not self.is_leave_node():
    #    exclude += ("fragment_in_stock", "fragment_pending_customer", "fragment_pending_supplier",)

    def queryset(self, request):
        return self.model.objects.filter(kind=Node.PRODUCT)


class VariantInline(admin.TabularInline):
    model = Variant
    can_delete = False  # deactivate instead
    extra = 4


class VarianceAdmin(admin.ModelAdmin):
    inlines = (VariantInline,)
    list_display = ['internal_name',
                    'name']
    search_fields = ['name',
                     'internal_name',
                     'description']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Variance, VarianceAdmin)
