"""Wick Theory — unified Streamlit entrypoint.

Sets page config once, initializes shared session state, and routes
between the Shop and Account views (plus Admin for admin accounts).
"""

import streamlit as st

import admin
import auth
import cart


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

    cart_count = sum(st.session_state.cart.values()) if st.session_state.cart else 0
    cart_label = f"Cart ({cart_count})" if cart_count else "Cart"
    options = ["Shop", cart_label, "Account"]
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

    if maintenance and not is_admin and choice != "Account":
        _render_maintenance()
        return

    if choice == "Shop":
        cart.render_shop()
    elif choice.startswith("Cart"):
        cart.render_cart()
    elif choice == "Account":
        auth.render()
    elif choice == "Admin":
        admin.render()


main()
