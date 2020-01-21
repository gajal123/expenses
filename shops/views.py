import json
from .models import Store, Item, Purchase, User, PaymentOutstanding
from .serializers import StoreSerializer, ItemSerializer, PurchaseSerializer, PaymentOutstandingSerializer
from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import F
from copy import copy
from rest_framework import status
from django.db import transaction

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class UserItem(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,  *args, **kwargs):
        purchases = Item.objects.filter(user=request.user.id)
        serializer = ItemSerializer(purchases, many=True)
        return Response(serializer.data)

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            data['created_by'] = request.user.id
            item_serializer = ItemSerializer(data=data)
            store = Store.objects.filter(pk=data['store'], items__name=data['name'], items__price=data['price'])
            saved = False
            if item_serializer.is_valid():
                item_serializer.save()
                saved = True
            if not store:
                item = Item.objects.get(name=data['name'], price=data['price'])
                Store.objects.get(pk=data['store']).items.add(item)
                saved = True
            if saved:
                return Response(item_serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "item already exists"}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PurchaseItem(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,  *args, **kwargs):
        purchases = Purchase.objects.filter(user=request.user.id)
        serializer = PurchaseSerializer(purchases, many=True)

        return Response(serializer.data)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            data['user'] = request.user.id
            data['entry_type'] = data.get('entry_type', 'purchase')
            data['payment_outstanding_model'] = {'user': request.user.id, 'store': data['store']}
            purchase_serializer = PurchaseSerializer(data=data)
            user = User.objects.get(id=request.user.id)
            store = Store.objects.get(id=data['store'])
            amount = data['amount'] * int(data.get('quantity', 1))
            payment_outstanding, created = PaymentOutstanding.objects.get_or_create(user=user, store=store)
            payment_outstanding.amount += amount
            payment_outstanding.save()

            if purchase_serializer.is_valid():
                purchase_serializer.save()
                serialized_data = copy(purchase_serializer.data)
                serialized_data.update({'outstanding_amount': payment_outstanding.amount})
                return Response(serialized_data, status=status.HTTP_201_CREATED)
            return Response(purchase_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserStores(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        stores = Store.objects.filter(followed_by=request.user.id)
        serializer = StoreSerializer(stores, many=True)
        for store in serializer.data:
            store['outstanding_amount'] = 0
            payment_outstanding = PaymentOutstanding.objects.filter(store=store['id'], user=request.user.id)
            if payment_outstanding:
                store['outstanding_amount'] = payment_outstanding[0].amount

            for idx, item_id in enumerate(store.get('items')):
                item = Item.objects.get(pk=item_id)
                item_serializer = ItemSerializer(item)
                store['items'][idx] = item_serializer.data
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            data['created_by'] = request.user.id
            data['followed_by'] = [request.user.id]
            outstanding_amount = data['outstanding_amount']
            serializer = StoreSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                if outstanding_amount:
                    PaymentOutstanding.objects.create(user=User.objects.get(pk=request.user.id), store=Store.objects.get(pk=serializer.data['id']), amount=outstanding_amount)
            else:
                print(serializer.errors)
                return Response({'error': serializer.errors})
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



def stores(request):
    return render(request, 'stores.html')

def index(request):
    return render(request, 'index.html')