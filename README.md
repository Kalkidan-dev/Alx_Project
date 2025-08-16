# Recipe Management API

## Overview
A backend API built with **Django** and **DRF** for managing recipes. Users can perform CRUD operations on recipes and their accounts, search/filter by category or ingredients, and securely manage their data.

## Features
- **Recipes CRUD:** Title, Description, Ingredients, Instructions, Category, Prep/Cook Time, Servings.  
- **User Management:** Register, login, and manage own recipes.  
- **Search & Filter:** By title, category, ingredients, prep/cook time, or servings.  
- **Pagination & Sorting:** Efficient listing of recipes.  
- **Security:** CSRF protection, HTTPS-ready, secure cookies, HSTS, and clickjacking prevention.  

## Installation
```bash
git clone https://github.com/yourusername/Alx_DjangoLearnLab.git
cd advanced_features_and_security/LibraryProject
python -m venv recipe_env
recipe_env\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
