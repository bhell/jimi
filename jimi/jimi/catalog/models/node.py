from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from variance import Variant
from jimi.price.fields import Money, MoneyField
from django.utils.translation import ugettext as _


class Node(MPTTModel):
    """Catalog node"""
    CATEGORY = "c"
    PRODUCT = "p"
    VARIATION = "v"
    KIND_CHOICES = ((CATEGORY, _("Category")),
                    (PRODUCT, _("Product")),
                    (VARIATION, _("Product variation")))
    name = models.CharField(_("Name"), max_length=128)
    kind = models.CharField(_("Kind"),
                            max_length=1,
                            choices=KIND_CHOICES,
                            db_index=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    variant = models.ManyToManyField(Variant,
                                     blank=True,
                                     db_table="jimi_productvariant",
                                     help_text=_("Variant of product"))
    slug = models.SlugField(max_length=128,
                            unique=True,
                            help_text=_("Unique text string for page URL. Created from name."))
    teaser = models.TextField(_("Teaser"))
    description = models.TextField(_("Description"))
    active = models.BooleanField(_("Is active"))
    meta_keywords = models.CharField(_("Meta keywords"),
                                     max_length=255,
                                     help_text=_("Comma separated list of SEO keywords for meta tag"))
    meta_description = models.CharField(_("Meta description"),
                                        max_length=255,
                                        help_text=_("Content for description meta tag"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    _supplier = models.CharField(_("Supplier"),
                                 max_length=255,
                                 blank=True,
                                 db_column="supplier",
                                 help_text=_("Supplier for catalog node. Fallback to parent"
                                          + " node supplier."))
    _price = MoneyField(_("Price"),
                        default=0.00,
                        db_column="price",
                        help_text=_("Total price is accumulated from fragments"
                                 + " spanning categories, product and variation"))
    _stock = models.IntegerField(_("Stock"),
                                 default=0,
                                 db_column="stock",
                                 help_text=_("Number of items in stock"))
    # TODO These two should be generated from Orders
    _pending_customer = models.IntegerField(_("Pending to customer"),
                                            default=0,
                                            db_column="pending_customer",
                                            help_text=_("Number of items pending to customer"))
    _pending_supplier = models.IntegerField(_("Pending from supplier"),
                                            default=0,
                                            db_column="pending_supplier",
                                            help_text=_("Number of items pending from supplier"))
    # TODO tax classification

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        db_table = 'jimi_catalog'
        app_label = 'catalog'

    def __unicode__(self):
        return self.name

    @property
    def price(self):
        """Accumulate price"""
        p = Money(0)
        for n in self.get_ancestors(include_self=True):
            p += n._price
        return p

    @price.setter
    def price(self, value):
        self._price = value

    @property
    def supplier(self):
        """Get supplier, either from node itself or from the first ancestor
        where it is set."""
        for n in self.get_ancestors(include_self=True, ascending=True):
            if n._supplier:
                return n._supplier
        return None

    @supplier.setter
    def supplier(self, value):
        self._supplier = value

    @property
    def stock(self):
        """Accumulate stock"""
        c = 0
        for n in self.get_descendants(include_self=True):
            c += n._stock
        return c

    @stock.setter
    def stock(self, value):
        self._stock = value

    @property
    def pending_customer(self):
        c = 0
        for n in self.get_descendants(include_self=True):
            c += n._pending_customer
        return c

    @pending_customer.setter
    def pending_customer(self, value):
        self._pending_customer = value

    @property
    def pending_supplier(self):
        c = 0
        for n in self.get_descendants(include_self=True):
            c += n._pending_supplier
        return c

    @pending_supplier.setter
    def pending_supplier(self, value):
        self._pending_supplier = value

    @property
    def stock_available(self):
        return self.stock - self.pending_customer

    @property
    def in_stock(self):
        return self.stock_available > 0

    @property
    def is_procurable(self):
        """Determine if node could be purchased"""
        if self.kind != Node.CATEGORY and self.is_leave_node():
            return True
        else:
            return False

    @property
    def is_variation(self):
        """Determine if node is a product variation"""
        if self.is_leave_node() and self.parent.kind == "P":
            return True
        else:
            return False

    @property
    def has_variations(self):
        """Determine if node is product with variations"""
        if self.kind == Node.PRODUCT and not self.is_leave_node():
            return True
        else:
            return False

    @models.permalink
    def get_absolute_url(self):
        if self.kind == Node.VARIATION:  # Parent URL for variations
            return ("node", (), {'slug': self.get_ancestors(ascending=True)[0].slug})
        else:
            return ("node", (), {'slug': self.slug})


class Category(Node):
    """Catalog nodes representing categories"""
    class Meta:
        proxy = True
        verbose_name_plural = _("Categories")
        app_label = 'catalog'

    def save(self, *args, **kwargs):
        self.kind = self.CATEGORY
        super(Category, self).save(*args, **kwargs)


class Product(Node):
    """Catalog nodes representing products or product variations"""
    # TODO Does limit_choices_to work for parent restrictions?
    # TODO Only Variations should be allowed to have a relation to Variant
    class Meta:
        proxy = True
        app_label = 'catalog'

    def save(self, *args, **kwargs):
        if self.parent.kind == self.PRODUCT:
            self.kind = self.VARIATION
        else:
            self.kind = self.PRODUCT
        super(Product, self).save(*args, **kwargs)
