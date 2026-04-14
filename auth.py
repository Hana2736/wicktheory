"""Login, register, and profile views for Wick Theory.

Rendered from app.py — this module does not call set_page_config itself.
The "database" is session-state only; the real schema lives in
WickTheorySetUpScript.sql.
"""

import streamlit as st
import hashlib
import re
from datetime import datetime


def initialize_state() -> None:
    if "users_db" not in st.session_state:
        st.session_state.users_db = {
            "admin@wicktheory.com": {
                "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
                "name": "Admin User",
                "phone": "210-000-0000",
                "address": "123 Admin St, San Antonio TX",
                "role": "admin",
                "created_at": "2026-01-01",
            },
            "test@gmail.com": {
                "password_hash": hashlib.sha256("password".encode()).hexdigest(),
                "name": "Test Customer",
                "phone": "210-555-1234",
                "address": "456 Main Ave, San Antonio TX",
                "role": "customer",
                "created_at": "2026-02-01",
            },
        }
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "current_user" not in st.session_state:
        st.session_state.current_user = None
    if "auth_page" not in st.session_state:
        st.session_state.auth_page = "login"


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def is_valid_email(email: str) -> bool:
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))


def login_user(email: str, password: str) -> bool:
    db = st.session_state.users_db
    if email in db and db[email]["password_hash"] == hash_password(password):
        st.session_state.logged_in = True
        st.session_state.current_user = email
        return True
    return False


def register_user(email: str, password: str, name: str, phone: str, address: str, role: str = "customer"):
    if not st.session_state.get("settings", {}).get("allow_signups", True) and role != "admin":
        return False, "New signups are currently disabled by an administrator."
    if email in st.session_state.users_db:
        return False, "An account with this email already exists."
    st.session_state.users_db[email] = {
        "password_hash": hash_password(password),
        "name": name,
        "phone": phone,
        "address": address,
        "role": role,
        "created_at": datetime.now().strftime("%Y-%m-%d"),
    }
    return True, "Account created successfully!"


def logout() -> None:
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.auth_page = "login"


def _current_user():
    return st.session_state.users_db[st.session_state.current_user]


def _show_login() -> None:
    st.markdown("## 🕯️ Wick Theory")
    st.markdown("### Welcome back")
    st.markdown("---")

    with st.form("login_form"):
        email = st.text_input("Email address", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submitted = st.form_submit_button("Log In", use_container_width=True)

        if submitted:
            if not email or not password:
                st.error("Please fill in all fields.")
            elif not is_valid_email(email):
                st.error("Please enter a valid email address.")
            elif login_user(email, password):
                st.success(f"Welcome back, {_current_user()['name']}!")
                st.rerun()
            else:
                st.error("Incorrect email or password. Please try again.")

    st.markdown("---")
    st.markdown("Don't have an account?")
    if st.button("Create an account", use_container_width=True):
        st.session_state.auth_page = "register"
        st.rerun()

    with st.expander("🧪 Test Credentials (dev only)"):
        st.code("Customer:  test@gmail.com  /  password\nAdmin:     admin@wicktheory.com  /  admin123")


def _show_register() -> None:
    st.markdown("## 🕯️ Wick Theory")
    st.markdown("### Create your account")
    st.markdown("---")

    with st.form("register_form"):
        name = st.text_input("Full name", placeholder="Jane Doe")
        email = st.text_input("Email address", placeholder="you@example.com")
        phone = st.text_input("Phone number (optional)", placeholder="210-555-0000")
        address = st.text_area("Shipping address (optional)", placeholder="123 Main St, San Antonio TX 78201")
        password = st.text_input("Password", type="password", placeholder="At least 6 characters")
        confirm = st.text_input("Confirm password", type="password", placeholder="Repeat password")
        submitted = st.form_submit_button("Create Account", use_container_width=True)

        if submitted:
            if not name or not email or not password or not confirm:
                st.error("Name, email, and password are required.")
            elif not is_valid_email(email):
                st.error("Please enter a valid email address.")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters.")
            elif password != confirm:
                st.error("Passwords do not match.")
            else:
                success, msg = register_user(email, password, name, phone, address)
                if success:
                    st.success(msg + " You can now log in.")
                    st.session_state.auth_page = "login"
                    st.rerun()
                else:
                    st.error(msg)

    st.markdown("---")
    st.markdown("Already have an account?")
    if st.button("Back to login", use_container_width=True):
        st.session_state.auth_page = "login"
        st.rerun()


def _show_profile() -> None:
    user = _current_user()
    email = st.session_state.current_user

    st.markdown(f"## 👤 Hello, {user['name'].split()[0]}!")
    st.markdown(f"*Member since {user['created_at']}  ·  Role: `{user['role']}`*")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["My Information", "Change Password", "Order History"])

    with tab1:
        st.markdown("### Account Details")
        with st.form("profile_form"):
            new_name = st.text_input("Full name", value=user["name"])
            st.text_input("Email address", value=email, disabled=True, help="Email cannot be changed.")
            new_phone = st.text_input("Phone number", value=user["phone"])
            new_address = st.text_area("Shipping address", value=user["address"])
            save = st.form_submit_button("Save Changes", use_container_width=True)

            if save:
                if not new_name:
                    st.error("Name cannot be empty.")
                else:
                    st.session_state.users_db[email]["name"] = new_name
                    st.session_state.users_db[email]["phone"] = new_phone
                    st.session_state.users_db[email]["address"] = new_address
                    st.success("Profile updated successfully!")
                    st.rerun()

    with tab2:
        st.markdown("### Change Password")
        with st.form("password_form"):
            current_pw = st.text_input("Current password", type="password")
            new_pw = st.text_input("New password", type="password", placeholder="At least 6 characters")
            confirm_pw = st.text_input("Confirm new password", type="password")
            change = st.form_submit_button("Update Password", use_container_width=True)

            if change:
                if hash_password(current_pw) != user["password_hash"]:
                    st.error("Current password is incorrect.")
                elif len(new_pw) < 6:
                    st.error("New password must be at least 6 characters.")
                elif new_pw != confirm_pw:
                    st.error("New passwords do not match.")
                else:
                    st.session_state.users_db[email]["password_hash"] = hash_password(new_pw)
                    st.success("Password changed successfully!")

    with tab3:
        st.markdown("### Your Orders")
        mine = [o for o in st.session_state.get("orders", []) if o.get("email") == email]
        if not mine:
            st.info("No orders yet. Place one from the Cart page.")
        else:
            for o in mine:
                with st.container(border=True):
                    st.markdown(f"**{o['order_no']}** — {len(o['items'])} item(s) — **${o['total']:,.2f}**")
                    st.caption(f"Shipped to {o['customer']}")

    st.markdown("---")
    if st.button("🚪 Log Out", use_container_width=True):
        logout()
        st.rerun()


def render() -> None:
    if st.session_state.logged_in:
        _show_profile()
    elif st.session_state.auth_page == "register":
        _show_register()
    else:
        _show_login()
