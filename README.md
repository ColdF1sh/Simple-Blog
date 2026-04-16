# Simple Blog

A simple blog web application built with Django for a university lab assignment.  
Users can register, log in, reset their password, create blog posts, view all posts, comment on posts, and manage their profile.

## Features

- User registration
- Login and logout
- Password reset using Django built-in authentication views
- User profile with editable bio
- Create, update, and delete posts
- View all posts on the home page
- Add comments to posts
- Django admin panel
- Bootstrap 5 user interface

## Technologies Used

- Python 3
- Django 5
- SQLite
- Django Templates
- Bootstrap 5 CDN

## Project Structure

```text
blog/
├── accounts/
├── blog_project/
├── posts/
├── static/
├── templates/
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt
```

## How to Run

1. Create a virtual environment:
   ```powershell
   python -m venv .venv
   ```
2. Activate the virtual environment:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Create migrations:
   ```powershell
   python manage.py makemigrations
   ```
5. Apply migrations:
   ```powershell
   python manage.py migrate
   ```
6. Create an admin user:
   ```powershell
   python manage.py createsuperuser
   ```
7. Run the development server:
   ```powershell
   python manage.py runserver
   ```
8. Open the project in your browser:
   `http://127.0.0.1:8000/`

## Password Reset Notes

- The email backend is configured to `console`, so reset emails are printed in the terminal during development.
- Copy the reset link from the terminal and open it in the browser to set a new password.

## Git Instructions

Initialize a new repository and push it to GitHub:

```powershell
git init
git add .
git commit -m "Initial commit - Simple Blog Django project"
git branch -M main
git remote add origin https://github.com/ColdF1sh/Simple-Blog.git
git push -u origin main
```
