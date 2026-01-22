
This version:

* Fixes repetition
* Adds **registration, roles, tests, use case diagram**
* Clarifies **SQLite vs MariaDB/MySQL**
* Adds **testing + planning sections**
* Is **submission-ready**

---

# 📰 Django News Application

> **SQLite is used for local development. The application is compatible with MariaDB/MySQL for production deployment.**

---

## 📌 Overview

This is a **Django-based News Application** that supports multiple user roles, article submission and approval workflows, email notifications, and API integration.
It is designed for learning full-stack development concepts such as **authentication, permissions, workflows, signals, and external API integration**.

---

## ✨ Key Features

* Multi-role users: **Reader, Journalist, Editor**
* **Frontend user registration**
* **Role selection during registration** (Reader / Journalist)
* **Journalist Dashboard**: Submit and manage own articles
* **Editor Dashboard**: Review, approve, reject articles
* **Reader Dashboard**: View approved articles
* **Approval workflow** with status tracking
* **Email notifications** when articles are approved
* **Social media posting** to X (Twitter) using official API credentials
* **REST API** endpoint: `/api/articles/`
* **Login / Logout** with role-based permissions
* **Bootstrap-based frontend templates**
* **Unit tests** for core workflows
* **Use case diagram** for planning and test mapping
* secure environment variable management

---

## 👥 User Roles & Permissions

| Role       | Capabilities                                        |
| ---------- | --------------------------------------------------- |
| Reader     | View approved articles, receive notifications       |
| Journalist | Register, submit articles, edit own articles        |
| Editor     | Approve/reject articles, edit or delete any article |

> 🔐 Editors cannot self-register and must be created by an administrator.

---

## Key Features

- Role-based authentication and dashboards
- Article approval workflow
- Email notifications when articles are approved
- Secure posting of article summaries to **X (Twitter)** using OAuth 1.0a
- REST API endpoint: `/api/articles/`
- Bootstrap-based frontend UI
- Unit tests for models, views, and workflows

---

## Technology Stack

- Python 3.13
- Django 5+
- SQLite (local development & testing)
- MySQL / MariaDB (production-ready)
- Bootstrap 5
- Tweepy (X API integration)
- python-dotenv

---

## Environment Variables (IMPORTANT)

Sensitive credentials are stored in a `.env` file **not committed to GitHub**.

### `.env` example (DO NOT COMMIT)

```env
X_API_KEY=your_api_key
X_API_SECRET=your_api_secret
X_ACCESS_TOKEN=your_access_token
X_ACCESS_TOKEN_SECRET=your_access_token_secret
X_BEARER_TOKEN=your_bearer_token

---

## 🧭 Use Case Diagram (Planning)

The use case diagram is stored in:

```
Planning/use_case_diagram.md
```

### Actors and Interactions

```
Reader ─────────────▶ View Approved Articles
Reader ─────────────▶ Read Full Article
Reader ─────────────▶ Receive Email Notifications

Journalist ─────────▶ Register
Journalist ─────────▶ Login
Journalist ─────────▶ Submit Article
Journalist ─────────▶ Edit Own Article
Journalist ─────────▶ View Article Status

Editor ─────────────▶ Login
Editor ─────────────▶ View Pending Articles
Editor ─────────────▶ Approve Article
Editor ─────────────▶ Reject Article
Editor ─────────────▶ Edit Any Article

Approve Article ────▶ Trigger Notifications
```

This diagram was used to **plan application logic and unit tests**.

---

You’re actually very close 👍
The error is **not in your tests** — it’s in your **database configuration for testing**.

Let’s break this down clearly and then fix it step by step.

---

## ✅ What the error is telling you (plain English)

### The key error

```text
django.db.utils.OperationalError: (2003, "Can't connect to MySQL server on '127.0.0.1:3306' (61)")
```

### Meaning

Django is trying to:

* Use **MySQL**
* Connect to **127.0.0.1:3306**
* While running `python manage.py test`

But:

* **MySQL is not running**, OR
* **MySQL is not installed**, OR
* **You intended to use SQLite for local/testing**, but Django is still configured for MySQL

👉 This is **expected** given what you wrote in your README:

> “SQLite is used for local development. The application is compatible with MariaDB for production deployment.”

Right now, your **settings.py does not reflect that separation**.

---

## 🔍 Why this happens specifically during `manage.py test`

When Django runs tests, it:

1. Reads `DATABASES` from `settings.py`
2. Tries to **create a test database**
3. Uses the **same database engine** unless told otherwise

Your settings are currently something like:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'news_db',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

So Django says:

> “Cool, I’ll create a MySQL test database.”

But MySQL isn’t available → 💥 crash.

---

## ✅ The CORRECT fix (best practice)

### Use:

* **SQLite for local dev + tests**
* **MySQL/MariaDB only in production**

### Option 1 (RECOMMENDED): Environment-based settings

#### 1️⃣ Update `settings.py`

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

ENVIRONMENT = os.getenv("DJANGO_ENV", "development")

if ENVIRONMENT == "production":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "HOST": os.getenv("DB_HOST", "127.0.0.1"),
            "PORT": os.getenv("DB_PORT", "3306"),
        }
    }
else:
    # Development & Testing
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
```

