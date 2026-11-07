
import os
import gradio as gr
from huggingface_hub import InferenceClient

# GHOST IA GN 🇬🇳
# Créé par Ibrahim Diallo

HF_TOKEN = os.environ.get("HF_TOKEN")

client = InferenceClient(
    api_key=HF_TOKEN
)

SYSTEM_PROMPT = """
Tu es GHOST IA GN, une intelligence artificielle généraliste
créée par Ibrahim Diallo en Guinée.

Tu aides dans les études, les sciences, les mathématiques,
la technologie, l'informatique, la rédaction et la vie quotidienne.

Tu réponds en français simple, avec précision, politesse
et intelligence.

Tu analyses les questions et fournis des explications claires.
Tu reconnais tes limites et ne fabriques pas de fausses informations.
"""

def ghost(message, history):
    if not HF_TOKEN:
        return "Erreur : le jeton HF_TOKEN n'est pas configuré."

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    for item in history:
        if isinstance(item, dict):
            role = item.get("role")
            content = item.get("content")

            if role in ("user", "assistant") and isinstance(content, str):
                messages.append({
                    "role": role,
                    "content": content
                })

    messages.append({
        "role": "user",
        "content": message
    })

    response = client.chat.completions.create(
        model="Qwen/Qwen2.5-7B-Instruct",
        messages=messages,
        max_tokens=1000
    )

    return response.choices[0].message.content

app = gr.ChatInterface(
    fn=ghost,
    title="👻 GHOST IA GN",
    description="Ton assistant intelligent créé en Guinée 🇬🇳",
    chatbot=gr.Chatbot(type="messages")
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))

    app.launch(
        server_name="0.0.0.0",
        server_port=port
    )
