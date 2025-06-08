import streamlit as st

def show_header(title: str, icon: str = None):
    """Display a consistent header with optional emoji/icon."""
    if icon:
        st.title(f"{icon} {title}")
    else:
        st.title(title)
    st.divider()

def input_text(label: str, key: str = None, value: str = "", placeholder: str = "", help_text: str = ""):
    """Reusable text input with optional default value and help."""
    return st.text_input(label, value=value, key=key, placeholder=placeholder, help=help_text)

def input_selectbox(label: str, options: list, key: str = None, index: int = 0, help_text: str = ""):
    """Reusable selectbox dropdown."""
    return st.selectbox(label, options, index=index, key=key, help=help_text)

def button(label: str, key: str = None):
    """Reusable button."""
    return st.button(label, key=key)

def show_success(message: str):
    """Show a green success message."""
    st.success(message)

def show_error(message: str):
    """Show a red error message."""
    st.error(message)

def show_warning(message: str):
    """Show a yellow warning message."""
    st.warning(message)

def confirm_action(message: str, key: str = None):
    """Show a yes/no confirmation checkbox for critical actions."""
    return st.checkbox(message, key=key)

def show_table(data, columns=None):
    """Display a table or dataframe."""
    st.table(data) if columns is None else st.dataframe(data[columns])
