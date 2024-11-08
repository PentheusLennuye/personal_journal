"""
Django views
"""

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Expense, ExpenseType, Vendor

# pylint: disable=E1101


class IndexView(generic.ListView):
    """Return a list of expenses in order of date."""

    template_name = "expenses/index.html"
    context_object_name = "expenses"  # Assign a template var to queryset.

    def get_queryset(self):
        """Return the expenses in reverse order of purchase date."""
        return Expense.objects.order_by("-date")


class DetailView(generic.DetailView):
    """Display the expense read-only form for an id."""

    model = Expense
    template_name = "expenses/expense.html"


class ExpenseEditView(generic.DetailView):
    """Display the expense write form for an id."""

    model = Expense
    template_name = "expenses/expense_form.html"

    def get_context_data(self, **kwargs):
        """Add context variables to the view."""
        context = super().get_context_data(**kwargs)
        context["vendors"] = Vendor.objects.all()
        context["expense_types"] = ExpenseType.objects.all()
        return context


def expense_save(request, expense_id):
    """Display the expense write form for an id."""
    e = get_object_or_404(Expense, pk=expense_id)
    v = Vendor.objects.all()  # pylint: disable=E1101
    t = ExpenseType.objects.all()  # pylint: disable=E1101
    vendor = Vendor.objects.get(pk=request.POST["vendor"])
    try:
        vendor = Vendor.objects.get(pk=request.POST["vendor"])
    except (KeyError, Vendor.DoesNotExist):
        return render(
            request,
            "expenses/expense_form.html",
            {
                "expense": e,
                "vendors": v,
                "expense_types": t,
                "error_message": "Invalid vendor",
            },
        )
    e.description = request.POST["description"]
    e.expense = request.POST["cost"]
    e.vendor = vendor
    e.save()
    return HttpResponseRedirect(reverse("expenses:expense", args=(e.id,)))
