from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'message', 'timestamp')
    list_filter = ('sender', 'receiver', 'timestamp')
    search_fields = ('message',)
