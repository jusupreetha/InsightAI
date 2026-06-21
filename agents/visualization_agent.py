from utils.gemini_config import model
def plan_visualizations(df):

    columns = list(df.columns)

    sample = df.head(5).to_string()

    prompt = f"""
    You are a senior data analyst.

    Dataset columns:
    {columns}

    Sample data:
    {sample}

    Suggest:
    1. Best visualizations
    2. Why each visualization is useful
    3. Which columns should be used

    Return in bullet points.
    """

    response = model.generate_content(prompt)

    return response.text