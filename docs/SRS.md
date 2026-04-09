# Software Requirements Specification (SRS)

## CampusEats — Online Food Ordering System

| Document | Details |
|----------|---------|
| **Project** | P2 — Online Food Ordering System (web application) |
| **Product name** | CampusEats |
| **Version** | 1.0 |
| **Intended audience** | Course evaluators, developers, maintainers |

---

## 1. Introduction

### 1.1 Purpose

This SRS describes the functional and non-functional requirements for **CampusEats**, a web-based system that lets **customers** browse campus food outlets, build a cart, place orders, and track status, while **outlet managers** maintain menus and manage incoming orders. Payment is implemented as a **demo integration** (no real money).

### 1.2 Scope

**In scope:**

- User registration and authentication with role selection (customer vs outlet manager).
- Listing of active outlets and public menu browsing.
- Shopping cart (single outlet per cart), checkout with delivery details.
- Order lifecycle including demo payment and status updates by the outlet.
- Basic administration via Django Admin.

**Out of scope (current release):**

- Real payment gateways (cards, UPI, wallets).
- Push notifications, SMS, or email delivery alerts.
- Multi-outlet carts, table booking, or rider assignment maps.
- Native mobile apps.

### 1.3 Definitions

| Term | Meaning |
|------|---------|
| **Customer** | User role that orders food. |
| **Outlet manager** | User role that owns one outlet and manages menu and orders. |
| **Outlet** | A restaurant / stall entity with name, address, and menu. |
| **Demo payment** | Simulated payment success or failure for coursework demonstration. |

### 1.4 References

- Django documentation: https://docs.djangoproject.com/
- Bootstrap 5 documentation: https://getbootstrap.com/docs/5.3/

---

## 2. Overall Description

### 2.1 Product Perspective

CampusEats is a standalone **three-tier** application: browser (HTML/CSS/Bootstrap), Django application server, and SQLite (or configurable MySQL/PostgreSQL) database. It does not depend on external payment APIs in the current build.

### 2.2 User Classes

| User class | Description |
|------------|-------------|
| **Guest** | Unauthenticated visitor; can browse outlets and menus only. |
| **Customer** | Authenticated user with customer role; cart, checkout, orders, demo payment. |
| **Outlet manager** | Authenticated user with owner role; one outlet, menu CRUD, order list and status updates. |
| **Administrator** | Superuser; Django Admin for data oversight. |

### 2.3 Operating Environment

- **Server OS:** Windows 11 or Linux (e.g. Ubuntu).
- **Client:** Modern web browser (Chrome, Edge, Firefox).
- **Runtime:** Python 3.x, Django 5.x/6.x.

### 2.4 Design and Implementation Constraints

- Must use Django’s authentication for passwords (hashed).
- Logout must use POST (Django security default).
- Cart enforces **one outlet** per cart at a time.

---

## 3. Functional Requirements

### 3.1 User Registration and Login

| ID | Requirement |
|----|---------------|
| FR-AUTH-1 | The system shall allow new users to register with username, email, password, optional phone, and role (customer or outlet manager). |
| FR-AUTH-2 | The system shall authenticate users with username and password. |
| FR-AUTH-3 | The system shall allow users to log out via a POST request. |
| FR-AUTH-4 | Each user shall have exactly one profile record linked to their account (role, phone). |

### 3.2 Outlet and Menu Management (Outlet Manager)

| ID | Requirement |
|----|---------------|
| FR-MENU-1 | An outlet manager shall create or update their outlet (name, description, address, phone, active flag). |
| FR-MENU-2 | An outlet manager shall add, edit, and delete menu items (name, description, price, optional image, availability). |
| FR-MENU-3 | Only outlet managers may access outlet and menu management URLs; customers shall be denied with an appropriate message. |

### 3.3 Browsing and Cart (Customer)

| ID | Requirement |
|----|---------------|
| FR-BROWSE-1 | The system shall list all **active** outlets to any visitor. |
| FR-BROWSE-2 | The system shall display available menu items for a selected outlet. |
| FR-CART-1 | A logged-in customer shall add available items to a cart. |
| FR-CART-2 | If the cart already contains items from another outlet, adding from a different outlet shall be blocked until the cart is cleared or checkout completes. |
| FR-CART-3 | The customer shall update quantities, remove lines, or clear the entire cart. |

### 3.4 Checkout and Orders

| ID | Requirement |
|----|---------------|
| FR-ORD-1 | The customer shall place an order from the cart with mandatory delivery address and optional phone. |
| FR-ORD-2 | On placement, the system shall create an order with line items (snapshot of name, unit price, quantity), clear the cart, and set status to **waiting for payment** with `is_paid = false`. |
| FR-ORD-3 | The customer shall view a list of their orders and open order detail. |
| FR-ORD-4 | The outlet manager shall view orders for their outlet and open order detail. |

### 3.5 Demo Payment

| ID | Requirement |
|----|---------------|
| FR-PAY-1 | After order placement, the customer shall reach a demo checkout page for that order. |
| FR-PAY-2 | On **success**, the system shall record a payment row, set the order paid, and set status to **order received**. |
| FR-PAY-3 | On **failure**, the system shall record a failed payment; the order remains unpaid and the customer may retry. |
| FR-PAY-4 | Paid orders shall not accept duplicate successful payment for the same flow (user is redirected with an informational message). |

### 3.6 Order Tracking (Status)

| ID | Requirement |
|----|---------------|
| FR-TRK-1 | The customer shall see current order status on the order detail page. |
| FR-TRK-2 | After payment, the outlet manager shall update order status (e.g. confirmed, preparing, out for delivery, delivered, cancelled). |
| FR-TRK-3 | Status updates shall not apply to unpaid orders (business rule enforced in application logic). |

---

## 4. Non-Functional Requirements

| ID | Category | Requirement |
|----|----------|-------------|
| NFR-1 | Security | Passwords stored hashed; CSRF protection on state-changing forms; session-based authentication. |
| NFR-2 | Usability | Responsive layout using Bootstrap; clear navigation for roles. |
| NFR-3 | Maintainability | Modular Django apps (`accounts`, `restaurant`, `orders`, `payments`). |
| NFR-4 | Portability | Database abstracted; SQLite default; MySQL/PostgreSQL configurable in settings. |
| NFR-5 | Performance | Suitable for coursework / small concurrent user load; no strict SLA defined. |

---

## 5. Data Requirements

Key entities: **User**, **Profile**, **Restaurant**, **MenuItem**, **Cart**, **CartItem**, **Order**, **OrderItem**, **Payment**. Detailed structure is shown in the **ER Diagram** document (`ER_Diagram.md`).

---

## 6. External Interface Requirements

- **Web UI:** HTML templates, Bootstrap 5, forms for input, messages for feedback.
- **Admin UI:** Django Admin at `/admin/` for superusers.
- **File upload:** Menu item images stored under configured `MEDIA_ROOT`.

---

## 7. Acceptance Criteria (Summary)

The system is acceptable for the stated coursework if: (1) both roles can complete their primary flows end-to-end, (2) cart and single-outlet rule hold, (3) demo payment toggles paid/unpaid correctly, (4) outlet manager status updates reflect on customer order view, and (5) unauthorized access to role-specific pages is blocked.

---

*End of SRS*
