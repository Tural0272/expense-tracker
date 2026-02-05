from datetime import datetime, date
from decimal import Decimal
from django.db.models import Sum, Q, Count
from ..models import Transaction, Category, Budget


def get_monthly_summary(user, year, month):
    """Get monthly financial summary for a user."""
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)
    
    transactions = Transaction.objects.filter(
        user=user,
        date__gte=start_date,
        date__lt=end_date
    )
    
    income = transactions.filter(
        category__type=Category.TYPE_INCOME
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    
    expense = transactions.filter(
        category__type=Category.TYPE_EXPENSE
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    
    net = income - expense
    
    # Get budget for the month
    month_str = f"{year:04d}-{month:02d}"
    budget = Budget.objects.filter(user=user, month=month_str).first()
    budget_limit = budget.limit_amount if budget else None
    budget_remaining = budget_limit - expense if budget_limit else None
    
    return {
        'income': income,
        'expense': expense,
        'net': net,
        'budget_limit': budget_limit,
        'budget_remaining': budget_remaining,
        'budget_used_percentage': (expense / budget_limit * 100) if budget_limit and budget_limit > 0 else None,
    }


def get_category_breakdown(user, year, month, limit=10):
    """Get expense breakdown by category for a month."""
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)
    
    categories = Category.objects.filter(
        user=user,
        type=Category.TYPE_EXPENSE
    ).annotate(
        total_spent=Sum(
            'transaction__amount',
            filter=Q(
                transaction__user=user,
                transaction__date__gte=start_date,
                transaction__date__lt=end_date
            )
        )
    ).filter(
        total_spent__isnull=False
    ).order_by('-total_spent')[:limit]
    
    return [
        {
            'name': cat.name,
            'amount': cat.total_spent or Decimal('0.00')
        }
        for cat in categories
    ]


def get_monthly_chart_data(user, year, month):
    """Get data for monthly charts."""
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)
    
    # Daily expense data
    daily_expenses = Transaction.objects.filter(
        user=user,
        category__type=Category.TYPE_EXPENSE,
        date__gte=start_date,
        date__lt=end_date
    ).values('date').annotate(
        total=Sum('amount')
    ).order_by('date')
    
    # Category breakdown for pie chart
    category_data = get_category_breakdown(user, year, month)
    
    return {
        'daily_expenses': [
            {
                'date': item['date'].strftime('%Y-%m-%d'),
                'amount': float(item['total'])
            }
            for item in daily_expenses
        ],
        'category_breakdown': [
            {
                'name': item['name'],
                'amount': float(item['amount'])
            }
            for item in category_data
        ]
    }
