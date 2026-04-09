# CampusEats — Project Description & How to Run

This document gives a **detailed overview** of the online food ordering system, **how to start it** (commands), and a breakdown of **all modules** and what each one contains.

---

## 1. What this project is

**CampusEats** is a **web application** built for a college software project (Online Food Ordering System). It runs in the browser and is implemented with **Django** (Python) on the server side, **SQLite** as the default database, **HTML + Bootstrap** for the user interface, and optional **menu images** stored on disk.

### 1.1 What users can do

- **Guests** can browse campus **outlets** (food stalls / restaurants) and view **menus**.
- **Customers** (registered users who chose the ordering role) can add items to a **cart**, **check out** with a delivery address, complete a **demo payment** (no real money), and **track** order status.
- **Outlet managers** (registered users who chose the outlet role) can create their **outlet profile**, manage **menu items** (add, edit, delete, photos), see **incoming orders**, and **update order status** (e.g. preparing, out for delivery, delivered).
- **Administrators** (Django superusers) can use **Django Admin** to inspect or edit data.

### 1.2 Technical stack

| Layer | Technology |
|-------|------------|
| Backend | Django |
| Frontend | Server-rendered templates, Bootstrap 5 |
| Database | SQLite (file `db.sqlite3`); can be switched to MySQL/PostgreSQL in settings |
| Media | Uploaded menu images under `media/` |

### 1.3 Important rules built into the app

- One **cart** belongs to one user; cart lines must all be from the **same outlet** (you cannot mix two outlets without clearing the cart).
- **Logout** uses **POST** only (security); use the **Log out** button in the navbar, not the URL bar.
- **Payment** is **demo only**: success or failure is simulated for coursework, not a real gateway.

---

## 2. How many modules?

The codebase is organised as **one Django project** plus **four Django applications** (apps). Together, these are the **five main code modules** you maintain:

| # | Module name | Type | Purpose (short) |
|---|-------------|------|------------------|
| 1 | **config** | Project package | Settings, root URL routing, WSGI/ASGI |
| 2 | **accounts** | App | Registration, login, logout, user profile (role) |
| 3 | **restaurant** | App | Outlets, public menus, outlet owner CRUD |
| 4 | **orders** | App | Cart, checkout, orders, order lines, status updates |
| 5 | **payments** | App | Demo payment screen and payment records |

**Additional folders** (supporting, not separate Django apps):

| Folder | Role |
|--------|------|
| `templates/` | HTML templates (pages, base layout) |
| `static/` | Static assets (if any; CSS/JS mainly from CDN) |
| `media/` | User-uploaded files (menu images), created at runtime |
| `docs/` | Project documentation (SRS, diagrams, this file, etc.) |
| `venv/` | Python virtual environment (created locally; do not commit) |

---

## 3. What is inside each module?

### 3.1 `config` (project configuration)

| File | What it does |
|------|----------------|
| `settings.py` | Installed apps, database, templates dir, static/media, `LOGIN_URL`, messages, security-related defaults |
| `urls.py` | Mounts `/admin/`, `/accounts/`, `/orders/`, `/payments/`, and site root; serves media in DEBUG mode; Django admin titles |
| `wsgi.py` / `asgi.py` | Entry points for production or async servers |

**Root:** `manage.py` lives next to `config/` and starts Django commands.

---

### 3.2 `accounts` (users and roles)

| File | What it does |
|------|----------------|
| `models.py` | **Profile**: one-to-one with Django `User`; **role** (customer vs outlet manager), optional phone |
| `signals.py` | Ensures a **Profile** row exists when a **User** is created |
| `forms.py` | **RegisterForm** (signup with role and email) |
| `auth_forms.py` | Login form with Bootstrap-friendly widgets |
| `views.py` | Register, custom **LoginView**, custom **LogoutView** |
| `urls.py` | `/accounts/register/`, `/accounts/login/`, `/accounts/logout/` |
| `admin.py` | Profile visible in Django Admin |
| `apps.py` | Loads signals when the app starts |
| `migrations/` | Database schema history for `Profile` |

---

### 3.3 `restaurant` (outlets and menus)

