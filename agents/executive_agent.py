from utils.gemini_config import model

def generate_executive_summary(df):

    sample_data = df.head(20).to_string()

    prompt = f"""
    You are a senior business analyst.

    Dataset Sample:
    {sample_data}

    Generate:
    1. Dataset type
    2. What the dataset appears to contain
    3. Data quality assessment
    4. Recommended analysis areas

    Keep it concise and professional.
    """

    response = model.generate_content(prompt)

    return response.text