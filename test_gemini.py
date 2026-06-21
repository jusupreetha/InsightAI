from utils.gemini_config import model
response = model.generate_content("Say Hello InsightAI")

print(response.text)