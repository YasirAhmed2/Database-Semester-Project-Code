# utils.py
import pandas as pd
import io

def export_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
    output.seek(0)
    return output

def filter_dataframe(df, query):
    return df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
