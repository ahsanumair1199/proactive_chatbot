from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin


class AccountAdmin(UserAdmin):
    list_display = ('id', 'uuid', 'email', 'name',
                    'last_login', 'date_joined')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    list_display_links = ('id', 'uuid', 'email', 'name')


admin.site.register(Account, AccountAdmin)
