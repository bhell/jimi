# -*- coding: utf-8 -*-
from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation
from django.utils.translation import ugettext as _

from django.utils.encoding import python_2_unicode_compatible, force_text


CURRENCIES = {
              "AED": {"code": 'AED', "name": _('UAE Dirham'), "abbr": ""},
              "AFN": {"code": 'AFN', "name": _('Afghani'), "abbr": ""},
              "ALL": {"code": 'ALL', "name": _('Lek'), "abbr": ""},
              "AMD": {"code": 'AMD', "name": _('Armenian Dram'), "abbr": ""},
              "ANG": {"code": 'ANG', "name": _('Netherlands Antillian Guilder'), "abbr": ""},
              "AOA": {"code": 'AOA', "name": _('Kwanza'), "abbr": ""},
              "ARS": {"code": 'ARS', "name": _('Argentine Peso'), "abbr": ""},
              "AUD": {"code": 'AUD', "name": _('Australian Dollar'), "abbr": ""},
              "AWG": {"code": 'AWG', "name": _('Aruban Guilder'), "abbr": ""},
              "AZN": {"code": 'AZN', "name": _('Azerbaijanian Manat'), "abbr": ""},
              "BAM": {"code": 'BAM', "name": _('Convertible Marks'), "abbr": ""},
              "BBD": {"code": 'BBD', "name": _('Barbados Dollar'), "abbr": ""},
              "BDT": {"code": 'BDT', "name": _('Taka'), "abbr": ""},
              "BGN": {"code": 'BGN', "name": _('Bulgarian Lev'), "abbr": ""},
              "BHD": {"code": 'BHD', "name": _('Bahraini Dinar'), "abbr": ""},
              "BIF": {"code": 'BIF', "name": _('Burundi Franc'), "abbr": ""},
              "BMD": {"code": 'BMD', "name": _('Bermudian Dollar'), "abbr": ""},
              "BND": {"code": 'BND', "name": _('Brunei Dollar'), "abbr": ""},
              "BOB": {"code": 'BOB', "name": _('Boliviano'), "abbr": ""},
              "BRL": {"code": 'BRL', "name": _('Brazilian Real'), "abbr": ""},
              "BSD": {"code": 'BSD', "name": _('Bahamian Dollar'), "abbr": ""},
              "BTN": {"code": 'BTN', "name": _('Bhutanese ngultrum'), "abbr": ""},
              "BWP": {"code": 'BWP', "name": _('Pula'), "abbr": ""},
              "BYR": {"code": 'BYR', "name": _('Belarussian Ruble'), "abbr": ""},
              "BZD": {"code": 'BZD', "name": _('Belize Dollar'), "abbr": ""},
              "CAD": {"code": 'CAD', "name": _('Canadian Dollar'), "abbr": ""},
              "CDF": {"code": 'CDF', "name": _('Congolese franc'), "abbr": ""},
              "CHF": {"code": 'CHF', "name": _('Swiss Franc'), "abbr": ""},
              "CLP": {"code": 'CLP', "name": _('Chilean peso'), "abbr": ""},
              "CNY": {"code": 'CNY', "name": _('Yuan Renminbi'), "abbr": ""},
              "COP": {"code": 'COP', "name": _('Colombian peso'), "abbr": ""},
              "CRC": {"code": 'CRC', "name": _('Costa Rican Colon'), "abbr": ""},
              "CUC": {"code": 'CUC', "name": _('Cuban convertible peso'), "abbr": ""},
              "CUP": {"code": 'CUP', "name": _('Cuban Peso'), "abbr": ""},
              "CVE": {"code": 'CVE', "name": _('Cape Verde Escudo'), "abbr": ""},
              "CZK": {"code": 'CZK', "name": _('Czech Koruna'), "abbr": ""},
              "DJF": {"code": 'DJF', "name": _('Djibouti Franc'), "abbr": ""},
              "DKK": {"code": 'DKK', "name": _('Danish Krone'), "abbr": ""},
              "DOP": {"code": 'DOP', "name": _('Dominican Peso'), "abbr": ""},
              "DZD": {"code": 'DZD', "name": _('Algerian Dinar'), "abbr": ""},
              "EGP": {"code": 'EGP', "name": _('Egyptian Pound'), "abbr": ""},
              "ERN": {"code": 'ERN', "name": _('Nakfa'), "abbr": ""},
              "ETB": {"code": 'ETB', "name": _('Ethiopian Birr'), "abbr": ""},
              "EUR": {"code": 'EUR', "name": _('Euro'), "abbr": "€"},
              "FJD": {"code": 'FJD', "name": _('Fiji Dollar'), "abbr": ""},
              "FKP": {"code": 'FKP', "name": _('Falkland Islands Pound'), "abbr": ""},
              "GBP": {"code": 'GBP', "name": _('Pound Sterling'), "abbr": ""},
              "GEL": {"code": 'GEL', "name": _('Lari'), "abbr": ""},
              "GHS": {"code": 'GHS', "name": _('Ghana Cedi'), "abbr": ""},
              "GIP": {"code": 'GIP', "name": _('Gibraltar Pound'), "abbr": ""},
              "GMD": {"code": 'GMD', "name": _('Dalasi'), "abbr": ""},
              "GNF": {"code": 'GNF', "name": _('Guinea Franc'), "abbr": ""},
              "GTQ": {"code": 'GTQ', "name": _('Quetzal'), "abbr": ""},
              "GYD": {"code": 'GYD', "name": _('Guyana Dollar'), "abbr": ""},
              "HKD": {"code": 'HKD', "name": _('Hong Kong Dollar'), "abbr": ""},
              "HNL": {"code": 'HNL', "name": _('Lempira'), "abbr": ""},
              "HRK": {"code": 'HRK', "name": _('Croatian Kuna'), "abbr": ""},
              "HTG": {"code": 'HTG', "name": _('Haitian gourde'), "abbr": ""},
              "HUF": {"code": 'HUF', "name": _('Forint'), "abbr": ""},
              "IDR": {"code": 'IDR', "name": _('Rupiah'), "abbr": ""},
              "ILS": {"code": 'ILS', "name": _('New Israeli Sheqel'), "abbr": ""},
              "IMP": {"code": 'IMP', "name": _('Isle of Man pount'), "abbr": ""},
              "INR": {"code": 'INR', "name": _('Indian Rupee'), "abbr": ""},
              "IQD": {"code": 'IQD', "name": _('Iraqi Dinar'), "abbr": ""},
              "IRR": {"code": 'IRR', "name": _('Iranian Rial'), "abbr": ""},
              "ISK": {"code": 'ISK', "name": _('Iceland Krona'), "abbr": ""},
              "JMD": {"code": 'JMD', "name": _('Jamaican Dollar'), "abbr": ""},
              "JOD": {"code": 'JOD', "name": _('Jordanian Dinar'), "abbr": ""},
              "JPY": {"code": 'JPY', "name": _('Yen'), "abbr": ""},
              "KES": {"code": 'KES', "name": _('Kenyan Shilling'), "abbr": ""},
              "KGS": {"code": 'KGS', "name": _('Som'), "abbr": ""},
              "KHR": {"code": 'KHR', "name": _('Riel'), "abbr": ""},
              "KMF": {"code": 'KMF', "name": _('Comoro Franc'), "abbr": ""},
              "KPW": {"code": 'KPW', "name": _('North Korean Won'), "abbr": ""},
              "KRW": {"code": 'KRW', "name": _('Won'), "abbr": ""},
              "KWD": {"code": 'KWD', "name": _('Kuwaiti Dinar'), "abbr": ""},
              "KYD": {"code": 'KYD', "name": _('Cayman Islands Dollar'), "abbr": ""},
              "KZT": {"code": 'KZT', "name": _('Tenge'), "abbr": ""},
              "LAK": {"code": 'LAK', "name": _('Kip'), "abbr": ""},
              "LBP": {"code": 'LBP', "name": _('Lebanese Pound'), "abbr": ""},
              "LKR": {"code": 'LKR', "name": _('Sri Lanka Rupee'), "abbr": ""},
              "LRD": {"code": 'LRD', "name": _('Liberian Dollar'), "abbr": ""},
              "LSL": {"code": 'LSL', "name": _('Lesotho loti'), "abbr": ""},
              "LTL": {"code": 'LTL', "name": _('Lithuanian Litas'), "abbr": ""},
              "LVL": {"code": 'LVL', "name": _('Latvian Lats'), "abbr": ""},
              "LYD": {"code": 'LYD', "name": _('Libyan Dinar'), "abbr": ""},
              "MAD": {"code": 'MAD', "name": _('Moroccan Dirham'), "abbr": ""},
              "MDL": {"code": 'MDL', "name": _('Moldovan Leu'), "abbr": ""},
              "MGA": {"code": 'MGA', "name": _('Malagasy Ariary'), "abbr": ""},
              "MKD": {"code": 'MKD', "name": _('Denar'), "abbr": ""},
              "MMK": {"code": 'MMK', "name": _('Kyat'), "abbr": ""},
              "MNT": {"code": 'MNT', "name": _('Tugrik'), "abbr": ""},
              "MOP": {"code": 'MOP', "name": _('Pataca'), "abbr": ""},
              "MRO": {"code": 'MRO', "name": _('Ouguiya'), "abbr": ""},
              "MUR": {"code": 'MUR', "name": _('Mauritius Rupee'), "abbr": ""},
              "MVR": {"code": 'MVR', "name": _('Rufiyaa'), "abbr": ""},
              "MWK": {"code": 'MWK', "name": _('Kwacha'), "abbr": ""},
              "MXN": {"code": 'MXN', "name": _('Mexixan peso'), "abbr": ""},
              "MYR": {"code": 'MYR', "name": _('Malaysian Ringgit'), "abbr": ""},
              "MZN": {"code": 'MZN', "name": _('Metical'), "abbr": ""},
              "NAD": {"code": 'NAD', "name": _('Namibian Dollar'), "abbr": ""},
              "NGN": {"code": 'NGN', "name": _('Naira'), "abbr": ""},
              "NIO": {"code": 'NIO', "name": _('Cordoba Oro'), "abbr": ""},
              "NOK": {"code": 'NOK', "name": _('Norwegian Krone'), "abbr": ""},
              "NPR": {"code": 'NPR', "name": _('Nepalese Rupee'), "abbr": ""},
              "NZD": {"code": 'NZD', "name": _('New Zealand Dollar'), "abbr": ""},
              "OMR": {"code": 'OMR', "name": _('Rial Omani'), "abbr": ""},
              "PAB": {"code": 'PAB', "name": _('Panamanian Balboa'), "abbr": ""},
              "PEN": {"code": 'PEN', "name": _('Nuevo Sol'), "abbr": ""},
              "PGK": {"code": 'PGK', "name": _('Kina'), "abbr": ""},
              "PHP": {"code": 'PHP', "name": _('Philippine Peso'), "abbr": ""},
              "PKR": {"code": 'PKR', "name": _('Pakistan Rupee'), "abbr": ""},
              "PLN": {"code": 'PLN', "name": _('Zloty'), "abbr": ""},
              "PYG": {"code": 'PYG', "name": _('Guarani'), "abbr": ""},
              "QAR": {"code": 'QAR', "name": _('Qatari Rial'), "abbr": ""},
              "RON": {"code": 'RON', "name": _('New Leu'), "abbr": ""},
              "RSD": {"code": 'RSD', "name": _('Serbian Dinar'), "abbr": ""},
              "RUB": {"code": 'RUB', "name": _('Russian Ruble'), "abbr": ""},
              "RWF": {"code": 'RWF', "name": _('Rwanda Franc'), "abbr": ""},
              "SAR": {"code": 'SAR', "name": _('Saudi Riyal'), "abbr": ""},
              "SBD": {"code": 'SBD', "name": _('Solomon Islands Dollar'), "abbr": ""},
              "SCR": {"code": 'SCR', "name": _('Seychelles Rupee'), "abbr": ""},
              "SDG": {"code": 'SDG', "name": _('Sudanese Pound'), "abbr": ""},
              "SEK": {"code": 'SEK', "name": _('Swedish Krona'), "abbr": "kr"},
              "SGD": {"code": 'SGD', "name": _('Singapore Dollar'), "abbr": ""},
              "SHP": {"code": 'SHP', "name": _('Saint Helena Pound'), "abbr": ""},
              "SKK": {"code": 'SKK', "name": _('Slovak Koruna'), "abbr": ""},
              "SLL": {"code": 'SLL', "name": _('Leone'), "abbr": ""},
              "SOS": {"code": 'SOS', "name": _('Somali Shilling'), "abbr": ""},
              "SRD": {"code": 'SRD', "name": _('Surinam Dollar'), "abbr": ""},
              "STD": {"code": 'STD', "name": _('Dobra'), "abbr": ""},
              "SVC": {"code": 'SVC', "name": _('Salvadoran Colon'), "abbr": ""},
              "SYP": {"code": 'SYP', "name": _('Syrian Pound'), "abbr": ""},
              "SZL": {"code": 'SZL', "name": _('Lilangeni'), "abbr": ""},
              "THB": {"code": 'THB', "name": _('Baht'), "abbr": ""},
              "TJS": {"code": 'TJS', "name": _('Somoni'), "abbr": ""},
              "TMM": {"code": 'TMM', "name": _('Manat'), "abbr": ""},
              "TND": {"code": 'TND', "name": _('Tunisian Dinar'), "abbr": ""},
              "TOP": {"code": 'TOP', "name": _('Paanga'), "abbr": ""},
              "TRY": {"code": 'TRY', "name": _('New Turkish Lira'), "abbr": ""},
              "TTD": {"code": 'TTD', "name": _('Trinidad and Tobago Dollar'), "abbr": ""},
              "TVD": {"code": 'TVD', "name": _('Tuvalu dollar'), "abbr": ""},
              "TWD": {"code": 'TWD', "name": _('New Taiwan Dollar'), "abbr": ""},
              "TZS": {"code": 'TZS', "name": _('Tanzanian Shilling'), "abbr": ""},
              "UAH": {"code": 'UAH', "name": _('Hryvnia'), "abbr": ""},
              "UGX": {"code": 'UGX', "name": _('Uganda Shilling'), "abbr": ""},
              "USD": {"code": 'USD', "name": _('US Dollar'), "abbr": "$"},
              "UYU": {"code": 'UYU', "name": _('Uruguayan peso'), "abbr": ""},
              "UZS": {"code": 'UZS', "name": _('Uzbekistan Sum'), "abbr": ""},
              "VEB": {"code": 'VEB', "name": _('Venezuelan bolivar'), "abbr": ""},
              "VEF": {"code": 'VEF', "name": _('Bolivar Fuerte'), "abbr": ""},
              "VND": {"code": 'VND', "name": _('Dong'), "abbr": ""},
              "VUV": {"code": 'VUV', "name": _('Vatu'), "abbr": ""},
              "WST": {"code": 'WST', "name": _('Tala'), "abbr": ""},
              "XAF": {"code": 'XAF', "name": _('CFA franc BEAC'), "abbr": ""},
              "XAG": {"code": 'XAG', "name": _('Silver'), "abbr": ""},
              "XAU": {"code": 'XAU', "name": _('Gold'), "abbr": ""},
              "XBA": {"code": 'XBA', "name": _('Bond Markets Units European Composite Unit (EURCO)'), "abbr": ""},
              "XBB": {"code": 'XBB', "name": _('European Monetary Unit (E.M.U.-6)'), "abbr": ""},
              "XBC": {"code": 'XBC', "name": _('European Unit of Account 9(E.U.A.-9)'), "abbr": ""},
              "XBD": {"code": 'XBD', "name": _('European Unit of Account 17(E.U.A.-17)'), "abbr": ""},
              "XCD": {"code": 'XCD', "name": _('East Caribbean Dollar'), "abbr": ""},
              "XDR": {"code": 'XDR', "name": _('SDR'), "abbr": ""},
              "XFO": {"code": 'XFO', "name": _('Gold-Franc'), "abbr": ""},
              "XFU": {"code": 'XFU', "name": _('UIC-Franc'), "abbr": ""},
              "XOF": {"code": 'XOF', "name": _('CFA Franc BCEAO'), "abbr": ""},
              "XPD": {"code": 'XPD', "name": _('Palladium'), "abbr": ""},
              "XPF": {"code": 'XPF', "name": _('CFP Franc'), "abbr": ""},
              "XPT": {"code": 'XPT', "name": _('Platinum'), "abbr": ""},
              "XTS": {"code": 'XTS', "name": _('Codes specifically reserved for testing purposes'), "abbr": ""},
              "YER": {"code": 'YER', "name": _('Yemeni Rial'), "abbr": ""},
              "ZAR": {"code": 'ZAR', "name": _('Rand'), "abbr": ""},
              "ZMK": {"code": 'ZMK', "name": _('Kwacha'), "abbr": ""},
              "ZWD": {"code": 'ZWD', "name": _('Zimbabwe Dollar A/06'), "abbr": ""},
              "ZWL": {"code": 'ZWL', "name": _('Zimbabwe dollar A/09'), "abbr": ""},
              "ZWN": {"code": 'ZWN', "name": _('Zimbabwe dollar A/08'), "abbr": ""},
}

