from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Category, Transaction, Budget


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type']
        widgets = {
            'type': forms.Select(choices=Category.TYPE_CHOICES)
        }


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'amount', 'date', 'note']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'note': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['month', 'limit_amount']
        widgets = {
            'month': forms.DateInput(attrs={'type': 'month'}),
        }
