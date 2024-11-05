# Personal Journal

For those who do not enjoy writing things down on paper. Also: personal diet,
exercise and expense journal.

## Project Creation Steps

```sh
poetry new personal_journal
cd personal_journal
rm -rf personal_journal  # Django will recreate the directory
poetry add django==5.1
poetry shell
django-admin startproject personal_journal .
./manage.py migrate  # Migrate the initial INSTALLED_APPS
DJANGO_SUPERUSER_USERNAME=admin \
DJANGO_SUPERUSER_PASSWORD=admin \
 ./manage.py createsuperuser --email admin@admin.com --noinput
```

## Django Workflow

urls.py > views.py > forms.py > models.py

## First App Expenses

```sh
./manage.py startapp expenses
```

1. Create _tox.ini_ to ignore _settings.py_
1. Create .gitignore to ignore pyc, sqlite3, `__pycache__`, etc.
1. Edit _personal_journal/settings.py_ LANGUAGE_CODE, TIME_ZONE, INSTALLED_APPS
   < "expenses.apps.CostJournalConfig"
1. Edit _expenses/models.py_ to create its models
1. Edit _expenses/views.py_ to create an index
1. Create _expenses/urls.py_ to create url_patterns
1. Optionally, edit _expenses/admin.py_ to register the models to the admin
1. Edit _personal_journal/urls.py_ to point to _expenses/urls_.
1. Migrate the new models, part one: `./manage.py makemigrations expenses`
1. Migrate the new models, part two: `./manage.py migrate
1. Fire up the system: `./manage.py runserver`
1. Set the browser to <http://localhost:8000/admin>
