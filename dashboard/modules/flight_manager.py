import re
import pandas as pd
import streamlit as st
from sqlalchemy import text
from modules.utils import (
    export_to_excel,
    filter_dataframe,
    log_action,
    get_session
)

st.set_page_config(layout="wide")
session = get_session()

@st.cache_data(show_spinner=False)
def load_full_table(table_name):
    return pd.read_sql(f"SELECT * FROM {table_name}", session.bind)

def get_primary_key_column(session, table_name):
    if not re.match(r'^\w+$', table_name):
        raise ValueError("Invalid table name")

    query = f"""
        SELECT a.attname
        FROM pg_index i
        JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
        WHERE i.indrelid = '{table_name}'::regclass AND i.indisprimary;
    """
    result = session.execute(text(query)).fetchone()
    return result[0] if result else None

def paginate_dataframe(df, page_size):
    total_pages = (len(df) - 1) // page_size + 1
    page_num = st.number_input("Page", 1, total_pages, 1)
    start = (page_num - 1) * page_size
    end = start + page_size
    return df.iloc[start:end], total_pages

def fast_filter(df, search_term):
    search_term = search_term.lower()
    return df[df.astype(str).apply(lambda row: row.str.lower().str.contains(search_term).any(), axis=1)]

def flight_manager_dashboard():
    st.sidebar.title("📋 Flight Manager Menu")

    tables = [  "flights", "flight_schedules","gates"]
    table = st.sidebar.selectbox("Select Table", tables)

    # View & Filter
    df = pd.read_sql(f"SELECT * FROM {table} ", session.bind)
    search = st.text_input("🔍 Search Table")
    if search:
        df = filter_dataframe(df, search)

    st.dataframe(df, use_container_width=True)

    # Export
    if st.download_button("📤 Export to Excel", data=export_to_excel(df),
                          file_name=f"{table}.xlsx", mime="application/vnd.ms-excel"):
        st.success("Downloaded")

    # Create
    st.subheader(f"➕ Add New Record to {table}")
    cols = df.columns.tolist()
    new_data = {col: st.text_input(f"{col}") for col in cols if col != 'id'}

    if st.button("Insert"):
        try:
            columns = ", ".join(new_data.keys())
            values = ", ".join([f"'{v}'" for v in new_data.values()])
            query = text(f"INSERT INTO {table} ({columns}) VALUES ({values}) RETURNING *")
            result = session.execute(query)
            session.commit()
            inserted_id = result.fetchone()[0]
            log_action(session, table, "INSERT", inserted_id, st.session_state.user['admin_id'])
            st.success("✅ Inserted Successfully")
        except Exception as e:
            session.rollback()  # 👈 This is crucial
            st.error(f"❌ Insert failed: {e}")







        # Update
    # Update
    st.subheader("✏️ Update Record")

    # Get primary key column of selected table
    pk_column = get_primary_key_column(session, table)
    if not pk_column:
        st.error(f"❌ No primary key found for table `{table}`.")
    else:
        update_id = st.text_input(f"Enter {pk_column} to update")

        if update_id:
            # Fetch the record using dynamic primary key
            record = session.execute(
                text(f"SELECT * FROM {table} WHERE {pk_column} = :pk"),
                {"pk": update_id}
            ).fetchone()

            if record:
                record_dict = dict(record._mapping)
                updated_data = {}

                st.markdown("### Update Fields")
                for key, value in record_dict.items():
                    if key == pk_column:
                        st.text_input(f"{key}", value, disabled=True)
                    else:
                        updated_data[key] = st.text_input(f"{key}", str(value))

                if st.button("Update"):
                    # Dynamically build update query
                    update_query = text(f"""
                        UPDATE {table} SET
                        {', '.join([f"{col} = :{col}" for col in updated_data])}
                        WHERE {pk_column} = :pk
                    """)
                    updated_data["pk"] = update_id
                    try:
                        session.execute(update_query, updated_data)
                        session.commit()
                        log_action(session, table, "UPDATE", update_id, st.session_state.user['admin_id'])
                        st.success("✅ Record updated successfully!")
                    except Exception as e:
                        st.error(f"❌ Failed to update record: {e}")
            else:
                st.warning(f"No record found with `{pk_column}` = {update_id}.")







