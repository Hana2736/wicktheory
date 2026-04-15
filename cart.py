"""Shop + cart + checkout view for Wick Theory.

Preserves Aiden's original single-page layout (shop in the left column,
cart in the right, sidebar checkout settings, tax explainer, and checkout
form). Integration changes only:
- no set_page_config (owned by app.py)
- products come from the shared session-state catalog (so admin edits stick)
- successful checkout records the order in session_state.orders
- checkout form prefills from the signed-in user, if any

Added features:
- Discount code application (WELCOME10, CANDLE20, FREESHIP)
- Search by name/scent/description on the Shop page
- Sort by price (low/high) and availability on the Shop page
- Stock deduction on successful checkout
"""

import streamlit as st

from data import STATE_TAX_RATES, SHIPPING_OPTIONS, DISCOUNT_CODES, PRODUCTS, money


DEFAULT_SETTINGS = {
    "maintenance": False,
    "allow_signups": True,
    "allow_coupons": True,
}


def initialize_state() -> None:
    if "cart" not in st.session_state:
        st.session_state.cart = {}
    if "selected_state" not in st.session_state:
        st.session_state.selected_state = "Texas"
    if "shipping_method" not in st.session_state:
        st.session_state.shipping_method = "Standard (5-7 days)"
    if "orders" not in st.session_state:
        st.session_state.orders = []
    if "products" not in st.session_state:
        st.session_state.products = [dict(p) for p in PRODUCTS]
    if "settings" not in st.session_state:
        st.session_state.settings = dict(DEFAULT_SETTINGS)
    if "applied_coupon" not in st.session_state:
        st.session_state.applied_coupon = None   # (code, rate) tuple or None


def add_to_cart(product_id: str) -> None:
    product = get_product(product_id)
    if product and product.get("stock", 0) > st.session_state.cart.get(product_id, 0):
        st.session_state.cart[product_id] = st.session_state.cart.get(product_id, 0) + 1


def remove_from_cart(product_id: str) -> None:
    if product_id in st.session_state.cart:
        del st.session_state.cart[product_id]


def update_quantity(product_id: str, quantity: int) -> None:
    if quantity <= 0:
        remove_from_cart(product_id)
    else:
        product = get_product(product_id)
        if product:
            capped = min(quantity, product.get("stock", quantity))
            st.session_state.cart[product_id] = capped


def get_product(product_id: str):
    return next((p for p in st.session_state.products if p["id"] == product_id), None)


def calculate_subtotal() -> float:
    subtotal = 0.0
    for product_id, quantity in st.session_state.cart.items():
        product = get_product(product_id)
        if product:
            subtotal += product["price"] * quantity
    return subtotal


def get_tax_rate(state_name: str) -> float:
    return STATE_TAX_RATES.get(state_name, 0.0)


def calculate_tax(subtotal: float, state_name: str) -> float:
    return subtotal * get_tax_rate(state_name)


def calculate_discount(subtotal: float, coupon_code: str | None) -> tuple[float, float]:
    """Return (discount_amount, effective_shipping_override).
    
    Returns (discount_off_subtotal, 0.0) for percent-off codes.
    Returns (0.0, -1.0) sentinel for FREESHIP (caller sets shipping to 0).
    """
    if not coupon_code:
        return 0.0, 0.0
    rate = DISCOUNT_CODES.get(coupon_code.upper(), None)
    if rate is None:
        return 0.0, 0.0
    if coupon_code.upper() == "FREESHIP":
        return 0.0, -1.0   # sentinel: free shipping
    return subtotal * rate, 0.0


def calculate_total(subtotal: float, discount: float, tax: float, shipping_cost: float) -> float:
    return max(0.0, subtotal - discount) + tax + shipping_cost


def deduct_stock(cart: dict) -> None:
    """Decrement stock for each product in the cart after a successful order."""
    for product_id, quantity in cart.items():
        for product in st.session_state.products:
            if product["id"] == product_id:
                product["stock"] = max(0, product.get("stock", 0) - quantity)
                break


# ---------- Shop Page ----------

