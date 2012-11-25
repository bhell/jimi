from django.db import models
from django.utils.translation import ugettext as _
from south.signals import pre_migrate
from django.dispatch import receiver
from django_countries.countries import COUNTRIES
import os.path


@receiver(pre_migrate)
def prepare_country_initial_data(sender, **kwargs):
    """Set up initial data fixture for Countries"""
    f = open(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          "../fixtures/initial_data.yaml")), "w")
    f.write("- model: price.Country\n")
    for c in COUNTRIES:
        f.write("  code: %s\n" % c[0])
        f.write("  fields:\n")
        f.write("    name: %s\n" % unicode(c[1]).encode('utf-8'))


class Country(models.Model):
    code = models.CharField(_("ISO 2 letter country code"), max_length=2, primary_key=True)
    name = models.CharField(_("Country name"), max_length=255)

    class Meta:
        ordering = ['name']
        verbose_name_plural = _('Countries')
        app_label = 'price'

    def __unicode__(self):
        return self.name


class Tax(models.Model):
    name = models.CharField(_("Name"), max_length=128)
    description = models.TextField(_("Description"), blank=True)
    percent = models.DecimalField(_("Percent"),
                                  max_digits=3,
                                  decimal_places=2,
                                  help_text=_("Tax percentage, typically ranging from 0 to 100."))
    region = models.ManyToManyField(Country, db_table="price_tax_valid_in_country")

    class Meta:
        ordering = ['name']
        verbose_name_plural = _("Taxes")
        app_label = 'price'

    def __unicode__(self):
        return "%s (%s%%)" % (self.name, self.percent)

    def factor(self):
        return self.percent / 100.0
