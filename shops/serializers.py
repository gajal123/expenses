from rest_framework import serializers
from .models import Store, Item, Purchase, User, PaymentOutstanding


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'price', 'created_by')


class StoreSerializer(serializers.ModelSerializer):
    # items = ItemSerializer(many=True)
    class Meta:
        model = Store
        fields = '__all__'


class PaymentOutstandingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentOutstanding
        fields = '__all__'


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ('id', 'user', 'item', 'quantity', 'store', 'date_of_purchase', 'entry_type')