def render_shop() -> None:
    st.title("🕯️ Wick Theory")
    st.caption("Browse the full catalog, then head to your cart to check out.")

    cart_count = sum(st.session_state.cart.values())
    if cart_count:
        st.info(f"You have **{cart_count}** item(s) in your cart. Open the Cart page from the sidebar to check out.")

    # ---- Search & Sort controls ----
    st.subheader("Shop Candles")
    col_search, col_sort = st.columns([3, 1])
    search_query = col_search.text_input(
        "Search candles",
        placeholder="Search by name, scent, or description…",
        label_visibility="collapsed",
    )
    sort_option = col_sort.selectbox(
        "Sort",
        ["Default", "Price: Low → High", "Price: High → Low", "Availability"],
        label_visibility="collapsed",
    )

    # ---- Filter ----
    products = list(st.session_state.products)
    if search_query:
        q = search_query.lower()
        products = [
            p for p in products
            if q in p["name"].lower()
            or q in p.get("scent", "").lower()
            or q in p.get("description", "").lower()
        ]

    # ---- Sort ----
    if sort_option == "Price: Low → High":
        products = sorted(products, key=lambda p: p["price"])
    elif sort_option == "Price: High → Low":
        products = sorted(products, key=lambda p: p["price"], reverse=True)
    elif sort_option == "Availability":
        products = sorted(products, key=lambda p: p.get("stock", 0), reverse=True)

    if not products:
        st.warning("No candles match your search. Try a different term.")
        return

    product_cols = st.columns(3)
    for index, product in enumerate(products):
        with product_cols[index % 3]:
            with st.container(border=True):
                if product.get("image"):
                    try:
                        st.image(product["image"], use_container_width=True)
                    except Exception:
                        pass
                st.markdown(f"### {product['name']}")
                st.write(f"**Scent:** {product['scent']}")
                st.write(f"**Size:** {product['size']}")
                st.write(product["description"])
                st.write(f"**Price:** {money(product['price'])}")

                stock = product.get("stock", 0)
                if stock == 0:
                    st.error("Out of stock")
                else:
                    st.caption(f"In stock: {stock}")
                    st.button(
                        f"Add {product['name']} to cart",
                        key=f"add_{product['id']}",
                        on_click=add_to_cart,
                        args=(product["id"],),
                        use_container_width=True,
                    )


# ---------- Cart Page ----------

