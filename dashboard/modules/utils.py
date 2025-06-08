# modules/utils.py
import streamlit as st

def set_session_user(user):
    st.session_state['user'] = user

def get_session_user():
    return st.session_state.get('user', None)

def clear_session_user():
    if 'user' in st.session_state:
        del st.session_state['user']
import pandas as pd
import io
from sqlalchemy import text
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://yasir:yasir1234@localhost:6677/AirportFlightManagement"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_session():
    return SessionLocal()

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
def export_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
    output.seek(0)
    return output

def filter_dataframe(df, query):
    return df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
