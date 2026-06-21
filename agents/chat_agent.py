from utils.gemini_config import model

def chat_with_dataset(df, question):

    sample_data = df.head(50).to_string()

    prompt = f"""
    Dataset Sample:

    {sample_data}

    User Question:
    {question}

    Answer based only on the dataset.
    """

    response = model.generate_content(
        prompt
    )

    return response.text