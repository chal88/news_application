# Django News Application

## Overview
This is a **Django-based News Application** that supports multiple user roles, article submission and approval workflows, email notifications, and a REST API. It is designed for learning full-stack development concepts such as authentication, permissions, and API integration.

**Key Features:**
- Multi-role users: **Reader, Journalist, Editor**
- **Journalist Dashboard**: Submit articles
- **Editor Dashboard**: Approve or reject articles
- **Reader Dashboard**: View approved articles
- **Email notifications**: Sent to readers when new articles are approved
- **Social media posting**: Posts article summaries to X (Twitter)
- **REST API**: Access articles via `/api/articles/` endpoint
- **Login/Logout**: Role-based login with proper permissions
- **Frontend templates**: Fully functional HTML templates for dashboards and articles

---

## Project Structure

# Django News Application

## Overview
This is a **Django-based News Application** that supports multiple user roles, article submission and approval workflows, email notifications, and a REST API. It is designed for learning full-stack development concepts such as authentication, permissions, and API integration.

**Key Features:**
- Multi-role users: **Reader, Journalist, Editor**
- **Journalist Dashboard**: Submit articles
- **Editor Dashboard**: Approve or reject articles
- **Reader Dashboard**: View approved articles
- **Email notifications**: Sent to readers when new articles are approved
- **Social media posting**: Posts article summaries to X (Twitter)
- **REST API**: Access articles via `/api/articles/` endpoint
- **Login/Logout**: Role-based login with proper permissions
- **Frontend templates**: Fully functional HTML templates for dashboards and articles


---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/username/news_application.git
cd news_application/news_project

python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

python manage.py runserver

python manage.py runserver
