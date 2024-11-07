#!/usr/bin/env python3

import os
import sys

from django.contrib.auth import get_user_model


sys.path.append("/app")

username = os.environ["DJANGO_SUPERUSER_USERNAME"]
password = os.environ["DJANGO_SUPERUSER_PASSWORD"]
email = os.environ["DJANGO_SUPERUSER_EMAIL"]

User = get_user_model()
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
else:
    print(f"superuser {username} already exists, skipping creation.")

