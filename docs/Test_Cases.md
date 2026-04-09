# Test Cases

## CampusEats — Online Food Ordering System

**Convention:** Each case has a unique **TC ID**, **preconditions**, **steps**, **expected result**, and **pass/fail** (to be filled during execution).

---

## 1. Authentication and registration

| TC ID | Module | Preconditions | Test steps | Expected result |
|-------|--------|---------------|------------|-----------------|
| TC-AUTH-01 | Register | None | Open Sign up; fill valid username, email, matching passwords; choose **I want to order food**; submit | Account created; user logged in; redirected toward home/outlets. |
| TC-AUTH-02 | Register | None | Register with existing username | Validation error; no duplicate user. |
| TC-AUTH-03 | Register | None | Register as **I run a campus outlet** | Profile role owner; redirect toward outlet setup. |
| TC-AUTH-04 | Login | User exists | Open Log in; enter valid credentials | Session created; navbar shows user. |
| TC-AUTH-05 | Login | User exists | Enter wrong password | Error message; no session. |
| TC-AUTH-06 | Logout | User logged in | Click **Log out** (POST) | Session cleared; guest links visible. |
| TC-AUTH-07 | Logout | None | GET `/accounts/logout/` in address bar | 405 Method Not Allowed (by design). |

---

## 2. Outlet and menu (outlet manager)

| TC ID | Module | Preconditions | Test steps | Expected result |
|-------|--------|---------------|------------|-----------------|
| TC-MENU-01 | Outlet | Logged in as owner | Submit outlet form with name + address | Outlet saved; success message. |
| TC-MENU-02 | Menu | Owner with outlet | Add dish with name, price | Item appears on menu manage list. |
| TC-MENU-03 | Menu | Owner | Edit dish price | List shows updated price. |
| TC-MENU-04 | Menu | Owner | Delete dish with confirm | Item removed from list. |
| TC-MENU-05 | Access | Logged in as customer | Manually open `/owner/menu/` URL | Redirect/denial; not allowed for customer. |

---

## 3. Browsing and cart (customer)

| TC ID | Module | Preconditions | Test steps | Expected result |
|-------|--------|---------------|------------|-----------------|
| TC-CART-01 | Browse | Any | Open home | Active outlets listed. |
| TC-CART-02 | Browse | Any | Open outlet detail | Available menu items shown. |
| TC-CART-03 | Cart | Customer logged in | Add item from outlet A | Item in cart. |
| TC-CART-04 | Cart | Cart has items from A | Try add from outlet B without clearing | Warning; item not mixed; still only A. |
| TC-CART-05 | Cart | Items in cart | Change quantity in cart | Total updates; message confirms. |
| TC-CART-06 | Cart | Items in cart | Remove one line | Line gone; total recalculates. |
| TC-CART-07 | Cart | Items in cart | Clear cart | Cart empty. |
| TC-CART-08 | Cart | Guest | Try add to cart | Must log in as customer (no add or redirect per UI). |

---

## 4. Checkout and orders

| TC ID | Module | Preconditions | Test steps | Expected result |
|-------|--------|---------------|------------|-----------------|
| TC-ORD-01 | Checkout | Customer; non-empty cart | Open checkout; leave address empty; submit | Error; order not created. |
| TC-ORD-02 | Checkout | Customer; cart with items | Enter address; submit | Order created; cart empty; redirect to demo payment. |
| TC-ORD-03 | Orders | Customer with orders | Open **My orders** | Own orders listed with status. |
| TC-ORD-04 | Orders | Owner with paid orders | Open **Kitchen orders** | Orders for own outlet only. |

---

## 5. Demo payment

| TC ID | Module | Preconditions | Test steps | Expected result |
|-------|--------|---------------|------------|-----------------|
| TC-PAY-01 | Payment | Unpaid order | Choose **Payment succeeds** | `is_paid` true; status **order received**; payment row exists. |
| TC-PAY-02 | Payment | Unpaid order | Choose **Payment fails** | Order still unpaid; failed payment recorded; can retry. |
| TC-PAY-03 | Payment | Already paid order | Open demo payment URL again | Info message; redirect to order detail. |

---

## 6. Order tracking (status)

| TC ID | Module | Preconditions | Test steps | Expected result |
|-------|--------|---------------|------------|-----------------|
| TC-TRK-01 | Status | Owner; **unpaid** order | POST status update | Rejected with message; status unchanged. |
| TC-TRK-02 | Status | Owner; **paid** order | Change status to **Being prepared** | Saved; customer sees new label on detail. |
| TC-TRK-03 | Status | Customer | Open order detail | Badge matches current status. |

---

## 7. Admin

| TC ID | Module | Preconditions | Test steps | Expected result |
|-------|--------|---------------|------------|-----------------|
| TC-ADM-01 | Admin | Superuser | Log in to `/admin/` | Dashboard loads. |
| TC-ADM-02 | Admin | Superuser | Edit an order in admin | Change persists in DB. |

---

## 8. Test execution log (template)

| TC ID | Executed by | Date | Result (Pass/Fail) | Notes |
|-------|-------------|------|--------------------|-------|
| TC-AUTH-01 | | | | |
| … | | | | |

---

*End of Test Cases document*