---

#### 2️⃣ Run tests (no MySQL needed)

```bash
python manage.py test
```

✅ Django will now:

* Use SQLite
* Auto-create a test DB
* Run tests successfully

---

### Option 2 (Quick fix): Force SQLite for tests only

If you want the **fastest fix**, add this to `settings.py`:

```python
if "test" in sys.argv:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    }
```

This uses an **in-memory database** for tests 🚀

---

## 🧪 Why your earlier error changed

You previously saw:

```text
AttributeError: 'PosixPath' object has no attribute 'startswith'
```

That happens when:

* MySQL backend expects a **string DB name**
* But receives a `Path` object

That’s another sign that **MySQL + SQLite settings were mixed incorrectly**.

Fixing the database separation resolves **both errors**.

---

## ✅ What to verify after fixing

Run these commands:

```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py test
```

Expected result:

```text
Found 4 test(s).
Creating test database for alias 'default'...
....
----------------------------------------------------------------------
Ran 4 tests in X.XXXs

OK
```

---

## 🧠 What to update in your README (important)

Add this section:

````md

## Testing

This project uses **SQLite for development and testing**.

To run tests locally:
```bash
python manage.py test
````

For production, configure **MariaDB/MySQL** using environment variables:

* `DB_NAME`
* `DB_USER`
* `DB_PASSWORD`
* `DB_HOST`
* `DB_PORT`
* `DJANGO_ENV=production`

```

### Test Location

```
news_app/tests.py
```

### Covered Test Cases

* Frontend user registration
* Automatic role & group assignment
* Article submission by journalists
* Article approval workflow by editors

### Running Tests

```bash
python manage.py test
```

---

## 🗂️ Project Structure

