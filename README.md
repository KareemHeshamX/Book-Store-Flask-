# The Book Store — Modern Literary E-Commerce

A premium, minimalist e-commerce web application for an independent bookstore built with Flask, SQLAlchemy, and Tailwind CSS. The interface adheres strictly to a "Modern Literary" design system, utilizing curated color palettes, elegant typography, and subtle micro-animations to create a high-end browsing experience.

## ✨ Features

- **Storefront & Catalog:** Dynamic catalog filtering by category and format, equipped with a live search-as-you-type JSON API.
- **Cart & Checkout:** Persistent user-linked shopping carts, quantity adjusters, and a simulated secure checkout flow.
- **User Authentication:** Fully featured registration and session-based login.
- **Profile Management:** Users can update their personal details, change passwords securely, and upload profile pictures.
- **Order History:** Expandable, interactive history of all past acquisitions.
- **Admin Dashboard:** A secure backend interface restricted to administrators to monitor total sales, perform CRUD operations on the book catalog (add/edit/delete), and manage user roles.
- **Responsive Design:** Pixel-perfect implementation matching the provided design specifications across mobile and desktop.

## 🛠 Tech Stack

- **Backend:** Python 3, Flask, Flask-SQLAlchemy, Flask-Login, Werkzeug
- **Database:** SQLite (local persistent storage)
- **Frontend:** HTML5, Jinja2 Templating, Tailwind CSS (via CDN)
- **Typography & Icons:** Bodoni Moda (Display), Hanken Grotesk (Body), Material Symbols Outlined

## 🚀 Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd "Book Store (Flask)"
   ```

2. **Install Dependencies:**
   Ensure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   ```bash
   python app.py
   ```
   *Note: On the first run, the SQLite database (`instance/bookstore.db`) is automatically generated and seeded with 10 premium books and a demo Administrator account.*

## 🔑 Demo Credentials

Upon initialization, the following demo admin account is created automatically:
- **Name:** Kareem Hesham
- **Email:** `kareem.hesham@example.com`
- **Username:** `@kareem_hesham`
- **Password:** `password123`

## ☁️ Deployment Notes

This project utilizes a local SQLite database and local file uploads (`static/uploads/`). 
If deploying to a modern cloud provider (like Render or Heroku) that utilizes an ephemeral file system, you must migrate the database to PostgreSQL and image storage to an S3-compatible bucket (like Cloudinary) to prevent data loss upon server restarts. For free deployment without modifying code, **PythonAnywhere** is highly recommended.
