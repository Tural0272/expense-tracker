import csv
from datetime import datetime, date
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.db.models import Sum, Q
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import io
import json

from .models import Category, Transaction, Budget
from .forms import CustomUserCreationForm, CategoryForm, TransactionForm, BudgetForm
from .services.analytics import get_monthly_summary, get_category_breakdown, get_monthly_chart_data


class CustomLoginView(LoginView):
    template_name = 'tracker/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    http_method_names = ['get', 'post']
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'tracker/register.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully! Please log in.')
        return response


@login_required
def dashboard(request):
    # Handle empty or invalid month/year parameters
    year_param = request.GET.get('year', '').strip()
    month_param = request.GET.get('month', '').strip()
    
    try:
        year = int(year_param) if year_param else datetime.now().year
    except (ValueError, TypeError):
        year = datetime.now().year
    
    try:
        month = int(month_param) if month_param else datetime.now().month
    except (ValueError, TypeError):
        month = datetime.now().month
    
    # Ensure month is valid (1-12)
    if month < 1 or month > 12:
        month = datetime.now().month
    
    summary = get_monthly_summary(request.user, year, month)
    category_breakdown = get_category_breakdown(request.user, year, month)
    chart_data = get_monthly_chart_data(request.user, year, month)
    
    context = {
        'summary': summary,
        'category_breakdown': category_breakdown,
        'chart_data_json': json.dumps(chart_data),
        'selected_year': year,
        'selected_month': month,
        'months': [
            {'value': 1, 'label': 'January'},
            {'value': 2, 'label': 'February'},
            {'value': 3, 'label': 'March'},
            {'value': 4, 'label': 'April'},
            {'value': 5, 'label': 'May'},
            {'value': 6, 'label': 'June'},
            {'value': 7, 'label': 'July'},
            {'value': 8, 'label': 'August'},
            {'value': 9, 'label': 'September'},
            {'value': 10, 'label': 'October'},
            {'value': 11, 'label': 'November'},
            {'value': 12, 'label': 'December'},
        ],
        'years': list(range(2020, datetime.now().year + 2)),
    }
    return render(request, 'tracker/dashboard.html', context)


@method_decorator(login_required, name='dispatch')
class CategoryListView(ListView):
    model = Category
    template_name = 'tracker/category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user).order_by('type', 'name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = context['categories']
        context['income_categories'] = categories.filter(type=Category.TYPE_INCOME)
        context['expense_categories'] = categories.filter(type=Category.TYPE_EXPENSE)
        return context


@method_decorator(login_required, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'tracker/category_form.html'
    success_url = reverse_lazy('category-list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'tracker/category_form.html'
    success_url = reverse_lazy('category-list')
    
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


@method_decorator(login_required, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'tracker/category_confirm_delete.html'
    success_url = reverse_lazy('category-list')
    
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


@login_required
def transaction_list(request):
    queryset = Transaction.objects.filter(user=request.user).select_related('category')
    
    # Filters
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    category_id = request.GET.get('category')
    transaction_type = request.GET.get('type')
    
    if date_from:
        queryset = queryset.filter(date__gte=date_from)
    if date_to:
        queryset = queryset.filter(date__lte=date_to)
    if category_id:
        queryset = queryset.filter(category_id=category_id)
    if transaction_type:
        queryset = queryset.filter(category__type=transaction_type)
    
    queryset = queryset.order_by('-date', '-created_at')
    
    # Pagination
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories for filter
    categories = Category.objects.filter(user=request.user).order_by('name')
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'filters': {
            'date_from': date_from,
            'date_to': date_to,
            'category': category_id,
            'type': transaction_type,
        }
    }
    return render(request, 'tracker/transaction_list.html', context)


@method_decorator(login_required, name='dispatch')
class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'tracker/transaction_form.html'
    success_url = reverse_lazy('transaction-list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class TransactionUpdateView(UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'tracker/transaction_form.html'
    success_url = reverse_lazy('transaction-list')
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


@method_decorator(login_required, name='dispatch')
class TransactionDeleteView(DeleteView):
    model = Transaction
    template_name = 'tracker/transaction_confirm_delete.html'
    success_url = reverse_lazy('transaction-list')
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


@login_required
def budget_view(request):
    budget = Budget.objects.filter(user=request.user).first()
    
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget_obj = form.save(commit=False)
            budget_obj.user = request.user
            
            # Delete existing budget for the month if any
            Budget.objects.filter(user=request.user, month=budget_obj.month).delete()
            
            budget_obj.save()
            messages.success(request, 'Budget updated successfully!')
            return redirect('budget')
    else:
        form = BudgetForm(instance=budget)
    
    context = {
        'form': form,
        'budget': budget,
    }
    return render(request, 'tracker/budget.html', context)


@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Date', 'Category', 'Type', 'Amount', 'Note'])
    
    queryset = Transaction.objects.filter(user=request.user).select_related('category')
    
    # Apply same filters as transaction list
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    category_id = request.GET.get('category')
    transaction_type = request.GET.get('type')
    
    if date_from:
        queryset = queryset.filter(date__gte=date_from)
    if date_to:
        queryset = queryset.filter(date__lte=date_to)
    if category_id:
        queryset = queryset.filter(category_id=category_id)
    if transaction_type:
        queryset = queryset.filter(category__type=transaction_type)
    
    queryset = queryset.order_by('-date', '-created_at')
    
    for transaction in queryset:
        writer.writerow([
            transaction.date,
            transaction.category.name,
            transaction.category.type,
            transaction.amount,
            transaction.note or '',
        ])
    
    return response


@login_required
def export_pdf(request):
    year = int(request.GET.get('year', datetime.now().year))
    month = int(request.GET.get('month', datetime.now().month))
    
    # Create PDF
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, f"Monthly Report - {year:04d}-{month:02d}")
    
    # Get data
    summary = get_monthly_summary(request.user, year, month)
    category_breakdown = get_category_breakdown(request.user, year, month)
    
    # Summary section
    y_position = height - 100
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y_position, "Summary:")
    y_position -= 20
    
    p.setFont("Helvetica", 10)
    p.drawString(50, y_position, f"Total Income: ${summary['income']}")
    y_position -= 15
    p.drawString(50, y_position, f"Total Expense: ${summary['expense']}")
    y_position -= 15
    p.drawString(50, y_position, f"Net: ${summary['net']}")
    y_position -= 15
    
    if summary['budget_limit']:
        p.drawString(50, y_position, f"Budget: ${summary['budget_limit']}")
        y_position -= 15
        p.drawString(50, y_position, f"Budget Remaining: ${summary['budget_remaining']}")
        y_position -= 15
        if summary['budget_used_percentage']:
            p.drawString(50, y_position, f"Budget Used: {summary['budget_used_percentage']:.1f}%")
            y_position -= 15
    
    # Category breakdown
    y_position -= 20
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y_position, "Expense Breakdown by Category:")
    y_position -= 20
    
    p.setFont("Helvetica", 10)
    for category in category_breakdown:
        p.drawString(50, y_position, f"{category['name']}: ${category['amount']}")
        y_position -= 15
        if y_position < 50:
            p.showPage()
            y_position = height - 50
    
    p.save()
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="monthly_report_{year:04d}_{month:02d}.pdf"'
    return response
