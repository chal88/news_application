Project News Application 

Django News Application — role-based article workflow

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
The manage.py file is located in the project root at
news_project/news_application/manage.py.
It serves as the main command-line utility for managing the Django project, including running the development server, applying database migrations, creating superusers, and executing administrative tasks.

---
## Database Configuration (MariaDB Requirement)

This application uses MariaDB when running in production mode.

By default, the project runs in development mode using SQLite.
To enable MariaDB, you MUST set the environment variable below:

```bash
export DJANGO_ENV=production

1. Install MariaDB
sudo apt update
sudo apt install mariadb-server mariadb-client

2. Login
sudo mariadb

3. Create database
CREATE DATABASE news_db;

4. Create database user
CREATE USER 'news_user'@'localhost' IDENTIFIED BY 'strongpassword';

5. Grant database permissions
GRANT ALL PRIVILEGES ON news_db.* TO 'news_user'@'localhost';
FLUSH PRIVILEGES;

6. Set required Environmental variables
export DJANGO_ENV=production
export DB_NAME=news_db
export DB_USER=news_user
export DB_PASSWORD=strongpassword
export DB_HOST=127.0.0.1
export DB_PORT=3306

7. Apply Database migrations 
python manage.py migrate

## User Registration & Login

Users can register themselves as **Reader** or **Journalist**. Editors not created through public registration page. 
After registering, users can log in using their credentials.

During registration:
Journalists  must select an existing Publishing House or create a new one.
Readers do not select a Publishing House.

👥 User Roles & Permissions
Reader:
   Can view approved articles and newsletters only.
   Cannot create or manage content.

Journalists:
Newsletter and Article Management

The application includes a Newsletter and article feature that allows journalists to communicate updates and announcements to readers within their publishing house.

Journalist Capabilities:
*Journalists can create newsletters and articles from their dashboard.
*Each newsletter and article is automatically linked to:
   *the logged-in journalist
   *the journalist’s publishing house
*Only authenticated users with the Journalist role can create articles or newsletters.
 How to Create a Newsletter:
   1. Log in as a Journalist
   2. Navigate to the Journalist Dashboard
   3. Click “Create Newsletter” or "Create article"
   4. Complete the newsletter or article form and submit

   Journalist Permissions:
   Journalists have full CRUD (Create, Read, Update, Delete) access to:
      * Articles
      * Newsletters
      * edit or delete option 
      * Editing an approved article or newsletter automatically resets its approval status and requires re-approval by an editor  via the Django Admin

This functionality ensures the application reflects real-world newsroom workflows and fulfills the journalist responsibility requirements of the task.

Creating Editors :

Steps to create an Editor:
Editors do not self-register.

Creating an Editor Account by:
Logging in to the Django Admin panel (/admin) as a superuser.
Navigate to: Users → Add User.
Fill in:
Username
Email
Password
Set the following fields:
Role: editor
is_staff: True (required to access the admin panel)
(Optional) Assign a Publishing House
Save the user.
✅ The editor can now log in with these credentials.

Only users created using this process will have Editor permissions.

2️⃣ Accessing the Application
Log in using the standard login page on the frontend.
After login, the editor is redirected to the Editor Dashboard.
The Editor Dashboard is informational only: it shows pending articles and newsletters but does not allow approval from the frontend.

3️⃣ Approving Articles & Newsletters
All content approval happens in the Django Admin panel (/admin).
Editors use the same username and password to log in to the admin site.
They can then:
Review pending articles
Approve or reject articles
Review and approve newsletters
Only users with is_staff = True can access this panel.

4️⃣ Security & Best Practices
Editors cannot grant themselves admin access.
Superusers control who can become an editor.
Editors do not have superuser privileges—they can only manage content according to their role.

🔐 Why Django Admin Is Used for Approval
Ensures secure and controlled access
Prevents self-approval of content
Clearly separates content creation and moderation
Aligns with real-world publishing workflows


### Models

- **CustomUser**: Extended user model with roles (`reader`, `journalist`, `editor`) and optional association to a `PublishingHouse`.
- **PublishingHouse**: Represents a publishing house managed by an editor. Editors are linked one-to-one to a PublishingHouse.
- **Article**: News articles submitted by journalists, optionally linked to a PublishingHouse, with an approval status.


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
news_project/Use Case Diagram News App.jpg

This diagram was used to **plan application logic and unit tests**.

---

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
### Testing

1. **Reader Registration**: Use the register page, select Reader, and verify you can login and see articles.  
2. **Journalist Registration**: Use the register page, select Journalist, submit an article, and confirm it appears as pending.  
3. **Editor Registration**: Must be done by superuser via Django Admin:
   - Go to Admin → Users → Add Editor.
   - Set role = Editor.
   - Set password using **"Set Password"**, not the raw password field.
   - Login with editor credentials and confirm dashboard shows pending articles.
4. **Role-Based Redirects**: Login with each role to confirm you are redirected automatically to the correct dashboard.
5. **Publishing House Filtering**:
   - Journalist assigns article to a Publishing House.
   - Editor linked to that Publishing House should see the article in their dashboard.


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

Before running the project, install the required Python packages.

From the **news_application/news_project/** folder (where `manage.py` is located), run:

```bash
pip install -r requirements.txt


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

## Architecture & Role Relationships

This application models real-world publishing workflows using relational data.

### User Roles

- **Reader**: Can register normally. Views approved articles.  
- **Journalist**: Can submit articles independently or under a Publishing House.  
- **Editor**: Must be created by the superuser. Can view and approve pending articles submitted to their Publishing House.  

**Login Behavior**:
- After login, the user is redirected automatically to the appropriate dashboard:
  - Journalists → Journalist Dashboard
  - Editors → Editor Dashboard
  - Readers → Article List

### Publishing Houses
- Each **Publishing House** is managed by exactly one Editor
- Journalists may submit articles:
  - Independently
  - OR under a specific Publishing House

### Article Workflow
1. Journalist submits article (selects publishing option)
2. Article is marked as *pending approval*
3. Editor sees only articles belonging to their publishing house
4. Editor approves or rejects the article
5. Approved articles become visible to readers



