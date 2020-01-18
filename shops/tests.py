from django.test import TestCase

from .models import Store
from .serializers import StoreSerializer

# Create your tests here.


class StoreTest(TestCase):
    """ Test odule for Store Model"""

    def setUp(self):
        Store.objects.create(
            name='Bakia Nathan', address='Indiranagar', city='Bangalore'
        )
        Store.objects.create(
            name='Juice shop', address='Bellandur', city='Bangalore'
        )

    def test_store_city(self):
        store_bakia_nathan = Store.objects.get(name='Bakia Nathan')
        store_juice_shop = Store.objects.get(name='Juice shop')
        self.assertEqual(store_bakia_nathan.city, store_juice_shop.city)