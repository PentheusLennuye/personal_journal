"""
Standard Django URLs

urls > views > forms > models
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index")
]
