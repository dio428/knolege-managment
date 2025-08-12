# Knowledge Management Web Application

This is a simple but powerful web application for managing product-related knowledge and tips. It is built entirely with Python and Flask, with no JavaScript. The application provides a clean interface for users to submit tips and for admins to manage users, products, and the tips themselves.

## Features

- **User Authentication**: Secure login and session management for users.
- **Role-Based Access Control**: Distinction between regular users and admins.
- **Admin Dashboard**: Admins can:
    - Create, view, and manage user accounts.
    - Create and manage products.
    - Review, approve, reject, and rate user-submitted tips.
    - View reports on user contributions, with date filtering.
- **User Dashboard**: Users can:
    - Submit tips for different products, including multiple file attachments.
    - View the status (approved/pending) and rating of their submitted tips.
    - Track their total number of approved tips and earned stars.
- **File Uploads**: Supports multiple file attachments per tip.
- **Responsive Design**: A clean and simple CSS-based design that works on all screen sizes.
- **No JavaScript**: The entire frontend is rendered server-side using Flask and Jinja2.

## Tech Stack

- **Backend**: Python 3, Flask
- **Frontend**: HTML, CSS, Jinja2
- **Database**: SQLite
- **Forms**: Flask-WTF
- **Authentication**: Flask-Login
- **Database ORM**: Flask-SQLAlchemy
- **Testing**: unittest

## Setup and Installation

To set up and run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize the database and create an admin user:**
    The application uses a Flask CLI command to create the first admin user.
    ```bash
    export FLASK_APP=run.py
    flask create-admin <username> <password>
    ```
    Replace `<username>` and `<password>` with your desired credentials.

5.  **Run the application:**
    ```bash
    flask run
    ```
    The application will be available at `http://127.0.0.1:5000`.

## Running Tests

To run the test suite, execute the following command in the root of the project directory:
```bash
python tests.py
```
