from rest_framework import serializers
from .models import Store, Item, Purchase, User, PaymentOutstanding


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',)


class StoreSerializer(serializers.ModelSerializer):
    # followed_by = UserSerializer(many=True)
    class Meta:
        model = Store
        fields = ('id', 'name', 'address', 'city', 'created_by', 'followed_by', 'created_at')


class ItemSerializer(serializers.ModelSerializer):
    # followed_by = UserSerializer(many=True)
    # store = StoreSerializer()
    class Meta:
        model = Item
        fields = ('id', 'name', 'price', 'created_by', 'store', 'followed_by')


class PaymentOutstandingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentOutstanding
        fields = '__all__'


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ('id', 'user', 'item', 'quantity', 'store', 'date_of_purchase', 'entry_type')





