# 📚 Green Hill Library

A modern Library Management System developed with **Flask**, **SQLAlchemy** and **MySQL**.

The application provides a complete environment for managing books, members, borrowings and returns, while also integrating with the **Open Library API** for automatic book information retrieval through ISBN.

🌐 **Live Demo**

https://konnachrys.pythonanywhere.com

---

# 📖 Table of Contents

* Features
* Technologies
* API Integration
* Screenshots
* Installation
* Future Improvements
* Author

---

# ✨ Features

## 📚 Book Management

* Add new books
* Edit existing books
* Delete books
* Upload custom book covers
* Automatic ISBN lookup
* Automatic book information retrieval
* Search books by title or author
* Filter by category, language, publication year and availability

## 👥 Member Management

* Add members
* Edit member information
* Delete members
* Automatic library card number generation
* Library card barcode support
* Loan history
* Outstanding balance tracking
* Search by card number
* Search by first and last name

## 📷 Barcode Support

- ISBN barcode scanning
- Library card barcode scanning
- Automatic form completion
- Fast borrowing workflow

## 🔄 Borrowing System

* Create new borrowings
* Borrow multiple books at once
* Automatic due date calculation
* Automatic availability update
* Automatic member balance update

## 📥 Return System

* Return borrowed books
* Automatic overdue detection
* Automatic fine calculation
* Fine payment tracking

## 🔍 Smart Search

Depending on the current page:

* Book search
* Member search
* Borrowing search
* Return search

## 🎨 User Interface

* Custom designed home page
* Custom library card layout
* Responsive Bootstrap components
* Custom CSS styling

  
---

# 🛠 Technologies

## Backend

* Python
* Flask
* SQLAlchemy
* MySQL

## Frontend

* HTML
* CSS
* JavaScript
* Bootstrap
* Tom Select

## External Services

* Open Library API

## Development Tools

* Visual Studio Code
* Git
* GitHub

## Deployment

* PythonAnywhere

---

# 🌐 API Integration

The application uses the **Open Library API** to automatically retrieve:

* Book title
* Author
* Publisher
* Categories
* Description
* Cover image
* Publication year
* Language

using only the ISBN number.

---

# 🖼 Screenshots

## Home Page

![Home](screenshots/home.png)

## Books

![Books](screenshots/books.png)

## Add Members

![Members](screenshots/add_member.png)

## Loans

![Loans](screenshots/loans.png)

---

# 🚀 Getting Started

```bash
git clone https://github.com/KonnaChrys/Green-Hill-Library.git

pip install -r requirements.txt

python app.py
```

Configure your MySQL database connection before running the application.

---

# 🚀 Future Improvements

* User authentication
* Reservation system
* Dashboard with statistics
* Email notifications
* Export reports
* Mobile friendly interface

---

# 👨‍💻 Author

Developed as a personal software development project.

---

⭐ If you like this project, feel free to give it a star!
