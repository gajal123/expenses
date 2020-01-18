from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from shops.models import User, Store

# Register your models here.
admin.site.register(User, UserAdmin)


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    pass
