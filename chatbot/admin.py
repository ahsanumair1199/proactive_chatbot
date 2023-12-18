from django.contrib import admin
from .models import Conversation, GptResponse, AddMessage


class AddMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'message', 'is_sent', 'created_at')
    list_display_links = ('id', 'uuid', 'message')


class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'whatsapp_user', 'text', 'created_at')
    list_display_links = ('id', 'uuid', 'whatsapp_user', 'text')


class GptResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'whatsapp_user', 'text', 'created_at')
    list_display_links = ('id', 'uuid', 'whatsapp_user', 'text')


admin.site.register(Conversation, ConversationAdmin)
admin.site.register(GptResponse, GptResponseAdmin)
admin.site.register(AddMessage, AddMessageAdmin)
