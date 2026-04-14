"""Admin panel for Wick Theory.

Only shown in the sidebar when the signed-in user has role=admin.
Every action mutates session state — users, orders, settings, products.
"""

import csv
import io

import streamlit as st

from auth import hash_password, register_user
from cart import DEFAULT_SETTINGS
from data import SIZE_LABELS, money


# ---------- Manage Users ----------

def _render_users() -> None:
    with st.expander("Manage Users", expanded=False):
        c1, c2, c3 = st.columns([3, 1, 1])
        if c2.button("Add User", key="users_add_btn"):
            st.session_state.show_add_user = not st.session_state.get("show_add_user", False)

        # CSV export
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["email", "name", "phone", "address", "role", "created_at"])
        for email, u in st.session_state.users_db.items():
            writer.writerow([email, u["name"], u["phone"], u["address"], u["role"], u["created_at"]])
        c3.download_button(
            "Export CSV",
            data=buf.getvalue(),
            file_name="wicktheory_users.csv",
            mime="text/csv",
            key="users_export",
        )

        if st.session_state.get("show_add_user"):
            with st.form("add_user_form", clear_on_submit=True):
                st.markdown("**Add a new user**")
                name = st.text_input("Name")
                email = st.text_input("Email")
                phone = st.text_input("Phone")
                address = st.text_input("Address")
                role = st.selectbox("Role", ["customer", "admin"])
                pw = st.text_input("Initial password", type="password")
                submitted = st.form_submit_button("Create user")
                if submitted:
                    if not (name and email and pw):
                        st.error("Name, email, and password are required.")
                    else:
                        ok, msg = register_user(email, pw, name, phone, address, role=role)
                        if ok:
                            st.success(f"Created {email}.")
                            st.session_state.show_add_user = False
                            st.rerun()
                        else:
                            st.error(msg)

        st.divider()

        for email, u in list(st.session_state.users_db.items()):
            col1, col2, col3, col4, col5 = st.columns([2, 3, 2, 2, 1])
            col1.write(f"**{u['name']}**")
            col2.write(email)
            col3.write(u.get("phone", ""))
            new_role = col4.selectbox(
                "Role",
                ["customer", "admin"],
                index=0 if u["role"] == "customer" else 1,
                key=f"role_{email}",
                label_visibility="collapsed",
            )
            if new_role != u["role"]:
                st.session_state.users_db[email]["role"] = new_role
                st.toast(f"{email} role updated to {new_role}.")
            if col5.button("Delete", key=f"del_user_{email}"):
                if email == st.session_state.current_user:
                    st.error("You can't delete the account you're signed in as.")
                else:
                    del st.session_state.users_db[email]
                    st.rerun()


# ---------- Recent Orders ----------

def _render_orders() -> None:
    with st.expander("Recent Orders", expanded=False):
        c1, c2, c3 = st.columns([3, 1, 1])
        if c2.button("Review Orders", key="orders_review"):
            st.session_state.show_order_details = not st.session_state.get("show_order_details", False)
        if c3.button("Refund Selected", key="orders_refund"):
            refunded_count = 0
            for o in st.session_state.orders:
                if st.session_state.get(f"refund_select_{o['order_no']}") and o.get("status") != "refunded":
                    o["status"] = "refunded"
                    refunded_count += 1
            if refunded_count:
                st.success(f"Refunded {refunded_count} order(s).")
                st.rerun()
            else:
                st.warning("No orders selected.")

        st.divider()
        orders = st.session_state.get("orders", [])
        if not orders:
            st.info("No orders placed yet this session. Go to Shop then Cart to place one.")
            return

        show_details = st.session_state.get("show_order_details", False)
        for o in orders:
            cols = st.columns([0.5, 2, 3, 2, 1.5])
            cols[0].checkbox(" ", key=f"refund_select_{o['order_no']}", label_visibility="collapsed")
            cols[1].write(f"`{o['order_no']}`")
            cols[2].write(f"{o['customer']} — {len(o['items'])} item(s)")
            cols[3].write(money(o["total"]))
            status = o.get("status", "paid")
            badge = "REFUNDED" if status == "refunded" else "PAID"
            cols[4].write(f"`{badge}`")
            if show_details:
                with st.container(border=True):
                    st.caption(f"{o['email']}  ·  subtotal {money(o['subtotal'])}  ·  tax {money(o['tax'])}  ·  shipping {money(o['shipping'])}")
                    for pid, qty in o["items"].items():
                        st.write(f"- {pid} × {qty}")


