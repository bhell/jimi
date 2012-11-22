from django.db import models
from django.contrib.auth.models import User
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
    _KIND_CHOICES = ((CART, _("Cart")),
                     (WISHLIST, _("Wish list")),
                     (SAVED, _("Saved for later")),
                     (ORDER, _("Order")))
    ident = models.AutoField(_("ID"),
                             db_index=True,
                             primary_key=True,
                             help_text=_("Unique ID. Auto generated."))
    kind = models.CharField(_("Kind"),
                            max_length=1,
                            choices=_KIND_CHOICES,
                            db_index=True,
                            help_text=_("Flag indicating if entry is in cart, wish list, purchased etc."))
    user = models.ForeignKey(User,
                             db_index=True,
                             blank=True,
                             null=True,
                             help_text=_("User owning cart"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def latest_status(self):
        return Status.objects.filter(itemlist__exact=self.ident).latest('created')

    def __unicode__(self):
        return "%s %s (%s: %s)" % (self.get_kind_display(), self.ident, self.updated, self.latest_status)

    class Meta:
        db_table = 'jimi_list'
        ordering = ['created']

    def save(self, *args, **kwargs):
        """For a new List, an initial Status is generated."""
        auto_status = False
        if not self.ident:
            auto_status = True
        super(ItemList, self).save(*args, **kwargs)
        if auto_status:
            s = Status(status=Status.STATUS_NEW, itemlist=self)
            s.save()


class Status(models.Model):
    """Status of order or purchase order lists"""
    STATUS_NEW = 'n'
    STATUS_PROCESSING = 'p'
    STATUS_INVOICED = 'i'
    STATUS_PAID = 'b'
    STATUS_SENT = 's'
    STATUS_DELIVERED = 'd'
    STATUS_FINISHED = 'f'
    STATUS_CANCELLED = 'x'
    _STATUS_CHOICES = ((STATUS_NEW, _("new")),
                       (STATUS_PROCESSING, _("processing")),
                       (STATUS_INVOICED, _("invoiced")),
                       (STATUS_PAID, _("paid")),
                       (STATUS_SENT, _("sent")),
                       (STATUS_DELIVERED, _("delivered")),
                       (STATUS_FINISHED, _("finished")),
                       (STATUS_CANCELLED, _("cancelled")))
    status = models.CharField(_("Status"),
                            max_length=1,
                            choices=_STATUS_CHOICES,
                            db_index=True,
                            default=STATUS_NEW,
                            help_text=_("Status flag indicating status of order, purchase order etc."))
    itemlist = models.ForeignKey(ItemList,
                                 verbose_name=_("Status"),
                                 db_index=True,
                                 help_text=_("Status flag"))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'jimi_liststatus'
        verbose_name_plural = _("Statuses")
        ordering = ('created',)

    def __unicode__(self):
        return self.get_status_display()


class Item(models.Model):
    """An item in a shopping cart"""
    active = models.BooleanField(_("is active"),
                                 default=True,
                                 help_text=_("deactivate to remove item"))
    itemlist = models.ForeignKey(ItemList,
                                 verbose_name=_("Cart/order/wishlist"),
                                 db_index=True,
                                 help_text=_("Related list"))
    product = models.ForeignKey(Product,
                                verbose_name=_("Product"),
                                db_index=True,
                                help_text=_("Related product"))
    # TODO float amounts
    quantity = models.IntegerField(_("Quantity"),
                                   default=1)
    orderprice = MoneyField(_("Price at order time"),
                            blank=True,
                            null=True,
                            help_text=_("Product price when ordered, including discounts etc."))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'jimi_listitem'
        ordering = ['created']

    @property
    def total(self):
        # TODO take care of bulk discounts
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


class Wishlist(ItemList):
    """Wish list."""
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.kind = self.WISHLIST
        super(Wishlist, self).save(*args, **kwargs)


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


# TODO
# Validate that only some product and variation nodes can be added to cart
# Order status, and mostly readonly data for finished orders
# Wishlist for purchase order and purchase order
# Cron job to delete cart items from expired sessions
