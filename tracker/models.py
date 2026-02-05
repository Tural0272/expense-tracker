from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class Category(models.Model):
    TYPE_INCOME = 'INCOME'
    TYPE_EXPENSE = 'EXPENSE'
    TYPE_CHOICES = [
        (TYPE_INCOME, 'Income'),
        (TYPE_EXPENSE, 'Expense'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'name', 'type']
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.type})"


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    date = models.DateField()
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['user', 'category']),
        ]
    
    def __str__(self):
        return f"{self.category.name}: {self.amount} on {self.date}"


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.CharField(max_length=7)  # Format: YYYY-MM
    limit_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'month']
        ordering = ['-month']
    
    def __str__(self):
        return f"Budget for {self.month}: {self.limit_amount}"
