# Sequence Diagrams

## CampusEats — Online Food Ordering System

Diagrams use **Mermaid** syntax. Open in a Mermaid-compatible viewer or paste into https://mermaid.live.

---

## 1. Customer — Place order and complete demo payment

Shows the main flow from checkout through unpaid order to successful demo payment.

```mermaid
sequenceDiagram
    actor Customer
    participant Browser
    participant Django as Django App
    participant DB as Database

    Customer->>Browser: Open checkout, enter address
    Browser->>Django: POST /orders/checkout/
    Django->>DB: BEGIN transaction
    Django->>DB: INSERT Order (status=pending_payment, is_paid=false)
    Django->>DB: INSERT OrderItem rows (snapshots)
    Django->>DB: DELETE CartItem rows
    Django->>DB: COMMIT
    Django->>Browser: Redirect to demo payment
    Browser->>Customer: Show demo checkout page

    Customer->>Browser: Click "Payment succeeds"
    Browser->>Django: POST /payments/mock/{order_id}/
    Django->>DB: INSERT Payment (success, transaction_id)
    Django->>DB: UPDATE Order (is_paid=true, status=placed)
    Django->>Browser: Redirect to order detail
    Browser->>Customer: Show paid order + status
```

---

## 2. Customer — Add item to cart (same outlet)

```mermaid
sequenceDiagram
    actor Customer
    participant Browser
    participant Django as Django App
    participant DB as Database

    Customer->>Browser: Click "Add to my cart"
    Browser->>Django: POST /orders/cart/add/{menu_item_id}/
    Django->>DB: get_or_create Cart for user
    alt Cart empty or same outlet as existing lines
        Django->>DB: get_or_create CartItem, increment qty if exists
        Django->>Browser: Redirect + success message
    else Different outlet in cart
        Django->>Browser: Redirect + warning message
    end
```

---

## 3. Outlet manager — Update order status after payment

```mermaid
sequenceDiagram
    actor Manager as Outlet Manager
    participant Browser
    participant Django as Django App
    participant DB as Database

    Manager->>Browser: Open order detail, select new status
    Browser->>Django: POST /orders/{id}/status/
    Django->>DB: SELECT Order (must belong to manager's restaurant)
    alt Order not paid
        Django->>Browser: Error message, no update
    else Valid status
        Django->>DB: UPDATE Order.status
        Django->>Browser: Redirect + success message
    end
    Manager->>Browser: Customer sees updated status on refresh
```

---

## 4. Registration and profile creation (conceptual)

```mermaid
sequenceDiagram
    actor User
    participant Browser
    participant Django as Django App
    participant DB as Database

    User->>Browser: Submit registration form
    Browser->>Django: POST /accounts/register/
    Django->>DB: INSERT User
    Note over Django,DB: Signal creates Profile with default role
    Django->>DB: UPDATE Profile (role, phone from form)
    Django->>Browser: Log in session + redirect
```

---

## 5. Diagram index

| # | Scenario |
|---|----------|
| 1 | Checkout → create order → demo payment success |
| 2 | Add to cart with single-outlet rule |
| 3 | Outlet manager updates tracking status |
| 4 | Register user and persist role on profile |

---

*End of Sequence Diagram document*
