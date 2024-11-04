# Self-Discipline

## Project Creation Steps

```sh
poetry new self_discipline
cd self_discipline
rm -rf self_discipline  # Django will recreate the directory
poetry add django==5.1
poetry shell
django-admin startproject self_discipline .
./manage.py migrate  # Migrate the initial INSTALLED_APPS
```

## Django Workflow

urls.py > views.py > forms.py > models.py

## First App Cost Journal

```sh
./manage.py startapp cost_journal
```

1. Create _tox.ini_ to ignore _settings.py_
1. Edit _self_discipline/settings.py_ LANGUAGE_CODE, TIME_ZONE, INSTALLED_APPS
   < "cost_journal.apps.CostJournalConfig"
1. Edit _cost_journal/models.py_ to create its models
1. Edit _cost_journal/views.py_ to create an index
1. Create _cost_journal/urls.py_ to create url_patterns
1. Edit _self_discipline/urls.py_ to point to _cost_journal/urls_.
1. Migrate the new models: `./manage.py makemigrations cost_journal`
1. Fire up the system: `./manage.py runserver`
