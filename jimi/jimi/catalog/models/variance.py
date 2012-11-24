from django.db import models
from django.utils.translation import ugettext as _


class Variance(models.Model):
    """Variance of a product, such as size or color."""
    name = models.CharField(_("Name"),
                            max_length=255,
                            help_text=_('Name of the variance visible'
                                     + ' for customer, e.g. "Size"'))
    internal_name = models.CharField(_("Internal name"),
                            max_length=255,
                            blank=True,
                            help_text=_('Name of the variance for'
                                     + ' internal use, e.g. "Shoe size"'))
    description = models.TextField(_("Description"),
                                   blank=True)

    class Meta:
        db_table = 'jimi_variance'
        app_label = 'catalog'

    def __unicode__(self):
        return self.name

    @property
    def label(self):
        if self.internal_name:
            return self.internal_name
        else:
            return self.name


class Variant(models.Model):
    """An instance of varience, such as large or red."""
    name = models.CharField(_("Name"),
                            max_length=255,
                            help_text=_('Name of the variant visible'
                                     + ' for customer, e.g. "red"'))
    internal_name = models.CharField(_("Internal name"),
                            max_length=255,
                            blank=True,
                            help_text=_('Name of the variance for internal'
                                     + ' use, e.g. manufacturer color code'))
    variance = models.ForeignKey(Variance,
                                 help_text=_("Variance the variant"
                                          + " belongs to"))
    active = models.BooleanField(_("Is active"), default=True)

    class Meta:
        db_table = 'jimi_variant'
        app_label = 'catalog'

    def __unicode__(self):
        return self.name

    @property
    def label(self):
        if self.internal_name:
            return self.internal_name
        else:
            return self.name
