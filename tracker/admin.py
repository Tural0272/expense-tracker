from django.contrib import admin
from .models import Category, Transaction, Budget


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'user', 'created_at']
    list_filter = ['type', 'created_at']
    search_fields = ['name', 'user__username']
    ordering = ['user', 'type', 'name']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['date', 'category', 'amount', 'user', 'created_at']
    list_filter = ['date', 'category__type', 'created_at']
    search_fields = ['category__name', 'user__username', 'note']
    ordering = ['-date', '-created_at']
    date_hierarchy = 'date'


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['month', 'limit_amount', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'month']
    ordering = ['-month', 'user']
