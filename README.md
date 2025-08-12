# 📘 Product Requirements Document (PRD)
## Knowledge Management Web Application

---

### 🧾 Overview

This document defines the requirements for a **web application to manage knowledge about products**. The system will be developed at a **high level of professionalism**, comparable to enterprise-grade applications.

The entire application will be built using **Python Flask** for both backend and frontend logic, and will use **HTML, CSS, and Jinja2** for templating.  
⚠️ **No JavaScript** will be used.

---

### 🎯 Goals

- Centralized, structured knowledge base per product
- Admin-controlled user and content management
- Responsive and aesthetically pleasing interface
- No reliance on JavaScript; built purely with Python, HTML, CSS, and Jinja2

---

### 🏗️ Tech Stack

| Layer      | Technology        |
|------------|-------------------|
| Backend    | Python 3.x, Flask |
| Frontend   | HTML, CSS, Jinja2 |
| Database   | SQLite (or PostgreSQL optional) |
| Server     | Gunicorn / uWSGI + Nginx (for deployment) |

---

### 👤 User Roles

#### 🛠 Admin

- Only the **admin can create user accounts**
- **No self-registration page** needed
- Can **approve or reject tips/information** before publishing
- Must **rate each approved tip** (1 to 10 stars)
- Can **view reports** of stars earned by each user:
  - By month
  - By specific date range

#### 👤 Regular User

- Can log in using credentials created by the admin
- Can **submit product tips or information**
- Can **view how many tips have been approved**
- Can **see how many stars earned**
  - By month
  - By date range

---

### 📂 Features

- Upload **multiple attachments** per tip (no limit)
- Show **file name and extension** for each uploaded file
- **Responsive and user-friendly UI**
- **Simple and clean file structure**
- Pages built using **HTML + CSS + Jinja2**, with **no JavaScript**

---

### 📁 File Structure (Suggested)

/app
│
├── /static
│ ├── /css
│ └── /uploads
│
├── /templates
│ ├── base.html
│ ├── dashboard.html
│ ├── login.html
│ └── ...
│
├── init.py
├── routes.py
├── models.py
├── forms.py
└── utils.py

---

### 📌 Non-Functional Requirements

- **Security**: Admin-only access for critical features (user creation, approval, rating)
- **Accessibility**: Designed with readability and keyboard-only usability in mind
- **Performance**: Fast loading despite being JavaScript-free
- **Maintainability**: Simple code and file structure for easy updates and feature expansion

---

### ✅ Success Criteria

- Fully functional admin dashboard for user and tip management
- Users can submit, track, and review their tips and stars
- Fully responsive design with good UX
- No JavaScript used at any point
