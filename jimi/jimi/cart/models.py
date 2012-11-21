from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils.translation import ugettext as _
from jimi.price.fields import MoneyField
from jimi.catalog.models import Product


class ItemList(models.Model):
    """
    Shopping cart or order list etc.

    There is no real distinction between a shopping cart before and after it is
    ordered. The ordered one just needs a couple of extra attributes, such as
    shipping and payment details.
    """
    CART = "c"
    WISHLIST = "w"
    SAVED = "s"
    ORDER = "o"
    KIND_CHOICES = ((CART, _("in cart")),
                    (WISHLIST, _("in wish list")),
                    (SAVED, _("saved for later")),
                    (ORDER, _("ordered")))
    ident = models.CharField(max_length=64,
                             db_index=True,
                             help_text=_("Unique ID. Auto generated."))
    kind = models.CharField(_("Status"),
                            max_length=1,
                            choices=KIND_CHOICES,
                            db_index=True,
                            help_text=_("Status flag indicating if entry is in cart, wish list, purchased etc."))
    session = models.ForeignKey(Session,
                               db_index=True,
                               blank=True,
                               help_text=_("Session ID. Auto generated."))
    user = models.ForeignKey(User,
                             db_index=True,
                             blank=True,
                             help_text=_("User owning cart"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'jimi_cart'
        ordering = ['created']


class Item(models.Model):
    """An item in a shopping cart"""
    active = models.BooleanField(_("is active"),
                                 default=True,
                                 help_text=_("deactivate to remove item"))
    itemlist = models.ForeignKey(ItemList,
                                 verbose_name=_("Cart/order/wishlist"),
                                 db_index=True,
                                 help_text=_("Related cart"))
    product = models.ForeignKey(Product,
                                verbose_name=_("Product"),
                                db_index=True,
                                help_text=_("Related product"))
    # TODO float amounts
    quantity = models.IntegerField(_("Quantity"),
                                   default=1)
    orderprice = MoneyField(_("Price at order time"),
                            blank=True,
                            help_text=_("Product price when ordered, including discounts etc."))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'jimi_cartitem'
        ordering = ['created']

    @property
    def total(self):
        return self.quantity * self.price

    @property
    def name(self):
        return self.product.name

    @property
    def price(self):
        """
        Get actual price.

        The orderprice attribute can only be set
        when an order is saved, so it should be safe to rely on it not
        being present in other cases.
        """
        # TODO: What happens with items ordered at a zero price?
        return self.orderprice or self.product.price

    @property
    def stock_available(self):
        return self.product.stock_available

    @property
    def in_stock(self):
        return self.stock_available > self.quantity

    def augment_quantity(self, n):
        self.quantity += int(n)
        self.save()
        return self.quantity

    @models.permalink
    def get_absolute_url(self):
        return self.product.get_absolute_url()


class Cart(ItemList):
    """Shopping cart."""
    class Meta:
        proxy = True

    @property
    def checkout_possible(self):
        """Make sure that stock is sufficient for checkout"""
        checkout = True
        for item in self.itemlist:
            if not item.in_stock:
                checkout = False
        return checkout

    def save(self, *args, **kwargs):
        self.kind = self.CART
        super(Cart, self).save(*args, **kwargs)


class Order(ItemList):
    """Order."""
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.kind = self.ORDER
        # Freeze item prices when order is created
        for item in Item.objects.filter(itemlist__exact=self.ident):
            item.orderprice = item.price
            item.save()
        super(Order, self).save(*args, **kwargs)


class Wishlist(ItemList):
    """Wish list."""
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.kind = self.WISHLIST
        super(Wishlist, self).save(*args, **kwargs)

# TODO
# Validate that only some product and variation nodes can be added to cart
# Cron job to delete cart items from expired sessions
