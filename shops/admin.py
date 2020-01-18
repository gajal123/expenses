from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from shops.models import User, Store, Item, Purchase

# Register your models here.
admin.site.register(User, UserAdmin)


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    pass



@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    pass