from django.conf import settings
if not hasattr(settings, 'SHOP_CURRENCY'):
    DEFAULT_CURRENCY = CURRENCIES["USD"]
DEFAULT_CURRENCY = settings.SHOP_CURRENCY


@python_2_unicode_compatible
class Currency(object):
    """Currency: ISO code, name and abbreviation"""
    def __init__(self, *args, **kwargs):
        self.code = None
        if len(args) == 1:
            try:
                _c = str(args[0]).upper()
                self.code = CURRENCIES[_c]["code"]
                self.name = CURRENCIES[self.code]["name"]
                self.abbr = CURRENCIES[self.code]["abbr"] or self.code
            except:
                raise ValueError("Currency %s not defined." % args[0])
        elif len(args) > 1:
            raise ValueError("Cannot figure out how to convert %s to currency." % args)
        else:  # len(args) == 0
            if kwargs:
                if "code" in kwargs:
                    _c = kwargs["code"].upper()
                    if _c in CURRENCIES:
                        self.code = CURRENCIES[_c]["code"]
                        self.name = CURRENCIES[self.code]["name"]
                        self.abbr = CURRENCIES[self.code]["abbr"] or self.code
                    else:
                        raise ValueError("Currency %s not defined." % kwargs["code"])
            else:
                self.code = DEFAULT_CURRENCY
                self.name = CURRENCIES[self.code]["name"]
                self.abbr = CURRENCIES[self.code]["abbr"] or self.code
        if not self.code:
            raise ValueError("Could not figure out what currency this is supposed to be: %s %s" % (args, kwargs))

    def __repr__(self):
        return force_text(self.code)

    def __str__(self):
        return force_text(self.code)

    def __eq__(self, other):
        return (isinstance(other, Currency) and
                self.code == other.code)

    def __ne__(self, other):
        result = self.__eq__(other)
        return not result


