# Project and Task Management API

## Overview

This project provides a REST API for managing projects and tasks. It includes functionality for:
- Creating, updating, and deleting projects and tasks.
- Filtering tasks by status and priority.
- Generating reports for task statuses and overdue tasks.
- JWT-based authentication for secure access.
- Integration with Telegram for sending notifications about overdue tasks.

## Features

- **Project Management**: Create, update, delete, and list projects.
- **Task Management**: Create, update, delete, and list tasks within projects. Filter tasks by status and priority.
- **Reports**: Generate reports for task statuses and overdue tasks.
- **Notifications**: Send notifications about overdue tasks via Telegram.
- **Authentication**: Secure the API using JWT authentication.

## Requirements

- Python 3.10 or later
- Django 5.x
- Django REST Framework 3.x
- PostgreSQL
- Requests library (for sending notifications)
- `django-cors-headers` (if needed for CORS)

## Setup

### Clone the Repository

```bash
git clone https://github.com/kchaitanya954/project-manager.git
cd project-manager/project_manager
```

### Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate ` # On Windows use `venv\Scripts\activate`
```
### Install Dependencies
```bash
pip install -r requirements.txt
```

- Create a PostgreSQL database and user. Update the database settings in project_manager/settings.py with your database credentials.

### Migrate the Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### Run the Development Server
```bash
python manage.py runserver
```

### JWT Authentication
```bash
curl -X POST http://127.0.0.1:8000/api/token/ -H "Content-Type: application/json" -d '{"username": "yourusername", "password": "yourpassword"}'
```
- Include the JWT token in the Authorization header of your API requests:
```bash
-H "Authorization: Bearer <your_token>"
```
## Access the API
- API Documentation (Swagger): http://127.0.0.1:8000/swagger/
### API Endpoints:
- Projects: /projects/
- Tasks: /projects/{project_id}/tasks/
- Overdue Tasks Report: /reports/overdue_tasks/

### Testing
```bash
python manage.py test
```

### Notifications
- This project integrates with the Telegram API to send notifications about overdue tasks. Make sure to configure the Telegram bot token and the chat id in your environment variables or settings.

