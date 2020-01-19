from rest_framework import serializers
from .models import Store, Item, Purchase, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'price', 'created_at']


class StoreSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    items = ItemSerializer(many=True)
    class Meta:
        model = Store
        fields = ['id', 'name', 'address', 'city', 'items', 'created_by', 'followed_by', 'created_at']



class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['id', 'user', 'item', 'store', 'date_of_purchase', 'paid', 'entry_type']




