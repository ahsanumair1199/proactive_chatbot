from django.contrib import admin
from .models import Account, WhatsappUser
from django.contrib.auth.admin import UserAdmin


class AccountAdmin(UserAdmin):
    list_display = ('id', 'uuid', 'email', 'name',
                    'last_login', 'date_joined')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    list_display_links = ('id', 'uuid', 'email', 'name')


class WhatsappUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'name', 'phone_number', 'date_joined')
    list_display_links = ('id', 'uuid', 'name', 'phone_number')


admin.site.register(Account, AccountAdmin)
admin.site.register(WhatsappUser, WhatsappUserAdmin)
