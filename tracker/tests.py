from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from datetime import date
from .models import Category, Transaction, Budget


class CategoryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_category_creation(self):
        """Test creating a category with valid data."""
        category = Category.objects.create(
            user=self.user,
            name='Food',
            type=Category.TYPE_EXPENSE
        )
        self.assertEqual(category.name, 'Food')
        self.assertEqual(category.type, Category.TYPE_EXPENSE)
        self.assertEqual(category.user, self.user)
    
    def test_category_unique_constraint(self):
        """Test that category name+type+user combination is unique."""
        Category.objects.create(
            user=self.user,
            name='Food',
            type=Category.TYPE_EXPENSE
        )
        
        # Should raise error when creating duplicate
        with self.assertRaises(Exception):
            Category.objects.create(
                user=self.user,
                name='Food',
                type=Category.TYPE_EXPENSE
            )
    
    def test_category_str_representation(self):
        """Test string representation of Category."""
        category = Category.objects.create(
            user=self.user,
            name='Salary',
            type=Category.TYPE_INCOME
        )
        expected = "Salary (INCOME)"
        self.assertEqual(str(category), expected)


class TransactionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            user=self.user,
            name='Food',
            type=Category.TYPE_EXPENSE
        )
    
    def test_transaction_creation(self):
        """Test creating a transaction with valid data."""
        transaction = Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('50.00'),
            date=date.today(),
            note='Lunch'
        )
        self.assertEqual(transaction.amount, Decimal('50.00'))
        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.category, self.category)
        self.assertEqual(transaction.note, 'Lunch')


class DashboardViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
    
    def test_dashboard_view_requires_login(self):
        """Test that dashboard requires authentication."""
        self.client.logout()
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_dashboard_view_returns_200_when_logged_in(self):
        """Test that dashboard returns 200 when user is logged in."""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_dashboard_context_data(self):
        """Test that dashboard provides correct context data."""
        response = self.client.get(reverse('dashboard'))
        self.assertIn('summary', response.context)
        self.assertIn('category_breakdown', response.context)
        self.assertIn('chart_data_json', response.context)
