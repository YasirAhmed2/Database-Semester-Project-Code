import streamlit as st
from config.db_config import get_cursor

def security_officer_dashboard(user):
    st.title("🛡️ Security Officer Dashboard")
    st.write(f"Welcome, Officer {user['full_name']}")

    menu = ["View Reports", "Add Report", "Update Report", "Delete Report"]
    choice = st.sidebar.selectbox("Choose Operation", menu)

    if choice == "View Reports":
        view_reports(user)
    elif choice == "Add Report":
        add_report(user)
    elif choice == "Update Report":
        update_report(user)
    elif choice == "Delete Report":
        delete_report(user)

# -------------------------------
# View all security reports
# -------------------------------
def view_reports(user):
    st.subheader("📄 All Security Reports")
    cursor = get_cursor()
    cursor.execute("""
        SELECT report_id, incident_summary, status, created_at 
        FROM security_reports 
        WHERE officer_id = %s ORDER BY created_at DESC
    """, (user['admin_id'],))
    reports = cursor.fetchall()

    if reports:
        for report in reports:
            st.markdown(f"**ID:** {report['report_id']}")
            st.markdown(f"**Summary:** {report['incident_summary']}")
            st.markdown(f"**Status:** {report['status']}")
            st.markdown(f"**Created At:** {report['created_at']}")
            st.markdown("---")
    else:
        st.info("No reports found.")

# -------------------------------
# Add a new report
# -------------------------------
def add_report(user):
    st.subheader("➕ Add New Report")

    summary = st.text_area("Incident Summary")
    status = st.selectbox("Status", ["Pending", "Investigating", "Closed"])

    if st.button("Submit Report"):
        if summary:
            cursor = get_cursor()
            cursor.execute("""
                INSERT INTO security_reports (officer_id, incident_summary, status, created_at)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
            """, (user['user_id'], summary, status))
            st.success("Report added successfully!")
        else:
            st.warning("Summary cannot be empty.")

# -------------------------------
# Update existing report
# -------------------------------
def update_report(user):
    st.subheader("✏️ Update Report")
    cursor = get_cursor()
    cursor.execute("""
        SELECT report_id, incident_summary, status FROM security_reports
        WHERE officer_id = %s ORDER BY created_at DESC
    """, (user['admin_id'],))
    reports = cursor.fetchall()

    if not reports:
        st.info("No reports available to update.")
        return

    report_options = {f"{r['report_id']} - {r['incident_summary']}": r['report_id'] for r in reports}
    selected = st.selectbox("Select Report to Edit", list(report_options.keys()))
    report_id = report_options[selected]

    new_summary = st.text_area("New Summary")
    new_status = st.selectbox("New Status", ["Pending", "Investigating", "Closed"])

    if st.button("Update"):
        cursor.execute("""
            UPDATE security_reports
            SET incident_summary = %s, status = %s
            WHERE report_id = %s AND officer_id = %s
        """, (new_summary, new_status, report_id, user['admin_id']))
        st.success("Report updated successfully.")

# -------------------------------
# Delete a report
# -------------------------------
def delete_report(user):
    st.subheader("🗑️ Delete Report")
    cursor = get_cursor()
    cursor.execute("""
        SELECT report_id, incident_summary FROM security_reports
        WHERE officer_id = %s ORDER BY created_at DESC
    """, (user['admin_id'],))
    reports = cursor.fetchall()

    if not reports:
        st.info("No reports available to delete.")
        return

    report_options = {f"{r['report_id']} - {r['incident_summary']}": r['report_id'] for r in reports}
    selected = st.selectbox("Select Report to Delete", list(report_options.keys()))
    report_id = report_options[selected]

    if st.button("Delete"):
        cursor.execute("""
            DELETE FROM security_reports
            WHERE report_id = %s AND officer_id = %s
        """, (report_id, user['admin_id']))
        st.success("Report deleted successfully.")
