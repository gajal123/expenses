from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    class Meta:
        db_table = 'users'


class Store(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    items = models.ManyToManyField("Item", related_name='stores')
    created_by = models.ForeignKey(User, related_name='created_stores', null=True, on_delete=models.SET_NULL)
    followed_by = models.ManyToManyField(User, related_name='followed_stores')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'stores'

    def __str__(self):
        return f"Name: {self.name}\n City: {self.city}\n Items: {self.items}"


class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_item', null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'items'
        unique_together = (('name', 'price'),)

    def __str__(self):
        return f" name: {self.name}. Price: {self.price}"

class Purchase(models.Model):
    user = models.ForeignKey(User, related_name='created_purchase', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='purchased_item', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    store = models.ForeignKey(Store, related_name='purchased_from_store', on_delete=models.CASCADE)
    date_of_purchase = models.DateTimeField(auto_now_add=True)
    entry_type = models.CharField(max_length=100)

    class Meta:
        db_table = 'purchases'

    def __str__(self):
        return f" user {self.user.username}: Item {self.item.name}. from store: {self.store.name}. Quantity {self.quantity}"


class PaymentOutstanding(models.Model):
    user = models.ForeignKey(User, related_name='created_payment', on_delete=models.CASCADE)
    store = models.ForeignKey(Store, related_name='created_store_payment', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = 'payment_outstanding'

    def __str__(self):
        return f" User {self.user.username}: {self.amount} from store {self.store.name}"