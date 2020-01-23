from django.test import TestCase

from .models import Store
from .serializers import StoreSerializer

# Create your tests here.


class StoreTest(TestCase):
    """ Test module for Store Model"""

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


class StoreSerializerTest(TestCase):
    """

    """
    def setUp(self):
        self.juice_shop = Store.objects.create(
            name='Juice shop', address='Bellandur', city='Bangalore'
        )
        self.serializer = StoreSerializer(self.juice_shop)

    def test(self):
        self.assertEqual(self.serializer.data.get('address'), self.juice_shop.address)
