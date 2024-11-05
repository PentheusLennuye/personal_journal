"""
Django views
"""

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Expense, ExpenseType, Vendor

# pylint: disable=E1101


def index(request):
    """Return a list of expenses in order of date."""
    expenses = Expense.objects.order_by("-date")  # pylint: disable=E1101
    return render(request, "cost_journal/index.html", {"expenses": expenses})


def expense(request, expense_id):
    """Display the expense read-only form for an id."""
    e = get_object_or_404(Expense, pk=expense_id)
    return render(request, "cost_journal/expense.html", {"expense": e})


def expense_edit(request, expense_id):
    """Display the expense write form for an id."""
    e = get_object_or_404(Expense, pk=expense_id)
    v = Vendor.objects.all()  # pylint: disable=E1101
    t = ExpenseType.objects.all()  # pylint: disable=E1101
    return render(request, "cost_journal/expense_form.html",
                  {"expense": e, "vendors": v, "expense_types": t})


def expense_save(request, expense_id):
    """Display the expense write form for an id."""
    e = get_object_or_404(Expense, pk=expense_id)
    v = Vendor.objects.all()  # pylint: disable=E1101
    t = ExpenseType.objects.all()  # pylint: disable=E1101
    vendor = Vendor.objects.get(pk=request.POST["vendor"])
    try:
        vendor = Vendor.objects.get(pk=request.POST["vendor"])
    except (KeyError, Vendor.DoesNotExist):
        return render(request, "cost_journal/expense_form.html",
                      {"expense": e, "vendors": v, "expense_types": t,
                       "error_message": "Invalid vendor"})
    e.description = request.POST["description"]
    e.expense = request.POST["cost"]
    e.vendor = vendor
    e.save()
    return HttpResponseRedirect(reverse("cost_journal:expense", args=(e.id,)))
