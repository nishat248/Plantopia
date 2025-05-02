# 🛍️ Plantopia

A full-featured eCommerce platform built with Django. This project supports product browsing, cart and wishlist management, user authentication, order handling, and a simple blog section for articles.

## 🚀 Features

- Product listing, categories, and product detail pages
- Add to Cart and Wishlist
- Dynamic Cart and Order Summary pages
- User Registration, Login, Profile with editable details and profile image
- Order placement and stock management
- Blog with article preview and detail pages
- Admin panel to manage products, categories, orders, users, and blog posts
- Custom popups and styled components with consistent theming

---

## 🛠️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/nishat248/Plantopia.git
cd Plantopia
````

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser (for admin access)

```bash
python manage.py createsuperuser
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

Then open your browser and go to:
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🧪 Sample Admin Setup

* Login at: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
* Add products, categories, and blog posts
* Manage users, orders, and inventory

---

## 📂 Project Structure (Important Folders)

```
shop/                 # Your main app with all models and views
templates/            # All HTML templates
static/               # Static files (CSS, JS, images)
media/                # Uploaded media files (profile images, etc.)
```

---

## 📌 Notes

* Product detail URLs use slugs, but internal logic uses product IDs.
* Cart, Wishlist, and Orders work only for logged-in users.
* Stock quantity is validated before adding to cart or placing an order.
* Profile edit and order history available under user dashboard.

---

## 📄 License

This project is open-source and free to use under the [MIT License](LICENSE).
