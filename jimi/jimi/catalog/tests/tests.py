from django.test import TestCase
from jimi.catalog import models
from jimi.price.fields import Money


class NodeTest(TestCase):
    def test_price(self):
        """Tests that price accumulation works."""
        self.node = models.Node.objects.get(slug__exact="bh")
        self.assertGreaterEqual(self.node.price(), Money())


class CategoryTest(TestCase):
    pass


class ProductTest(TestCase):
    pass
