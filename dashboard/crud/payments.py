import streamlit as st
from config.db_config import get_db_connection

# ------------------------------
# CRUD functions for payments table
# ------------------------------

def fetch_payments():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.payment_id, b.booking_id, pm.method_name, p.amount, p.payment_status, p.payment_date
        FROM payments p
        JOIN bookings b ON p.booking_id = b.booking_id
        JOIN payment_methods pm ON p.method_id = pm.method_id
        ORDER BY p.payment_date DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def fetch_bookings():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT booking_id FROM bookings ORDER BY booking_id")
    bookings = cur.fetchall()
    conn.close()
    return bookings

def fetch_payment_methods():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT method_id, method_name FROM payment_methods ORDER BY method_name")
    methods = cur.fetchall()
    conn.close()
    return methods

def add_payment(booking_id, amount, method_id, payment_status):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO payments (booking_id, amount, method_id, payment_status)
            VALUES (%s, %s, %s, %s)
        """, (booking_id, amount, method_id, payment_status))
        conn.commit()
        st.success("✅ Payment added successfully.")
    except Exception as e:
        st.error(f"Error adding payment: {e}")
    finally:
        conn.close()

def update_payment(payment_id, booking_id, amount, method_id, payment_status):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE payments
            SET booking_id = %s,
                amount = %s,
                method_id = %s,
                payment_status = %s
            WHERE payment_id = %s
        """, (booking_id, amount, method_id, payment_status, payment_id))
        conn.commit()
        st.success("✏️ Payment updated successfully.")
    except Exception as e:
        st.error(f"Error updating payment: {e}")
    finally:
        conn.close()

def delete_payment(payment_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM payments WHERE payment_id = %s", (payment_id,))
        conn.commit()
        st.success("🗑️ Payment deleted successfully.")
    except Exception as e:
        st.error(f"Error deleting payment: {e}")
    finally:
        conn.close()

# ------------------------------
# Streamlit UI for payments
# ------------------------------

def show_payments_dashboard():
    st.title("💳 Payments Management")

    # List payments
    st.subheader("📋 Existing Payments")
    payments = fetch_payments()
    if payments:
        st.table(payments)
    else:
        st.info("No payments found.")

    st.divider()

    # Prepare dropdown data
    bookings = fetch_bookings()
    booking_ids = [str(b[0]) for b in bookings]
    payment_methods = fetch_payment_methods()
    method_names = [m[1] for m in payment_methods]
    method_dict = {m[1]: m[0] for m in payment_methods}

    # Add payment
    st.subheader("➕ Add Payment")
    booking_id = st.selectbox("Select Booking ID", booking_ids)
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    method_name = st.selectbox("Payment Method", method_names)
    payment_status = st.text_input("Payment Status", value="Completed")

    if st.button("Add Payment"):
        if booking_id and amount > 0 and payment_status.strip():
            add_payment(booking_id, amount, method_dict[method_name], payment_status.strip())
        else:
            st.warning("Please fill all fields with valid values.")

    st.divider()

    # Update payment
    st.subheader("✏️ Update Payment")
    payment_id = st.text_input("Payment ID to Update")
    if payment_id:
        booking_id_upd = st.selectbox("Booking ID", booking_ids, key="upd_booking")
        amount_upd = st.number_input("Amount", min_value=0.0, format="%.2f", key="upd_amount")
        method_name_upd = st.selectbox("Payment Method", method_names, key="upd_method")
        payment_status_upd = st.text_input("Payment Status", value="Completed", key="upd_status")

        if st.button("Update Payment"):
            if booking_id_upd and amount_upd > 0 and payment_status_upd.strip():
                update_payment(payment_id, booking_id_upd, amount_upd, method_dict[method_name_upd], payment_status_upd.strip())
            else:
                st.warning("Please fill all fields with valid values.")

    st.divider()

    # Delete payment
    st.subheader("❌ Delete Payment")
    delete_id = st.text_input("Payment ID to Delete", key="delete_payment_id")
    if st.button("Delete Payment"):
        if delete_id:
            delete_payment(delete_id)
        else:
            st.warning("Please enter a Payment ID to delete.")
