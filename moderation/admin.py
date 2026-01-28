from django.contrib import admin
from .models import Message, ModerationResult, Report, ModerationAction

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'content', 'status', 'created_at']
    list_filter = ['status', 'created_at']

@admin.register(ModerationResult)
class ModerationResultAdmin(admin.ModelAdmin):
    list_display = ['message', 'category', 'toxicity', 'analyzed_at']
    list_filter = ['category']

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['message', 'reporter', 'reason', 'created_at']
    list_filter = ['reason']

@admin.register(ModerationAction)
class ModerationActionAdmin(admin.ModelAdmin):
    list_display = ['message', 'moderator', 'action', 'created_at']
    list_filter = ['action']
