# Recipe Management API

A Django REST Framework project for managing recipes, categories, and ingredients.  
Supports JWT authentication for secure access.

---

## Features
- User registration & JWT login
- Create, update, delete categories
- Add recipes with ingredients & quantities
- List recipes by user
- Update recipes with PATCH/PUT

---

##  Tech Stack
- Django & Django REST Framework
- JWT Authentication (`djangorestframework-simplejwt`)
- SQLite (default, can be switched to PostgreSQL)

---

##  API Endpoints

### Auth
- `POST /api/accounts/register/` – Register new user
- `POST /api/token/` – Get JWT access & refresh token
- `POST /api/token/refresh/` – Refresh JWT token

### Categories
- `GET /api/recipes/categories/` – List categories
- `POST /api/recipes/categories/` – Create category

### Ingredients
- `GET /api/recipes/ingredients/` – List ingredients
- `POST /api/recipes/ingredients/` – Create ingredient

### Recipes
- `GET /api/recipes/recipes/` – List recipes
- `POST /api/recipes/recipes/` – Create recipe
- `PATCH /api/recipes/recipes/<id>/` – Update recipe
- `DELETE /api/recipes/recipes/<id>/` – Delete recipe

---

## ▶️ Demo Video
👉 [Loom Video Link Here](#)

---

## ⚙️ Installation
```bash
git clone https://github.com/Kalkidan-dev/Alx_DjangoLearnLab.git
cd advanced_features_and_security/LibraryProject
python -m venv recipe_env
recipe_env\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
