from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from jimi.price.fields import MoneyField
from django.utils.translation import ugettext as _



class Node(MPTTModel):
    """Catalog node"""
    KIND_CHOICES = (("C", _("Category")),
                    ("P", _("Product")),
                    ("V", _("Product variation")))
    name = models.CharField(_("Name"), max_length=128)
    kind = models.CharField(_("Kind"),
                            max_length=1,
                            choices=KIND_CHOICES,
                            db_index=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
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
    price_fragment = MoneyField(_("Price"),
                                max_digits=9,
                                decimal_places=2,
                                default=0.00,
                                help_text=_("Total price is accumulated from fragments spanning categories, product and variation"))
    fragment_in_stock = models.IntegerField(_("Stock"),
                                            default=0,
                                            help_text=_("Number of items in stock"))
    # TODO These two should be generated from Orders
    fragment_pending_customer = models.IntegerField(_("Pending to customer"),
                                            default=0,
                                            help_text=_("Number of items pending to customer"))
    fragment_pending_supplier = models.IntegerField(_("Pending from supplier"),
                                            default=0,
                                            help_text=_("Number of items pending from supplier"))

    class MPTTMeta:
        order_insertion_by = ['name']

    def __unicode__(self):
        return self.name

    def price(self):
        p = 0
        for n in self.get_ancestors(include_self=True):
            p += n.price_fragment
        return p

    def in_stock(self):
        c = 0
        for n in self.get_descendants(include_self=True):
            c += n.fragment_in_stock
        return c

    def pending_customer(self):
        c = 0
        for n in self.get_descendants(include_self=True):
            c += n.fragment_pending_customer
        return c

    def pending_supplier(self):
        c = 0
        for n in self.get_descendants(include_self=True):
            c += n.fragment_pending_supplier
        return c

    def is_procurable(self):
        """Determine if node could be purchased"""
        if self.kind != "C" and self.is_leave_node():
            return True
        else:
            return False

    def is_variation(self):
        """Determine if node is a product variation"""
        if self.is_leave_node() and self.parent.kind == "P":
            return True
        else:
            return False

    def has_variations(self):
        """Determine if node is product with variations"""
        if self.kind == "P" and not self.is_leave_node():
            return True
        else:
            return False

    @models.permalink
    def get_absolute_url(self):
        if self.kind == "V":  # Parent URL for variations
            return ("node", (), {'slug': self.get_ancestors(ascending=True)[0].slug})
        else:
            return ("node", (), {'slug': self.slug})


class Category(Node):
    """Catalog nodes representing categories"""
    class Meta:
        proxy = True
        verbose_name_plural = _("Categories")

    def save(self, *args, **kwargs):
        self.kind = "C"
        super(Category, self).save(*args, **kwargs)


class Product(Node):
    """Catalog nodes representing products or product variations"""
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if self.parent.kind == "P":
            self.kind = "V"
        else:
            self.kind = "P"
        super(Product, self).save(*args, **kwargs)
