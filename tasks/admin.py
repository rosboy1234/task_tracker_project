from django.contrib import admin
from .models import Task, Comment

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'priority', 'due_date', 'created_at')
    list_filter = ('status', 'priority', 'due_date', 'user')
    search_fields = ('title', 'description')
    list_editable = ('status', 'priority', 'due_date')
    date_hierarchy = 'created_at'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'author', 'created_at')
    search_fields = ('text',)
    list_filter = ('author', 'created_at')