@python_2_unicode_compatible
class Money(object):
    """Money: Amount and currency.

    Some inspiration and code taken from python-money,
    https://bitbucket.org/acoobe/python-money/"""
    # def old__init__(self, amount=Decimal('0.0'), currency=None):
    #     if not isinstance(amount, Decimal):
    #         amount = Decimal(str(amount))
    #     self.amount = amount
    #     if currency is None:
    #         self.currency = Currency()
    #     elif not isinstance(currency, Currency):
    #         self.currency = Currency(code=currency.upper())
    #     else:
    #         self.currency = currency

    def __init__(self, *args, **kwargs):
        self.amount = None
        self.currency = None
        if len(args) == 1:
            if isinstance(args[0], Money):
                self.amount = args[0].amount
                self.currency = args[0].currency
                return
            else:
                try:  # to convert to Decimal amount
                    self.amount = Decimal(args[0])
                except InvalidOperation:
                    if len(args[0] == 2):
                        args = (args[0][0], args[0][1])
                    else:
                        try:
                            _new = ("", "")
                            _new[0], _new[1] = args[0].split()
                            args = _new
                        except ValueError:
                            raise ValueError("Cannot figure out how to convert %s to Money." % args[0])
        if len(args) == 2:
            try:
                self.amount = Decimal(args[0])
                self.currency = Currency(args[1])
                return
            except InvalidOperation, ValueError:
                try:  # the other way round
                    self.amount = Decimal(args[1])
                    self.currency = Currency(args[0])
                    return
                except InvalidOperation, ValueError:
                    raise ValueError("Cannot figure out how to convert %s to Money." % args)
        if len(args) > 2:
            raise ValueError("Cannot figure out how to convert %s to Money." % args)
        if "amount" in kwargs:
            self.amount = Decimal(kwargs["amount"])
        if "currency" in kwargs:
            self.currency = Currency(kwargs["currency"])
        elif "code" in kwargs:
            self.currency = Currency(kwargs["code"])

        if not isinstance(self.amount, Decimal):
            self.amount = Decimal("0.0")
        if not isinstance(self.currency, Currency):
            self.currency = Currency()

    def __repr__(self):
        return force_text("Money(%s %s)" % (self.currency, self.amount))

    def __str__(self):
        return force_text("%s %s" % (self.currency, self.amount))

    def __eq__(self, other):
        # Allow comparison to 0
        if (other == 0) and (self.amount == 0):
            return True
        return (isinstance(other, Money) and
                self.amount == other.amount and
                self.currency == other.currency)

    def __ne__(self, other):
        result = self.__eq__(other)
        return not result

    def __pos__(self):
        return Money(amount=self.amount, currency=self.currency)

    def __neg__(self):
        return Money(amount=-self.amount, currency=self.currency)

    def __add__(self, other):
        if not isinstance(other, Money):
            raise TypeError('Cannot add or subtract a ' +
                            'Money (%s) and non-Money (type(%s) == %s) instance.' % (self, other, type(other)))
        if self.currency == other.currency:
            return Money(
                amount=self.amount + other.amount,
                currency=self.currency)
        raise TypeError('Cannot add or subtract two Money ' +
                        'instances with different currencies.')

    def __sub__(self, other):
        return self.__add__(-other)

    def __mul__(self, other):
        if isinstance(other, Money):
            raise TypeError('Cannot multiply two Money instances.')
        return Money(amount=self.amount * Decimal(other), currency=self.currency)

    def __div__(self, other):
        if isinstance(other, Money):
            raise TypeError('Cannot divide two Money instances.')
        return Money(amount=self.amount / Decimal(other), currency=self.currency)

    def __rmod__(self, other):
        """
        Calculate percentage of an amount.  The left-hand side of the
        operator must be a numeric value.

        Example:
        >>> money = Money(200, 'USD')
        >>> 5 % money
        USD 10.00
        """
        if isinstance(other, Money):
            raise TypeError('Invalid __rmod__ operation')
        else:
            return Money(amount=Decimal(str(other)) * self.amount / 100,
                         currency=self.currency)

    def __float__(self):
        return float(self.amount)

    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__
    __rdiv__ = __div__

    def __lt__(self, other):
        if isinstance(other, Money):
            if (self.currency == other.currency):
                return (self.amount < other.amount)
            else:
                raise TypeError('Cannot compare Money with different currencies.')
        else:
            return (self.amount < Decimal(str(other)))

    def __gt__(self, other):
        if isinstance(other, Money):
            if (self.currency == other.currency):
                return (self.amount > other.amount)
            else:
                raise TypeError('Cannot compare Money with different currencies.')
        else:
            return (self.amount > Decimal(str(other)))

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other

    def __hash__(self):
        return self.__repr__


