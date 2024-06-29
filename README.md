# Simple Reddit

## Overview
Simple Reddit is a web application inspired by Reddit, built with Django. It allows users to create and join subreddits, post content, comment on posts, and upvote posts.

## Features
- User Registration and Authentication
- Subreddit Creation and Management
- Post Creation and Listing
- Commenting on Posts
- Upvoting Posts
- User Profile with Subscriptions and Upvotes

## Tech Stack
- Backend: Django, Django REST Framework
- Database: SQLite (default)
- Authentication: JWT

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/simple-reddit.git
    cd simple-reddit
    ```

2. Create a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Apply migrations:
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Create a superuser:
    ```sh
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```sh
    python manage.py runserver
    ```