# ---------- System Settings ----------

def _render_settings() -> None:
    with st.expander("System Settings", expanded=False):
        s = st.session_state.settings
        new_maint = st.toggle("Down for Maintenance", value=s["maintenance"], key="sys_maint")
        new_signups = st.toggle("Allow New Signups", value=s["allow_signups"], key="sys_signups")
        new_coupons = st.toggle("Allow Coupon Codes", value=s["allow_coupons"], key="sys_coupons")
        st.divider()
        c1, c2 = st.columns(2)
        if c1.button("Save Settings", key="settings_save"):
            st.session_state.settings = {
                "maintenance": new_maint,
                "allow_signups": new_signups,
                "allow_coupons": new_coupons,
            }
            st.success("Settings saved.")
        if c2.button("Reset to Defaults", key="settings_reset"):
            st.session_state.settings = dict(DEFAULT_SETTINGS)
            st.rerun()


# ---------- Items ----------

def _render_items() -> None:
    with st.expander("Items", expanded=False):
        c1, c2, c3 = st.columns([3, 1, 1])
        if c2.button("Add Item", key="items_add_btn"):
            st.session_state.show_add_item = not st.session_state.get("show_add_item", False)
        if c3.button("Edit Items", key="items_edit_btn"):
            st.session_state.items_edit_mode = not st.session_state.get("items_edit_mode", False)

        if st.session_state.get("show_add_item"):
            with st.form("add_item_form", clear_on_submit=True):
                st.markdown("**Add a new candle**")
                name = st.text_input("Name")
                size = st.selectbox("Size", ["L", "M", "S"], format_func=lambda s: SIZE_LABELS[s])
                scent = st.selectbox("Scent", ["citrus", "floral", "fruity", "earthy", "gourmet"])
                price = st.number_input("Price", min_value=0.0, value=19.99, step=0.50)
                stock = st.number_input("Stock", min_value=0, value=10, step=1)
                description = st.text_area("Description")
                submitted = st.form_submit_button("Create item")
                if submitted:
                    if not name:
                        st.error("Name is required.")
                    else:
                        new_id = name.lower().replace(" ", "") + f"_{size}_{len(st.session_state.products)}"
                        st.session_state.products.append({
                            "id": new_id,
                            "name": name,
                            "scent": scent,
                            "size": size,
                            "price": float(price),
                            "stock": int(stock),
                            "description": description,
                            "image": "",
                        })
                        st.success(f"Added {name}.")
                        st.session_state.show_add_item = False
                        st.rerun()

        st.divider()
        st.caption(f"{len(st.session_state.products)} candles in catalog")
        edit_mode = st.session_state.get("items_edit_mode", False)
        for i, p in enumerate(list(st.session_state.products)):
            if edit_mode:
                with st.container(border=True):
                    cols = st.columns([3, 1, 1, 1, 1])
                    new_name = cols[0].text_input("name", value=p["name"], key=f"name_{p['id']}", label_visibility="collapsed")
                    new_price = cols[1].number_input("price", value=float(p["price"]), step=0.50, key=f"price_{p['id']}", label_visibility="collapsed")
                    new_stock = cols[2].number_input("stock", value=int(p["stock"]), step=1, key=f"stock_{p['id']}", label_visibility="collapsed")
                    if cols[3].button("Save", key=f"save_{p['id']}"):
                        p["name"] = new_name
                        p["price"] = float(new_price)
                        p["stock"] = int(new_stock)
                        st.toast(f"Saved {new_name}.")
                    if cols[4].button("Delete", key=f"delete_{p['id']}"):
                        st.session_state.products = [x for x in st.session_state.products if x["id"] != p["id"]]
                        st.rerun()
            else:
                col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                col1.write(f"**{p['name']}**")
                col2.write(SIZE_LABELS.get(p["size"], p["size"]))
                col3.write(money(p["price"]))
                col4.write(f"Stock: {p['stock']}")


def render() -> None:
    st.title("Admin Panel")
    st.caption("Wick Theory")
    _render_users()
    _render_orders()
    _render_settings()
    _render_items()
