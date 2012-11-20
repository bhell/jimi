from django.db import models
from decimal import Decimal
from django.utils.translation import ugettext as _

from django.conf import settings
if not hasattr(settings, 'SHOP_CURRENCY'):
    DEFAULT_CURRENCY = {"code": "USD", "name": _("US Dollar"), "abbr": "$"}
DEFAULT_CURRENCY = settings.SHOP_CURRENCY


class Currency(object):
    """Currency: ISO code, name and abbreviation"""
    def __init__(self, code="", name="", abbr=""):
        if code:
            self.code = code
        else:
            self.code = DEFAULT_CURRENCY["code"]
        if name:
            self.name = name
        else:
            self.name = DEFAULT_CURRENCY["name"]
        if abbr:
            self.abbr = abbr
        else:
            self.abbr = DEFAULT_CURRENCY["abbr"]

    def __repr__(self):
        return self.code

    def __unicode__(self):
        return u"%s" % self.name


class Money(object):
    """Money: Amount and currency"""
    def __init__(self, amount=Decimal('0.0'), currency=None):
        if not isinstance(amount, Decimal):
            amount = Decimal(str(amount))
        self.amount = amount
        if currency is None:
            currency = Currency()
        elif not isinstance(currency, Currency):
            currency = Currency(code=currency.upper())
            # TODO lookup name and abbr
        self.currency = currency

    def __unicode__(self):
        return u"%s %s" % (self.price, self.currency)


class MoneyField(models.Field):
    """Money stored in Django database"""
    description = "Money: Amount and currency"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 104
        super(MoneyField, self).__init__(*args, **kwargs)
