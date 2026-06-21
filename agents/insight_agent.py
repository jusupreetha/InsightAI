from utils.gemini_config import model

def generate_insights(summary):

    prompt = f"""
    You are a professional business data analyst.

    Analyze this dataset summary:

    Rows: {summary['rows']}
    Columns: {summary['columns']}
    Missing Values: {summary['missing_values']}
    Duplicates: {summary['duplicates']}
    Columns: {summary['column_names']}

    Generate:
    1. Data Quality Assessment
    2. Key Business Observations
    3. Recommended Analysis Areas

    Keep the response concise and professional.
    """

    response = model.generate_content(prompt)

    return response.text