from .models import Store, Item, Purchase
from .serializers import StoreSerializer, ItemSerializer, PurchaseSerializer
from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

class StoreViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer