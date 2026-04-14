"""Shop + cart + checkout view for Wick Theory.

Preserves Aiden's original single-page layout (shop in the left column,
cart in the right, sidebar checkout settings, tax explainer, and checkout
form). Integration changes only:
- no set_page_config (owned by app.py)
- products come from the shared session-state catalog (so admin edits stick)
- successful checkout records the order in session_state.orders
- checkout form prefills from the signed-in user, if any
"""

import streamlit as st

from data import STATE_TAX_RATES, SHIPPING_OPTIONS, PRODUCTS, money


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


def add_to_cart(product_id: str) -> None:
    st.session_state.cart[product_id] = st.session_state.cart.get(product_id, 0) + 1


def remove_from_cart(product_id: str) -> None:
    if product_id in st.session_state.cart:
        del st.session_state.cart[product_id]


def update_quantity(product_id: str, quantity: int) -> None:
    if quantity <= 0:
        remove_from_cart(product_id)
    else:
        st.session_state.cart[product_id] = quantity


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


def calculate_total(subtotal: float, tax: float, shipping_cost: float) -> float:
    return subtotal + tax + shipping_cost


def render() -> None:
    st.title("🕯️ Wick Theory")
    st.caption("Candle store project with sales-tax logic and a working shopping cart.")

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

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Shop Candles")
        product_cols = st.columns(2)

        for index, product in enumerate(st.session_state.products):
            with product_cols[index % 2]:
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
                    st.button(
                        f"Add {product['name']} to cart",
                        key=f"add_{product['id']}",
                        on_click=add_to_cart,
                        args=(product["id"],),
                        use_container_width=True,
                    )

    with col2:
        st.subheader("Your Cart")

        if not st.session_state.cart:
            st.info("Your cart is empty. Add a candle to get started.")
        else:
            for product_id, quantity in list(st.session_state.cart.items()):
                product = get_product(product_id)
                if not product:
                    continue

                with st.container(border=True):
                    st.write(f"**{product['name']}**")
                    st.write(f"Unit price: {money(product['price'])}")
                    new_qty = st.number_input(
                        f"Quantity for {product['name']}",
                        min_value=0,
                        step=1,
                        value=quantity,
                        key=f"qty_{product_id}",
                    )
                    update_quantity(product_id, int(new_qty))
                    line_total = product["price"] * st.session_state.cart.get(product_id, 0)
                    st.write(f"Line total: {money(line_total)}")
                    st.button(
                        f"Remove {product['name']}",
                        key=f"remove_{product_id}",
                        on_click=remove_from_cart,
                        args=(product_id,),
                        use_container_width=True,
                    )

        subtotal = calculate_subtotal()
        tax = calculate_tax(subtotal, st.session_state.selected_state)
        total = calculate_total(subtotal, tax, shipping_cost)

        st.markdown("---")
        st.write(f"**Subtotal:** {money(subtotal)}")
        st.write(f"**Sales tax ({selected_rate * 100:.2f}% - {st.session_state.selected_state}):** {money(tax)}")
        st.write(f"**Shipping:** {money(shipping_cost)}")
        st.write(f"## Total: {money(total)}")

    st.markdown("---")
    st.subheader("How the sales tax logic works")
    st.write(
        "The app uses the customer's selected state to look up a sales-tax rate, "
        "then multiplies that rate by the cart subtotal."
    )

    with st.expander("Show tax formula used in this project"):
        st.code(
            """tax_rate = STATE_TAX_RATES[selected_state]
tax_amount = subtotal * tax_rate
total = subtotal + tax_amount + shipping_cost"""
        )

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
                st.session_state.orders.append({
                    "order_no": order_no,
                    "customer": name,
                    "email": email,
                    "items": dict(st.session_state.cart),
                    "subtotal": subtotal,
                    "tax": tax,
                    "shipping": shipping_cost,
                    "total": total,
                    "status": "paid",
                })
                st.session_state.cart = {}
                st.success(
                    f"Thanks, {name}! Your demo order total is {money(total)}. "
                    "This school-project version does not process real payments."
                )
