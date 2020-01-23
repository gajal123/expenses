from copy import copy

from django.contrib.auth import authenticate
from django.shortcuts import render
from django.db import transaction
from django.http import Http404
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Store, Item, Purchase, User, PaymentOutstanding
from .serializers import StoreSerializer, ItemSerializer, PurchaseSerializer, PaymentOutstandingSerializer


class StoreListView(APIView):

    def get(self, request, *args, **kwargs):
        all_stores = Store.objects.filter()
        serializer = StoreSerializer(all_stores, many=True)
        for store in serializer.data:
            items = Item.objects.filter(store__id=store['id'])
            item_serializer = ItemSerializer(items, many=True)
            store['outstanding_amount'] = 0
            store['items'] = item_serializer.data

            payment_outstanding = PaymentOutstanding.objects.filter(store=store['id'], user=request.user.id)
            if payment_outstanding:
                store['outstanding_amount'] = payment_outstanding[0].amount
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
                payment_serializer = PaymentOutstandingSerializer(data={'user': request.user.id, 'store': serializer.data['id'], 'amount': outstanding_amount})
                if payment_serializer.is_valid():
                    payment_serializer.save()
                else:
                    print(payment_serializer.errors)
                    return Response({'error': payment_serializer.errors})
                return Response(serializer.data)
            print(serializer.errors)
            return Response({'error': serializer.errors})

        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StoreDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Store.objects.get(pk=pk)
        except Store.DoesNotExist:
            raise Http404


    def get(self, request, pk, format=None):
        store = self.get_object(pk)
        serializer = StoreSerializer(store)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        data = request.data
        user = request.user.id

        store = self.get_object(pk)
        user_obj = User.objects.get(id=user)
        if data.get('add_user'):
            store.followed_by.add(user_obj)
        if data.get('remove_user'):
            store.followed_by.remove(user_obj)

        serializer = StoreSerializer(store, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)
        return Response({'error': serializer.errors})


class ItemListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        items = Item.objects.filter()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            data['created_by'] = request.user.id
            data['followed_by'] = [request.user.id]
            item_serializer = ItemSerializer(data=data)
            if item_serializer.is_valid():
                item_serializer.save()
                return Response(item_serializer.data, status=status.HTTP_200_OK)
            print(item_serializer.errors)
            return Response({'error': 'Item already exists', 'info': item_serializer.errors},
                            status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PurchaseItem(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        purchases = Purchase.objects.filter(user=request.user.id)
        serializer = PurchaseSerializer(purchases, many=True)

        return Response(serializer.data)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            data['user'] = request.user.id
            data['entry_type'] = data.get('entry_type', 'purchase')

            amount = data['amount'] * int(data.get('quantity', 1))
            payment = PaymentOutstanding.objects.get(user=data['user'], store=data['store'])
            payment.amount = payment.amount + amount
            payment.save()

            purchase_serializer = PurchaseSerializer(data=data)
            if purchase_serializer.is_valid():
                purchase_serializer.save()
                serialized_data = copy(purchase_serializer.data)
                serialized_data.update({'outstanding_amount': payment.amount})
                return Response(serialized_data, status=status.HTTP_201_CREATED)
            print(purchase_serializer.errors)
            return Response(purchase_serializer.errors, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserPayments(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            amount = int(data['amount'])
            user = User.objects.get(pk=request.user.id)
            store = Store.objects.get(pk=data['store'])
            payment_outstanding = PaymentOutstanding.objects.get(user=user, store=data['store'])
            payment_outstanding.amount -= amount
            payment_outstanding.save()
            Purchase.objects.create(user=user, store=store, entry_type='payment')
            return Response({'outstanding_amount': payment_outstanding.amount}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PaymenOutstandingViewSet(viewsets.ModelViewSet):
    queryset = PaymentOutstanding.objects.all()
    serializer_class = PaymentOutstandingSerializer


def index(request):
    return render(request, 'login.html')


def stores(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        print('logging in user')
        return render(request, 'stores.html', {'username': username, 'password': password, 'user_id': user.id})
    return render(request, 'login.html', {'error': 'Invalid Username/password'})


def stores_detail(request, store_id):
    auth_token = request.GET.get('auth_token')
    return render(request, 'stores_detail.html', {'auth_token': auth_token, 'user_id': request.user.id, 'store_id': store_id})