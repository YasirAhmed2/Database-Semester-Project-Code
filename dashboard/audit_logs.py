# audit_log.py
from sqlalchemy import text
from datetime import datetime

def log_action(session, table_name, action, record_id, admin_id):
    session.execute(text("""
        INSERT INTO audit_logs (table_name, action, record_id, admin_id, timestamp)
        VALUES (:table_name, :action, :record_id, :admin_id, :timestamp)
    """), {
        "table_name": table_name,
        "action": action,
        "record_id": record_id,
        "admin_id": admin_id,
        "timestamp": datetime.utcnow()
    })
    session.commit()
