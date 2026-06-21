import pandas as pd

def analyze_data(df):
    summary = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing_values": int(df.isnull().sum().sum()),
        "duplicates": int(df.duplicated().sum()),
        "column_names": list(df.columns)
    }

    return summary