| File | What it does |
|------|----------------|
| `models.py` | **Restaurant** (one per outlet manager: name, description, address, phone, active); **MenuItem** (belongs to restaurant: name, description, price, image, availability) |
| `forms.py` | Forms to edit restaurant and menu items |
| `views.py` | Home (list outlets), outlet detail (menu), **owner-only**: my outlet, menu list, add/edit/delete menu item |
| `urls.py` | Public and owner URLs under site root (e.g. `/`, `/restaurant/<id>/`, `/owner/...`) |
| `admin.py` | Restaurant and MenuItem in admin |
| `migrations/` | Schema for `Restaurant` and `MenuItem` |

---

### 3.4 `orders` (cart, checkout, orders)

| File | What it does |
|------|----------------|
| `models.py` | **Cart** (one per user), **CartItem** (cart + menu item + quantity); **Order** (user, restaurant, status, totals, address, paid flag); **OrderItem** (snapshot lines on the order) |
| `views.py` | Add/update/remove cart lines, clear cart, checkout (creates order + clears cart), list orders (customer vs owner), order detail, **owner POST** to update status |
| `urls.py` | `/orders/cart/`, checkout, cart actions, `mine`, order detail, status update |
| `admin.py` | Cart, CartItem, Order registration |
| `migrations/` | Schema for cart and order tables |

---

### 3.5 `payments` (demo payment)

| File | What it does |
|------|----------------|
| `models.py` | **Payment**: links to order, success/fail status, unique **transaction_id**, timestamp |
| `views.py` | Demo checkout page: POST **success** or **fail** → writes `Payment`, updates order when success |
| `urls.py` | `/payments/mock/<order_id>/` |
| `admin.py` | Payment records in admin |
| `migrations/` | Schema for `Payment` |

---

## 4. How to start the project

### 4.1 Prerequisites

- **Python 3.10+** (3.12 is fine) installed and available as `python` in the terminal.
- **Windows PowerShell** (or Command Prompt) — paths below use your project folder.

### 4.2 First-time setup

Open PowerShell and run:

```powershell
cd "c:\Users\Deepak\Desktop\software project"
```

**Create virtual environment** (skip if `venv` already exists):

```powershell
python -m venv venv
```

**Activate virtual environment:**

```powershell
.\venv\Scripts\Activate.ps1
```

If execution policy blocks activation, run once (as Administrator if needed):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Install dependencies:**

```powershell
pip install -r requirements.txt
```

**Create database tables** (migrations are already in the repo; this applies them):

```powershell
python manage.py migrate
```

**Optional — create admin user** (for `/admin/`):

```powershell
python manage.py createsuperuser
```

Follow the prompts for username, email, and password.

### 4.3 Run the development server

With the venv **activated** and current directory still the project root:

```powershell
python manage.py runserver
```

Default URL: **http://127.0.0.1:8000/**

To use another port:

```powershell
python manage.py runserver 8080
```

### 4.4 Quick command reference

| Goal | Command |
|------|---------|
| Activate venv | `.\venv\Scripts\Activate.ps1` |
| Install packages | `pip install -r requirements.txt` |
| Apply DB migrations | `python manage.py migrate` |
| Create new migrations after model change | `python manage.py makemigrations` |
| Run server | `python manage.py runserver` |
| Django system check | `python manage.py check` |
| Admin user | `python manage.py createsuperuser` |

### 4.5 After pulling changes from Git

```powershell
cd "c:\Users\Deepak\Desktop\software project"
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 5. URLs at a glance

| Path | Meaning |
|------|---------|
| `/` | Home — list of outlets |
| `/accounts/register/` | Sign up |
| `/accounts/login/` | Log in |
| `/orders/cart/` | Shopping cart (customer) |
| `/orders/checkout/` | Checkout |
| `/payments/mock/<id>/` | Demo payment for order `id` |
| `/admin/` | Django Admin (superuser) |

Exact paths for outlet owner pages are under `/owner/...` in `restaurant/urls.py`.

---

## 6. Suggested demo flow (for viva / report)

1. Register as **outlet manager** → create outlet → add menu items (with optional image).  
2. Register as **customer** (or use incognito) → open outlet → add to cart → checkout → **demo payment success**.  
3. Log in as outlet manager → **Kitchen orders** → open order → update status.  
4. Log in as customer → **My orders** → confirm status text updated.

---

*Document version: 1.0 — matches CampusEats Django codebase structure.*
