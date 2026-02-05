# Expense Tracker

A personal finance management web application built with Django that helps users track their income, expenses, and budgets.

## Author

**Owner/Author:** Tural Alakbarov  
**Email:** tural0272@gmail.com  
**Student Index:** 39251

## Features (Implemented Now - Phase 1)

### Core Functionality
- **User Authentication**: Registration, login, logout with Django's built-in auth system
- **Category Management**: Create, edit, delete income and expense categories
- **Transaction Tracking**: Add, edit, delete transactions with filtering and pagination
- **Budget Management**: Set monthly budget limits and track spending against budget
- **Dashboard**: Visual overview with charts and financial summaries
- **Data Export**: CSV and PDF export functionality for reports

### Dashboard Features
- Monthly financial summary (income, expense, net)
- Budget vs actual spending comparison
- Daily expense trend charts using Chart.js
- Category-wise expense breakdown
- Interactive month/year selector

### Security & Data Isolation
- User-specific data isolation (users can only see their own data)
- CSRF protection enabled
- Authentication required for all app pages
- Protection against IDOR (Insecure Direct Object Reference) attacks

### User Interface
- Clean, responsive design using Bootstrap 5
- Server-rendered Django templates (no separate frontend framework)
- Consistent navigation and messaging system
- Mobile-friendly interface

## Planned Features (Phase 2)

### Advanced Analytics
- Recurring transactions setup
- Yearly and quarterly financial reports
- Advanced spending patterns analysis
- Financial goals and savings tracking

### Technical Improvements
- PostgreSQL database migration
- Docker containerization
- REST API development
- Enhanced roles and permissions system

### User Experience
- Data import functionality
- Advanced filtering and search
- Customizable dashboard widgets
- Email notifications and reports

### Deployment & Operations
- Production deployment configuration
- Automated backup system
- Performance optimization
- Monitoring and logging

## Tech Stack

- **Backend**: Django 5.1 (Python)
- **Database**: SQLite (development), PostgreSQL (planned for production)
- **Frontend**: Bootstrap 5, Chart.js, Django Templates
- **PDF Generation**: ReportLab
- **Testing**: Django Test Framework
- **Authentication**: Django built-in authentication

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd expense-tracker
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Unix/MacOS
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main application: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Running Tests

```bash
python manage.py test
```

## Project Structure

```
expense-tracker/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore file
├── README.md                    # This file
├── PROGRESS_REPORT.md           # Progress report
├── expense_tracker/             # Django project package
│   ├── __init__.py
│   ├── settings.py              # Django settings
│   ├── urls.py                  # Main URL configuration
│   ├── wsgi.py                  # WSGI configuration
│   └── asgi.py                  # ASGI configuration
└── tracker/                     # Main Django app
    ├── __init__.py
    ├── admin.py                 # Django admin configuration
    ├── apps.py                  # App configuration
    ├── models.py                # Data models
    ├── views.py                 # View logic
    ├── forms.py                 # Django forms
    ├── urls.py                  # App URL configuration
    ├── tests.py                 # Test cases
    ├── services/
    │   ├── __init__.py
    │   └── analytics.py         # Analytics service functions
    └── templates/
        └── tracker/
            ├── base.html         # Base template
            ├── dashboard.html    # Dashboard page
            ├── login.html        # Login page
            ├── register.html     # Registration page
            ├── category_*.html   # Category management pages
            ├── transaction_*.html # Transaction management pages
            └── budget.html       # Budget management page
```

## Screenshots

*Note: Screenshots will be added after deployment*

## Contributing

This is a student project for academic purposes. The codebase demonstrates Django web development skills and follows best practices for security and maintainability.

## License

This project is for educational purposes as part of academic coursework.

## Support

For questions or support, please contact:
- **Email**: tural0272@gmail.com
- **Student Index**: 39251
