"""
Django views
"""

from django.http import HttpResponse


def index(request):
    """Return a string at the home directory."""
    return HttpResponse("Hello, world!")
