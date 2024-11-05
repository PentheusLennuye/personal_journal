"""
Cost Journal Models
"""

from django.db import models


class CostCategory(models.Model):
    """The Kakeibo Category System."""
    # General (Essentials: food, utilities, healthcare, rent, transport)
    # Wants (Travel, Clothing, Dining Out, Unessential transport)
    # Culture (Museums, Tickets, Books, Zoos)
    # Unexpected Extras (Birthdays, Cars, medical bills)
    category = models.CharField(max_length=20)

    def __str__(self):
        return str(self.category)

    class Meta:
        """CostCategory Overrides."""
        verbose_name_plural = "cost categories"


class ExpenseType(models.Model):
    """Travel, Public Transport, Snacks, Postage"""
    expense_type = models.CharField(max_length=50)
    category = models.ForeignKey(CostCategory, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.expense_type)


class Vendor(models.Model):
    """The Supplier of the expense."""
    vendor = models.CharField(max_length=128)

    def __str__(self):
        return str(self.vendor)


class Expense(models.Model):
    """The ledger entry."""
    date = models.DateTimeField("receipt time")
    expense_type = models.ForeignKey(ExpenseType, on_delete=models.PROTECT)
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT)
    description = models.CharField(max_length=256)
    expense = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return str(self.description)
