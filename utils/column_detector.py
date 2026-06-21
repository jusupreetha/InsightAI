def detect_columns(df):

    numeric_cols = []
    categorical_cols = []
    date_cols = []
    id_cols = []

    for col in df.columns:

        col_lower = col.lower()

        # Detect ID-like columns
        if (
            "id" in col_lower
            or "code" in col_lower
            or "postal" in col_lower
        ):
            id_cols.append(col)

        # Numeric
        elif str(df[col].dtype) in [
            "int64",
            "float64",
            "int32",
            "float32"
        ]:
            numeric_cols.append(col)

        # Categorical
        else:
            categorical_cols.append(col)

    return {
        "numeric": numeric_cols,
        "categorical": categorical_cols,
        "date": date_cols,
        "id": id_cols
    }