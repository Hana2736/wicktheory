import streamlit as st
import hashlib
import re
from datetime import datetime

# ─────────────────────────────────────────────
# DUMMY DATABASE (replace with MySQL later)
# Each user: { email: { password_hash, name, phone, address, role, created_at } }
# ─────────────────────────────────────────────
if "users_db" not in st.session_state:
    st.session_state.users_db = {
        "admin@wicktheory.com": {
            "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
            "name": "Admin User",
            "phone": "210-000-0000",
            "address": "123 Admin St, San Antonio TX",
            "role": "admin",
            "created_at": "2026-01-01"
        },
        "test@gmail.com": {
            "password_hash": hashlib.sha256("password".encode()).hexdigest(),
            "name": "Test Customer",
            "phone": "210-555-1234",
            "address": "456 Main Ave, San Antonio TX",
            "role": "customer",
            "created_at": "2026-02-01"
        }
    }

# Session defaults
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "page" not in st.session_state:
    st.session_state.page = "login"

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def login_user(email, password):
    db = st.session_state.users_db
    if email in db and db[email]["password_hash"] == hash_password(password):
        st.session_state.logged_in = True
        st.session_state.current_user = email
        return True
    return False

def register_user(email, password, name, phone, address):
    if email in st.session_state.users_db:
        return False, "An account with this email already exists."
    st.session_state.users_db[email] = {
        "password_hash": hash_password(password),
        "name": name,
        "phone": phone,
        "address": address,
        "role": "customer",
        "created_at": datetime.now().strftime("%Y-%m-%d")
    }
    return True, "Account created successfully!"

def logout():
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.page = "login"

def get_user():
    return st.session_state.users_db[st.session_state.current_user]

# ─────────────────────────────────────────────
# PAGE: LOGIN
# ─────────────────────────────────────────────
def show_login():
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
                st.success(f"Welcome back, {get_user()['name']}!")
                st.session_state.page = "profile"
                st.rerun()
            else:
                st.error("Incorrect email or password. Please try again.")

    st.markdown("---")
    st.markdown("Don't have an account?")
    if st.button("Create an account", use_container_width=True):
        st.session_state.page = "register"
        st.rerun()

    # Dev helper - remove before final submission
    with st.expander("🧪 Test Credentials (dev only)"):
        st.code("Customer:  test@gmail.com  /  password\nAdmin:     admin@wicktheory.com  /  admin123")

# ─────────────────────────────────────────────
# PAGE: REGISTER
# ─────────────────────────────────────────────
def show_register():
    st.markdown("## 🕯️ Wick Theory")
    st.markdown("### Create your account")
    st.markdown("---")

    with st.form("register_form"):
        name     = st.text_input("Full name", placeholder="Jane Doe")
        email    = st.text_input("Email address", placeholder="you@example.com")
        phone    = st.text_input("Phone number (optional)", placeholder="210-555-0000")
        address  = st.text_area("Shipping address (optional)", placeholder="123 Main St, San Antonio TX 78201")
        password = st.text_input("Password", type="password", placeholder="At least 6 characters")
        confirm  = st.text_input("Confirm password", type="password", placeholder="Repeat password")
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
                    st.session_state.page = "login"
                    st.rerun()
                else:
                    st.error(msg)

    st.markdown("---")
    st.markdown("Already have an account?")
    if st.button("Back to login", use_container_width=True):
        st.session_state.page = "login"
        st.rerun()

# ─────────────────────────────────────────────
# PAGE: PROFILE / ACCOUNT
# ─────────────────────────────────────────────
def show_profile():
    user = get_user()
    email = st.session_state.current_user

    st.markdown(f"## 👤 Hello, {user['name'].split()[0]}!")
    st.markdown(f"*Member since {user['created_at']}  ·  Role: `{user['role']}`*")
    st.markdown("---")

    tab1, tab2 = st.tabs(["My Information", "Change Password"])

    # ── Tab 1: Edit profile info ──
    with tab1:
        st.markdown("### Account Details")
        with st.form("profile_form"):
            new_name    = st.text_input("Full name", value=user["name"])
            st.text_input("Email address", value=email, disabled=True, help="Email cannot be changed.")
            new_phone   = st.text_input("Phone number", value=user["phone"])
            new_address = st.text_area("Shipping address", value=user["address"])
            save = st.form_submit_button("Save Changes", use_container_width=True)

            if save:
                if not new_name:
                    st.error("Name cannot be empty.")
                else:
                    st.session_state.users_db[email]["name"]    = new_name
                    st.session_state.users_db[email]["phone"]   = new_phone
                    st.session_state.users_db[email]["address"] = new_address
                    st.success("Profile updated successfully!")
                    st.rerun()

    # ── Tab 2: Change password ──
    with tab2:
        st.markdown("### Change Password")
        with st.form("password_form"):
            current_pw  = st.text_input("Current password", type="password")
            new_pw      = st.text_input("New password", type="password", placeholder="At least 6 characters")
            confirm_pw  = st.text_input("Confirm new password", type="password")
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

    st.markdown("---")
    if st.button("🚪 Log Out", use_container_width=True):
        logout()
        st.rerun()

# ─────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────
st.set_page_config(page_title="Wick Theory — Auth", page_icon="🕯️", layout="centered")

if st.session_state.logged_in:
    show_profile()
else:
    if st.session_state.page == "register":
        show_register()
    else:
        show_login()
