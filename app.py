"""Wick Theory — unified Streamlit entrypoint.

Sets page config once, initializes shared session state, and routes between
the Home, Shop, Cart, and Account views.
"""

import streamlit as st

import admin
import auth
import cart
from data import PRODUCTS, money


st.set_page_config(page_title="Wick Theory", layout="wide")

auth.initialize_state()
cart.initialize_state()


def _sidebar_nav() -> str:
    st.sidebar.title("Wick Theory")

    if st.session_state.logged_in:
        user = st.session_state.users_db[st.session_state.current_user]
        st.sidebar.success(f"Signed in as **{user['name']}**")
    else:
        st.sidebar.info("Browsing as guest")

    options = ["Home", "Shop", "Account"]
    is_admin = (
        st.session_state.logged_in
        and st.session_state.users_db[st.session_state.current_user]["role"] == "admin"
    )
    if is_admin:
        options.append("Admin")
    default_index = 0
    if st.session_state.get("active_nav") in options:
        default_index = options.index(st.session_state.active_nav)
    choice = st.sidebar.radio("Navigate", options, index=default_index)
    st.session_state.active_nav = choice
    return choice


def _render_home() -> None:
    st.title("Wick Theory")
    st.subheader("Small-batch candles, built for any room.")
    st.write(
        "Browse three sizes across citrus, floral, fruity, earthy, and gourmet scents. "
        "Add a candle to your cart, apply a discount code, and check out — all on one page."
    )

    featured = st.session_state.products[:6]
    st.markdown("### Featured")
    cols = st.columns(3)
    for i, p in enumerate(featured):
        with cols[i % 3]:
            with st.container(border=True):
                try:
                    st.image(p["image"], use_container_width=True)
                except Exception:
                    pass
                st.markdown(f"**{p['name']}**")
                st.caption(p["description"])
                st.write(money(p["price"]))

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    c1.metric("Candles in catalog", len(st.session_state.products))
    c2.metric("Orders placed (session)", len(st.session_state.orders))
    c3.metric("Registered users", len(st.session_state.users_db))


def _render_maintenance() -> None:
    st.title("Down for Maintenance")
    st.warning(
        "Wick Theory is temporarily unavailable while we update the store. "
        "Please check back shortly."
    )
    st.caption("Admins can still sign in from the Account page to manage the site.")


def main() -> None:
    choice = _sidebar_nav()
    maintenance = st.session_state.settings.get("maintenance", False)
    is_admin = (
        st.session_state.logged_in
        and st.session_state.users_db[st.session_state.current_user]["role"] == "admin"
    )

    if maintenance and not is_admin and choice not in ("Account",):
        _render_maintenance()
        return

    if choice == "Home":
        _render_home()
    elif choice == "Shop":
        cart.render()
    elif choice == "Account":
        auth.render()
    elif choice == "Admin":
        admin.render()


main()