```
news_application/
├── news_project
│   ├── manage.py
│   ├── news_app
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-313.pyc
│   │   │   ├── admin.cpython-313.pyc
│   │   │   ├── apps.cpython-313.pyc
│   │   │   ├── models.cpython-313.pyc
│   │   │   ├── signals.cpython-313.pyc
│   │   │   ├── tests.cpython-313.pyc
│   │   │   ├── urls.cpython-313.pyc
│   │   │   └── views.cpython-313.pyc
│   │   ├── admin.py
│   │   ├── api
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   │   ├── __init__.cpython-313.pyc
│   │   │   │   ├── serializers.cpython-313.pyc
│   │   │   │   ├── urls.cpython-313.pyc
│   │   │   │   └── views.cpython-313.pyc
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   └── views.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── migrations
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   │   ├── __init__.cpython-313.pyc
│   │   │   │   ├── 0001_initial.cpython-313.pyc
│   │   │   │   └── 0002_article_notified.cpython-313.pyc
│   │   │   ├── 0001_initial.py
│   │   │   └── 0002_article_notified.py
│   │   ├── models.py
│   │   ├── signals.py
│   │   ├── static
│   │   │   └── news_app
│   │   │       └── static
│   │   ├── templates
│   │   │   └── news_app
│   │   │       ├── article_detail.html
│   │   │       ├── article_list.html
│   │   │       ├── base.html
│   │   │       ├── journalist_dashboard.html
│   │   │       ├── login.html
│   │   │       ├── pending_articles.html
│   │   │       ├── register.html
│   │   │       └── submit_article.html
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── news_application Capstone project.txt
│   ├── news_project
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-313.pyc
│   │   │   ├── settings.cpython-313.pyc
│   │   │   └── urls.cpython-313.pyc
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── Planning
│   │   └── use_case_diagram.md
│   └── README.md
├── requirements.txt
└── venv
    ├── bin
    │   ├── activate
    │   ├── activate.csh
    │   ├── activate.fish
    │   ├── Activate.ps1
    │   ├── django-admin
    │   ├── dotenv
    │   ├── normalizer
    │   ├── pip
    │   ├── pip3
    │   ├── pip3.13
    │   ├── pipreqs
    │   ├── python -> python3.13
    │   ├── python3 -> python3.13
    │   ├── python3.13 -> /opt/homebrew/opt/python@3.13/bin/python3.13
    │   └── sqlformat
    ├── include
    │   └── python3.13
    ├── lib
    │   └── python3.13
    │       └── site-packages
    │           ├── __pycache__
    │           ├── asgiref
    │           ├── asgiref-3.11.0.dist-info
    │           ├── certifi
    │           ├── certifi-2025.11.12.dist-info
    │           ├── charset_normalizer
    │           ├── charset_normalizer-3.4.4.dist-info
    │           ├── django
    │           ├── django-6.0.dist-info
    │           ├── djangorestframework-3.16.1.dist-info
    │           ├── docopt-0.6.2.dist-info
    │           ├── docopt.py
    │           ├── dotenv
    │           ├── idna
    │           ├── idna-3.11.dist-info
    │           ├── mariadb
    │           ├── mariadb-1.1.14.dist-info
    │           ├── mysqlclient-2.2.7.dist-info
    │           ├── MySQLdb
    │           ├── packaging
    │           ├── packaging-25.0.dist-info
    │           ├── pip
    │           ├── pip-25.3.dist-info
    │           ├── pipreqs
    │           ├── pipreqs-0.4.13.dist-info
    │           ├── python_dotenv-1.2.1.dist-info
    │           ├── requests
    │           ├── requests-2.32.5.dist-info
    │           ├── rest_framework
    │           ├── sqlparse
    │           ├── sqlparse-0.5.5.dist-info
    │           ├── urllib3
    │           ├── urllib3-2.6.2.dist-info
    │           ├── yarg
    │           └── yarg-0.1.10.dist-info
    └── pyvenv.cfg
```

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/username/news_application.git
cd news_application/news_project
```

---

### 2️⃣ Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Database Setup

#### Local Development (SQLite)

No configuration required.

#### Production (MariaDB / MySQL)

1. Create database and user
2. Update `settings.py`
3. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🔔 Email Notifications

* Implemented using **Django signals**
* Console email backend used for development
* Notifications are sent **once per approved article**

---

## 🐦 X (Twitter) API Integration

Posting to X requires **five credentials** generated via the X Developer Platform:

1. API Key
2. API Secret
3. Access Token
4. Access Token Secret
5. Bearer Token

Errors from external APIs are **logged to the console** to ensure visibility and debugging.

---

## 🚀 REST API

* Endpoint: `/api/articles/`
* Returns approved articles
* Read-only access for public consumption

---

## ✅ Completed Features

* Role-based authentication & permissions
* Frontend registration and login
* Article approval workflow
* Email notifications
* X API integration
* Unit testing
* Use case planning documentation
* Bootstrap UI
* GitHub-ready repository

---

## 🔮 Future Improvements

* Pagination and search
* Rich text editor for articles
* Deployment to production server
* API authentication
* Image uploads for articles

---

## 👨‍🏫 Mentor Notes

This project demonstrates:

* Secure authentication and authorization
* Proper separation of user roles
* Signal-driven automation
* Test-driven validation
* Planning documentation alignment

---

## ✅ What to Add or Correct Next

**Must Do**

* Finish MariaDB/MySQL authentication setup
* Run migrations on production database
* Add screenshots for submission

**Recommended**

* Permission-based view tests
* `.env.example` file
* Deployment notes

**Optional**

* Diagram image (draw.io)
* Pagination & search
* Docker setup

---

If you want, I can next:

* ✅ Align this README exactly to your **bootcamp rubric**
* 📸 Provide a **submission screenshot checklist**
* 🧪 Add **advanced permission tests**
* 🚀 Prepare a **deployment guide**

Just say the word — you’re very close to final submission 👌
