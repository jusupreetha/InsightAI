from utils.gemini_config import model

def understand_dataset(df):

    columns = list(df.columns)

    sample_data = df.head(5).to_string()

    prompt = f"""
    You are an expert data analyst.

    Dataset Columns:
    {columns}

    Sample Data:
    {sample_data}

    Identify:

    1. Dataset Type
    2. Business Domain
    3. Key Metrics
    4. Important Dimensions
    5. Recommended Analyses

    Keep the response concise.
    """

    response = model.generate_content(prompt)

    return response.text