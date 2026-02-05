from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),
    
    # Transactions
    path('transactions/', views.transaction_list, name='transaction-list'),
    path('transactions/add/', views.TransactionCreateView.as_view(), name='transaction-create'),
    path('transactions/<int:pk>/edit/', views.TransactionUpdateView.as_view(), name='transaction-update'),
    path('transactions/<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='transaction-delete'),
    
    # Budget
    path('budget/', views.budget_view, name='budget'),
    
    # Exports
    path('export/csv/', views.export_csv, name='export-csv'),
    path('export/pdf/', views.export_pdf, name='export-pdf'),
]