def render_cart() -> None:
    st.title("🕯️ Wick Theory")
    st.caption("Your cart, tax breakdown, and checkout form.")

    st.sidebar.header("Checkout Settings")
    st.session_state.selected_state = st.sidebar.selectbox(
        "Where is the order being purchased/shipped?",
        list(STATE_TAX_RATES.keys()),
        index=list(STATE_TAX_RATES.keys()).index(st.session_state.selected_state),
    )
    st.session_state.shipping_method = st.sidebar.selectbox(
        "Shipping method",
        list(SHIPPING_OPTIONS.keys()),
        index=list(SHIPPING_OPTIONS.keys()).index(st.session_state.shipping_method),
    )

    selected_rate = get_tax_rate(st.session_state.selected_state)
    shipping_cost = SHIPPING_OPTIONS[st.session_state.shipping_method]

    st.subheader("Your Cart")

    if not st.session_state.cart:
        st.info("Your cart is empty. Head to the Shop page to add a candle.")
    else:
        for product_id, quantity in list(st.session_state.cart.items()):
            product = get_product(product_id)
            if not product:
                continue

            with st.container(border=True):
                cols = st.columns([3, 2, 1])
                cols[0].write(f"**{product['name']}**")
                cols[0].write(f"Unit price: {money(product['price'])}")
                new_qty = cols[1].number_input(
                    f"Quantity for {product['name']}",
                    min_value=0,
                    max_value=product.get("stock", 99),
                    step=1,
                    value=quantity,
                    key=f"qty_{product_id}",
                )
                update_quantity(product_id, int(new_qty))
                line_total = product["price"] * st.session_state.cart.get(product_id, 0)
                cols[1].write(f"Line total: {money(line_total)}")
                cols[2].button(
                    "Remove",
                    key=f"remove_{product_id}",
                    on_click=remove_from_cart,
                    args=(product_id,),
                    use_container_width=True,
                )

    subtotal = calculate_subtotal()

    # ---- Discount / Coupon ----
    st.markdown("---")
    st.subheader("Discount Code")

    coupons_allowed = st.session_state.settings.get("allow_coupons", True)
    if not coupons_allowed:
        st.caption("Coupon codes are currently disabled.")
    else:
        coupon_col, btn_col, clear_col = st.columns([3, 1, 1])
        coupon_input = coupon_col.text_input(
            "Enter coupon code",
            label_visibility="collapsed",
            placeholder="e.g. WELCOME10",
        )
        if btn_col.button("Apply", use_container_width=True):
            code = coupon_input.strip().upper()
            if code in DISCOUNT_CODES:
                st.session_state.applied_coupon = code
                st.success(f"Coupon **{code}** applied!")
            else:
                st.error("Invalid coupon code.")
        if clear_col.button("Remove", use_container_width=True):
            st.session_state.applied_coupon = None
            st.info("Coupon removed.")

        if st.session_state.applied_coupon:
            st.caption(f"Active coupon: **{st.session_state.applied_coupon}**")

    # ---- Totals ----
    applied = st.session_state.applied_coupon if coupons_allowed else None
    discount_amount, ship_override = calculate_discount(subtotal, applied)

    effective_shipping = 0.0 if ship_override == -1.0 else shipping_cost
    tax = calculate_tax(max(0.0, subtotal - discount_amount), st.session_state.selected_state)
    total = calculate_total(subtotal, discount_amount, tax, effective_shipping)

    st.markdown("---")
    st.write(f"**Subtotal:** {money(subtotal)}")
    if discount_amount > 0:
        st.write(f"**Discount ({applied}):** -{money(discount_amount)}")
    if ship_override == -1.0:
        st.write(f"**Shipping:** ~~{money(shipping_cost)}~~ FREE (coupon applied)")
    else:
        st.write(f"**Shipping:** {money(effective_shipping)}")
    st.write(f"**Sales tax ({selected_rate * 100:.2f}% — {st.session_state.selected_state}):** {money(tax)}")
    st.write(f"## Total: {money(total)}")

    st.markdown("---")
    st.subheader("How the sales tax logic works")
    st.write(
        "The app uses the customer's selected state to look up a sales-tax rate, "
        "then multiplies that rate by the discounted cart subtotal."
    )

    with st.expander("Show tax formula used in this project"):
        st.code(
            """tax_rate   = STATE_TAX_RATES[selected_state]
discounted = subtotal - discount_amount
tax_amount = discounted * tax_rate
total      = discounted + tax_amount + shipping_cost"""
        )

    # ---- Checkout Form ----
    st.subheader("Simple checkout form")
    with st.form("checkout_form"):
        default_name = default_email = default_addr = ""
        if st.session_state.get("logged_in"):
            u = st.session_state.users_db[st.session_state.current_user]
            default_name = u["name"]
            default_email = st.session_state.current_user
            default_addr = u["address"]

        name = st.text_input("Full name", value=default_name)
        email = st.text_input("Email", value=default_email)
        address = st.text_input("Shipping address", value=default_addr)
        submitted = st.form_submit_button("Place order")

        if submitted:
            if not st.session_state.cart:
                st.error("Your cart is empty.")
            elif not name or not email or not address:
                st.error("Please fill in your name, email, and shipping address.")
            else:
                order_no = f"WCT-2026-{10500 + len(st.session_state.orders):07d}"

                # Deduct stock before clearing the cart
                deduct_stock(st.session_state.cart)

                st.session_state.orders.append({
                    "order_no": order_no,
                    "customer": name,
                    "email": email,
                    "items": dict(st.session_state.cart),
                    "subtotal": subtotal,
                    "discount": discount_amount,
                    "coupon": applied,
                    "tax": tax,
                    "shipping": effective_shipping,
                    "total": total,
                    "status": "paid",
                })

                # Clear cart and coupon
                st.session_state.cart = {}
                st.session_state.applied_coupon = None

                st.success(
                    f"Thanks, {name}! Your demo order total is {money(total)}. "
                    "This school-project version does not process real payments."
                )
