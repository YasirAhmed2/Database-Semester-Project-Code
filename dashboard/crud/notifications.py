import streamlit as st
from config.db_config import get_db_connection

# ------------------------------
# CRUD functions for notifications table
# ------------------------------

def fetch_notifications():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT n.notification_id, p.full_name, n.message, n.sent_at
        FROM notifications n
        JOIN passengers p ON n.passenger_id = p.passenger_id
        ORDER BY n.sent_at DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def fetch_passengers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT passenger_id, full_name FROM passengers ORDER BY full_name")
    passengers = cur.fetchall()
    conn.close()
    return passengers

def add_notification(passenger_id, message):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO notifications (passenger_id, message)
            VALUES (%s, %s)
        """, (passenger_id, message))
        conn.commit()
        st.success("✅ Notification added successfully.")
    except Exception as e:
        st.error(f"Error adding notification: {e}")
    finally:
        conn.close()

def update_notification(notification_id, passenger_id, message):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE notifications
            SET passenger_id = %s, message = %s
            WHERE notification_id = %s
        """, (passenger_id, message, notification_id))
        conn.commit()
        st.success("✏️ Notification updated successfully.")
    except Exception as e:
        st.error(f"Error updating notification: {e}")
    finally:
        conn.close()

def delete_notification(notification_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM notifications WHERE notification_id = %s", (notification_id,))
        conn.commit()
        st.success("🗑️ Notification deleted successfully.")
    except Exception as e:
        st.error(f"Error deleting notification: {e}")
    finally:
        conn.close()

# ------------------------------
# Streamlit UI for notifications
# ------------------------------

def show_notifications_dashboard():
    st.title("🔔 Notifications Management")

    # List notifications
    st.subheader("📋 Existing Notifications")
    notifications = fetch_notifications()
    if notifications:
        st.table(notifications)
    else:
        st.info("No notifications found.")

    st.divider()

    # Passenger dropdown
    passengers = fetch_passengers()
    passenger_display = [p[1] for p in passengers]
    passenger_dict = {p[1]: p[0] for p in passengers}

    # Add notification
    st.subheader("➕ Add Notification")
    passenger_sel = st.selectbox("Select Passenger", passenger_display)
    message = st.text_area("Message")

    if st.button("Add Notification"):
        if message.strip():
            add_notification(passenger_dict[passenger_sel], message.strip())
        else:
            st.warning("Please enter a notification message.")

    st.divider()

    # Update notification
    st.subheader("✏️ Update Notification")
    notification_id = st.text_input("Notification ID to Update")
    if notification_id:
        passenger_upd = st.selectbox("New Passenger", passenger_display, key="upd_passenger")
        message_upd = st.text_area("New Message", key="upd_message")

        if st.button("Update Notification"):
            if message_upd.strip():
                update_notification(notification_id, passenger_dict[passenger_upd], message_upd.strip())
            else:
                st.warning("Please enter a new notification message.")

    st.divider()

    # Delete notification
    st.subheader("❌ Delete Notification")
    delete_id = st.text_input("Notification ID to Delete", key="delete_notification_id")
    if st.button("Delete Notification"):
        if delete_id:
            delete_notification(delete_id)
        else:
            st.warning("Please enter a Notification ID to delete.")
