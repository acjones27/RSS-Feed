# 🔥 RSS Feed

[![Python 3.10.6](https://img.shields.io/badge/python-3.10.6-blue.svg)](https://www.python.org/downloads/release/python-3106/)


An RSS Feed built from scratch using Python and Django 

![Example Homepage](/screenshots/preview.png?raw=true "Example Homepage")


## 🔥 Functionality

Started with a lot of the template from this tutorial from [Real Python](https://realpython.com/build-a-content-aggregator-python/) 🎉

♻️ Changed the scope to be an RSS Feed for journals like Nature/Science

✨ Added functionality to filter by journal or keyword search in the Title/Description

🚧 Pending
- Add more tests
- Fix image parsing (really not working with Javascript and currently taking the first .png/.jpg which may not always be the main image for the article)
- Add more RSS feeds
- Host it somewhere e.g. PythonAnywhere

## 🔧 Setup

Tested with Python 3.10.6 with on a Mac M1 (Ventura 13.2.1)

```zsh
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 🧑‍💻 Running the app

- Generate a django secret key

```zsh
python manage.py shell
```

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Save the key to a file called .env at the root of the project

- Create an admin user so that you can manage your DB/jobs from /admin
```zsh
python manage.py createsuperuser
```

- Create migrations
```zsh
python manage.py makemigrations && python manage.py migrate
```

- Run the scheduler
```zsh
python manage.py startjobs
```

- Run the server
```zsh
python manage.py runserver
```

## 🔍️ Using the app

- `http://127.0.0.1:8000/` -> See the full feed
- `http://127.0.0.1:8000/<journal>` -> Filter journals (partial match) e.g. `/nature`
- `http://127.0.0.1:8000/search/<keyword>` -> Filter article title/description by keyword e.g. `/search/brain`

## 🐛 Known issues

- If you're on a Mac and get an error like "Error: pg_config executable not found.", you may need to run `brew install postgresql` and try reinstalling the requirements again
