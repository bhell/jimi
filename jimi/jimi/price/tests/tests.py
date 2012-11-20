from django.test import TestCase
from decimal import Decimal
from jimi.price import fields

# All this is needed for temporary testing models
from django.conf import settings
from django.core.management import call_command
from django.db.models import loading

from models import TestModel


class CurrencyTest(TestCase):
    def test_default_currency(self):
        """Testing if default currency and __eq__() work."""
        self.currency1 = fields.Currency()
        self.currency2 = fields.Currency(fields.DEFAULT_CURRENCY)
        self.assertEqual(self.currency1, self.currency2)

    def test_init(self):
        """Testing if __init__ is sufficiently intelligent."""
        invalid = "ZZZ"
        self.assertRaisesRegexp(ValueError,
                                'Currency %s not defined.' % invalid,
                                fields.Currency,
                                invalid)
        self.assertRaisesRegexp(ValueError,
                                'Currency %s not defined.' % invalid,
                                fields.Currency,
                                code=invalid)

    def test_code_mapping(self):
        """Testing if mapping code to name works"""
        self.currency = fields.Currency()
        self.name = str(self.currency)
        self.assertEqual(self.name, fields.CURRENCIES[fields.DEFAULT_CURRENCY]["code"])


class MoneyTest(TestCase):
    def test_init_without_currency(self):
        """Testing if initialization without currency gives DEFAULT_CURRENCY."""
        self.price = fields.Money(amount=3.14)
        self.currency = fields.Currency()
        self.assertEqual(self.price.currency, self.currency)

    def test_str(self):
        pass  # TODO string conversion

    def test_equality(self):
        """Testing if == works"""
        self.price1 = fields.Money(amount=3.14, currency="USD")
        self.price2 = fields.Money(amount=3.14, currency="USD")
        self.assertEqual(self.price1, self.price2)

    def test_inequality_amount(self):
        """Testing if != works with differing amounts"""
        self.price1 = fields.Money(amount=3.14, currency="USD")
        self.price2 = fields.Money(amount=4.14, currency="USD")
        self.assertNotEqual(self.price1, self.price2)

    def test_inequality_currency(self):
        """Testing if != works with differing currencies"""
        self.price1 = fields.Money(amount=3.14, currency="USD")
        self.price2 = fields.Money(amount=3.14, currency="EUR")
        self.assertNotEqual(self.price1, self.price2)

    def test_pos(self):
        """Testing if __pos__ works"""
        amount = 100
        self.price1 = fields.Money(amount=amount)
        self.price2 = fields.Money(amount=amount)
        self.assertEqual(self.price1, +self.price2)

    def test_neg(self):
        """Testing if __neg__ works"""
        amount = 100
        self.price1 = fields.Money(amount=amount)
        self.price2 = fields.Money(amount=-amount)
        self.assertEqual(self.price1, -self.price2)

    def test_add(self):
        """Testing if __add__ works"""
        amount1 = Decimal("100.01")
        amount2 = Decimal("20000000.01")
        self.price1 = fields.Money(amount=amount1)
        self.price2 = fields.Money(amount=amount2)
        self.assertEqual(self.price1 + self.price2, fields.Money(amount1 + amount2))

    def test_sub(self):
        """Testing if __sub__ works"""
        amount1 = Decimal("100.01")
        amount2 = Decimal("20000000.01")
        self.price1 = fields.Money(amount=amount1)
        self.price2 = fields.Money(amount=amount2)
        self.assertEqual(self.price1 - self.price2, fields.Money(amount1 - amount2))

    def test_mul(self):
        """Testing if __mul__ works"""
        amount1 = Decimal("100.01")
        self.price1 = fields.Money(amount=amount1)
        self.assertEqual(self.price1 * 100, fields.Money(amount1 * Decimal(100)))
        self.assertEqual(100.23 * self.price1, fields.Money(amount1 * Decimal(100.23)))

    def test_div(self):
        """Testing if __div__ works"""
        amount1 = Decimal("100.01")
        self.price1 = fields.Money(amount=amount1)
        self.assertEqual(self.price1 / "100", fields.Money(amount1 / Decimal("100")))
        self.assertEqual(100.23 / self.price1, fields.Money(amount1 / Decimal(100.23)))

    def test_percentage(self):
        r"""Testing if percentage operator % works"""
        self.price = fields.Money(200)
        self.assertAlmostEqual(5 % self.price, fields.Money(amount=10))

    def test_float(self):
        """Testing if casting to float works"""
        amount = 1000000.01
        self.price = fields.Money(amount=amount)
        self.assertAlmostEqual(float(self.price), amount)

    def test_lt(self):
        """Testing if __lt__() works"""
        amount1 = Decimal("1")
        amount2 = Decimal("2")
        self.price1 = fields.Money(amount=amount1)
        self.price2 = fields.Money(amount=amount2)
        self.assertTrue(self.price1 < self.price2)

    def test_lt_different_currencies(self):
        """Testing if __lt__() works with differing currencies"""
        def run_test(price1, price2):
            return price1 < price2

        amount = Decimal("1")
        self.price1 = fields.Money(amount=amount, currency="USD")
        self.price2 = fields.Money(amount=amount, currency="EUR")
        self.assertRaisesRegexp(TypeError,
                                'Cannot compare Money with different currencies.',
                                run_test,
                                price1=self.price1, price2=self.price2)

    def test_gt(self):
        """Testing if __gt__() works"""
        amount1 = Decimal("2")
        amount2 = Decimal("1")
        self.price1 = fields.Money(amount=amount1)
        self.price2 = fields.Money(amount=amount2)
        self.assertTrue(self.price1 > self.price2)

    def test_gt_different_currencies(self):
        """Testing if __gt__() works with differing currencies"""
        def run_test(price1, price2):
            return price1 > price2

        amount = Decimal("1")
        self.price1 = fields.Money(amount=amount, currency="USD")
        self.price2 = fields.Money(amount=amount, currency="EUR")
        self.assertRaisesRegexp(TypeError,
                                'Cannot compare Money with different currencies.',
                                run_test,
                                price1=self.price1, price2=self.price2)

    def test_le(self):
        """Testing if __le__() works"""
        amount1 = Decimal("1")
        amount2 = Decimal("2")
        self.price1 = fields.Money(amount=amount1)
        self.price2 = fields.Money(amount=amount2)
        self.assertTrue(self.price1 <= self.price1)
        self.assertTrue(self.price1 <= self.price2)

    def test_ge(self):
        """Testing if __ge__() works"""
        amount1 = Decimal("2")
        amount2 = Decimal("1")
        self.price1 = fields.Money(amount=amount1)
        self.price2 = fields.Money(amount=amount2)
        self.assertTrue(self.price1 >= self.price1)
        self.assertTrue(self.price1 >= self.price2)

    def test_hash(self):
        pass  # TODO hashing


class MoneyFieldTest(TestCase):
    apps = ("jimi.price.tests",)

    def _pre_setup(self):
        # Add the models to the db.
        self._original_installed_apps = list(settings.INSTALLED_APPS)
        for app in self.apps:
            settings.INSTALLED_APPS += (app,)
        loading.cache.loaded = False
        call_command('syncdb', interactive=False, migrate=False, verbose=0)
        # Call the original method that does the fixtures etc.
        super(MoneyFieldTest, self)._pre_setup()

    def _post_teardown(self):
        # Call the original method.
        super(MoneyFieldTest, self)._post_teardown()
        # Restore the settings.
        settings.INSTALLED_APPS = self._original_installed_apps
        loading.cache.loaded = False

    def setUp(self):
        a = TestModel(ident=1, price=fields.Money(amount="11.11", currency="USD"))
        a.save()
        b = TestModel(ident=2, price=fields.Money(amount="200.02", currency="USD"))
        b.save()

    def test_filter_price(self):
#        res = TestModel.objects.get(price__gt=fields.Money(amount=100, currency="USD"))
        res = TestModel.objects.filter(ident__exact=1)
        self.assertEqual(res[0].price, fields.Money("11.11", "USD"))
