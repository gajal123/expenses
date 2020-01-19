import rest_framework.response

from .models import Store, Item, Purchase, User
from .serializers import StoreSerializer, ItemSerializer, PurchaseSerializer
from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.models import TokenUser

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer


class UserStores(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        stores = Store.objects.filter(followed_by=request.user.id)
        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data)


def stores(request):
    return render(request, 'stores.html')

def index(request):
    return render(request, 'index.html')