class MoneyField(models.CharField):
    """Money stored in Django database"""
    empty_strings_allowed = False
    default_error_messages = {
        'invalid_format': _("'%s' value has an invalid format. It must be "
                            "in XXXX.XX YYY format, with max 17 significant figures X "
                            "and a valid currency code YYY."),
        'invalid_amount': _("'%s' value has the correct format "
                          "but it has an invalid amount."),
        'invalid_currency': _("'%s' value has the correct format "
                          "but it has an invalid currency code."),
        }
    description = "Money: Amount and currency"

    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 21  # up to 999999999999.99 XXX
        super(MoneyField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, Money):
            return value
        try:
            c, a = value.split(" ")
        except ValueError:
            msg = self.error_messages['invalid_format'] % value
            raise ValidationError(msg)
        except AttributeError:  # NoneType cannot be split
            return None
        try:
            amount = Decimal(a)
        except InvalidOperation:
            msg = self.error_messages['invalid_amount'] % value
            raise ValidationError(msg)
        if amount > Decimal("999999999999999.99"):
            msg = self.error_messages['invalid_amount'] % value
            raise ValidationError(msg)
        try:
            currency = CURRENCIES[c.upper()]['code']
        except:
            msg = self.error_messages['invalid_currency'] % value
            raise ValidationError(msg)
        return Money(amount=Decimal(amount), currency=Currency(currency))

    def value_to_string(self, obj):
        val = self._get_val_from_obj(obj)
        return self.get_prep_value(val)

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^jimi\.price\.fields\.MoneyField"])
