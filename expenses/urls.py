"""
Standard Django URLs

urls > views > forms > models
"""

from django.urls import path

from . import views

# pylint: disable=E1101

app_name = "expenses"  # pylint: disable=C0103
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="expense"),
    path(
        "<int:pk>/edit", views.ExpenseEditView.as_view(), name="edit_expense"
    ),
    path("<int:expense_id>/save", views.expense_save, name="save_expense"),
]
