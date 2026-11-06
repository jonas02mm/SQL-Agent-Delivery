import os
from google import genai

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Chave da API não encontrada.")

client = genai.Client(api_key=api_key)

interaction = client.interactions.create(
    model="gemini-3.5-flash-lite",
    input="Explique em português, de forma simples, o que é SQL."
)

print("\nResposta do Gemini:\n")
print(interaction.output_text)