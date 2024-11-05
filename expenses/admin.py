"""Pre-generated Django admin registration page."""

from django.contrib import admin

from .models import CostCategory, ExpenseType, Vendor, Expense

for model_class in [CostCategory, ExpenseType, Vendor, Expense]:
    admin.site.register(model_class)
