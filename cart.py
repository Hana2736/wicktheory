import streamlit as st

st.set_page_config(page_title="Wick Theory", page_icon="🕯️", layout="wide")

PRODUCTS = [
    {
        "id": "lavender_dream",
        "name": "Lavender Dream",
        "scent": "Lavender + Vanilla",
        "price": 18.00,
        "size": "8 oz",
        "description": "A calming candle made for winding down in the evening.",
    },
    {
        "id": "citrus_sunrise",
        "name": "Citrus Sunrise",
        "scent": "Orange + Lemon",
        "price": 16.50,
        "size": "8 oz",
        "description": "A bright, fresh scent that works well in kitchens and living rooms.",
    },
    {
        "id": "midnight_amber",
        "name": "Midnight Amber",
        "scent": "Amber + Musk",
        "price": 22.00,
        "size": "10 oz",
        "description": "A warm, richer candle for cozy nights and gift bundles.",
    },
    {
        "id": "pine_cabin",
        "name": "Pine Cabin",
        "scent": "Pine + Cedar",
        "price": 20.00,
        "size": "10 oz",
        "description": "A woodsy seasonal candle with a crisp, outdoors feel.",
    },
]

# Example sales tax rates by state for a school/demo project.
# These are sample values so the logic works differently by location.
STATE_TAX_RATES = {
    "Alabama": 0.04,
    "Alaska": 0.00,
    "Arizona": 0.056,
    "Arkansas": 0.065,
    "California": 0.0725,
    "Colorado": 0.029,
    "Connecticut": 0.0635,
    "Delaware": 0.00,
    "Florida": 0.06,
    "Georgia": 0.04,
    "Hawaii": 0.04,
    "Idaho": 0.06,
    "Illinois": 0.0625,
    "Indiana": 0.07,
    "Iowa": 0.06,
    "Kansas": 0.065,
    "Kentucky": 0.06,
    "Louisiana": 0.0445,
    "Maine": 0.055,
    "Maryland": 0.06,
    "Massachusetts": 0.0625,
    "Michigan": 0.06,
    "Minnesota": 0.06875,
    "Mississippi": 0.07,
    "Missouri": 0.04225,
    "Montana": 0.00,
    "Nebraska": 0.055,
    "Nevada": 0.0685,
    "New Hampshire": 0.00,
    "New Jersey": 0.06625,
    "New Mexico": 0.05125,
    "New York": 0.04,
    "North Carolina": 0.0475,
    "North Dakota": 0.05,
    "Ohio": 0.0575,
    "Oklahoma": 0.045,
    "Oregon": 0.00,
    "Pennsylvania": 0.06,
    "Rhode Island": 0.07,
    "South Carolina": 0.06,
    "South Dakota": 0.042,
    "Tennessee": 0.07,
    "Texas": 0.0625,
    "Utah": 0.061,
    "Vermont": 0.06,
    "Virginia": 0.053,
    "Washington": 0.065,
    "West Virginia": 0.06,
    "Wisconsin": 0.05,
    "Wyoming": 0.04,
    "Washington, D.C.": 0.06,
}

SHIPPING_OPTIONS = {
    "Standard (5-7 days)": 6.99,
    "Express (2-3 days)": 12.99,
    "Free pickup": 0.00,
}


def money(amount: float) -> str:
    return f"${amount:,.2f}"


def initialize_state() -> None:
    if "cart" not in st.session_state:
        st.session_state.cart = {}
    if "selected_state" not in st.session_state:
        st.session_state.selected_state = "Texas"
    if "shipping_method" not in st.session_state:
        st.session_state.shipping_method = "Standard (5-7 days)"



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
    return next((item for item in PRODUCTS if item["id"] == product_id), None)



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


initialize_state()

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

    for index, product in enumerate(PRODUCTS):
        with product_cols[index % 2]:
            with st.container(border=True):
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
    name = st.text_input("Full name")
    email = st.text_input("Email")
    address = st.text_input("Shipping address")
    submitted = st.form_submit_button("Place order")

    if submitted:
        if not st.session_state.cart:
            st.error("Your cart is empty.")
        elif not name or not email or not address:
            st.error("Please fill in your name, email, and shipping address.")
        else:
            st.success(
                f"Thanks, {name}! Your demo order total is {money(total)}. "
                "This school-project version does not process real payments."
            )
