# SaasCom

A modern platform for developers, companies, and engineering students to discover apps, jobs, articles, communities,  and learning resources in one place.

---

## 🚀 Overview

SaaCom is a full-featured community-driven platform built with Django. The platform combines:

* SaaS/App showcase
* Job board system
* Engineering / Development related article publishing
* User interaction system
* Company and developer profiles

The goal of this project is to create a centralized ecosystem where developers, companies, and students can connect, learn, share, and grow together.

---

## ✨ Features

### 👤 Authentication & User System

* Custom User Model
* Developer & Company user types
* User registration and login
* Role-based permissions
* Profile management
* Authentication & authorization system

### 💼 Job Board

* Post jobs
* Apply for jobs
* Job filtering
* Company job management
* Application tracking
* Responsive job feed UI

### 🧑‍💻 App Showcase

* Publish SaaS applications
* Multiple image upload support (Maximum 5)
* App detail pages
* Founder information
* App management system
* App reporting system
* App upvote and downvote system 

### 📝 Article & Community System

* Engineering articles
* Rich text editor support
* User engagement system
* Community-driven content
* Comments & interactions

### 🎧 Audio Streaming / Podcast (Planned)

* Audio upload
* Podcast episodes
* Streaming support
* Tech podcast system

###  Dashboard

* Apps Dashboard
* Jobs Dashboard
* Discussion Dashboard
* Application Dashboard

### ❤️ Interactive Features

* Like system
* Comment system
* AJAX interactions (Not now , in future)

### 🔒 Security

* CSRF protection
* Permission checks
* Secure authentication
* Custom validation
* Protected delete operations

---

## 🛠️ Tech Stack

### Backend

* Python
* Django
* Django REST Framework (For API)
* Django Channels (planned)

### Frontend

* HTML5
* CSS3
* Bootstrap
* JavaScript

### Database

* MySQL (SQlite in development)

### Tools & Services

* Summernote
* Git & GitHub
* Cloudinary

---

## 📂 Project Structure

```bash
SaasCom/
│
├── apps/
├── community/
├── jobs/
├── saas_com/
├── session/
├── static/
├── .gitignore/
├── requirements.txt
├── manage.py
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/nishan756/SaasCom.git
cd your-repository
```

### 2. Create Virtual Environment

```bash
python -m venv env
```

### 3. Activate Virtual Environment

#### Windows

```bash
env\Scripts\activate
```

#### Linux / Mac

```bash
source env_name/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Database

Update your database configuration inside:

```python
settings.py
```

Example:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'database_name',
        'USER': 'database_user',
        'PASSWORD': 'database_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

### 8. Run Development Server

```bash
python manage.py runserver
```

---
