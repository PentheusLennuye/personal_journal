"""
Standard Django URLs

urls > views > forms > models
"""

from django.urls import path

from . import views

app_name = "cost_journal"  # pylint: disable=C0103
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:expense_id>/", views.expense, name="expense"),
    path("<int:expense_id>/edit", views.expense_edit, name="edit_expense"),
    path("<int:expense_id>/save", views.expense_save, name="save_expense")
]
