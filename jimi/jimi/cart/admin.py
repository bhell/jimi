from django.contrib import admin
from models import ItemList, Item, Cart, Order, Wishlist
#from django.utils.translation import ugettext as _


class ItemInline(admin.TabularInline):
    model = Item
    can_delete = False  # deactivate instead
    extra = 1
    readonly_fields = ("orderprice",)



class ItemListAdmin(admin.ModelAdmin):
    exclude = ('kind',)
    readonly_fields = ('ident', 'session', 'user', 'created', 'updated',)
    inlines = (ItemInline,)
    # fieldsets = (
    #     (None, {
    #         'fields': ('ItemInline',)
    #     }),
    #     (_('Advanced attributes'), {
    #         'classes': ('collapse',),
    #         'fields': ('ident', 'session',)
    #     }),
    # )

    class Meta:
        abstract = True


class CartAdmin(ItemListAdmin):
    #def __init__(self):
    #self.exclude += ("fragment_in_stock", "fragment_pending_customer", "fragment_pending_supplier",)

    def queryset(self, request):
        return self.model.objects.filter(kind=ItemList.CART)


class OrderAdmin(ItemListAdmin):
    #def __init__(self):
    #self.exclude += ("fragment_in_stock", "fragment_pending_customer", "fragment_pending_supplier",)

    def queryset(self, request):
        return self.model.objects.filter(kind=ItemList.ORDER)


class WishlistAdmin(ItemListAdmin):
    #def __init__(self):
    #self.exclude += ("fragment_in_stock", "fragment_pending_customer", "fragment_pending_supplier",)

    def queryset(self, request):
        return self.model.objects.filter(kind=ItemList.WISHLIST)

admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Wishlist, WishlistAdmin)
