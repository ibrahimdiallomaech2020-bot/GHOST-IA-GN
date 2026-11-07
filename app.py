import os
import traceback
import gradio as gr
from huggingface_hub import InferenceClient

HF_TOKEN = os.environ.get("HF_TOKEN")
MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"

SYSTEM_PROMPT = """
Tu es GHOST IA GN, une intelligence artificielle généraliste
créée par Ibrahim Diallo en Guinée.

Tu aides dans les études, les sciences, les mathématiques,
la technologie, l'informatique, la rédaction et la vie quotidienne.

Tu réponds en français simple, avec précision et intelligence.
Tu expliques clairement et tu ne fabriques pas de fausses informations.
"""

def extract_text(content):
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text":
                    parts.append(block.get("text", ""))
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(parts)

    return ""

def ghost(message, history):
    if not HF_TOKEN:
        return "Erreur : le jeton HF_TOKEN est absent."

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    for item in history or []:
        if isinstance(item, dict):
            role = item.get("role")
            content = extract_text(item.get("content"))

            if role in ["user", "assistant"] and content:
                messages.append({
                    "role": role,
                    "content": content
                })

    messages.append({
        "role": "user",
        "content": message
    })

    try:
        client = InferenceClient(api_key=HF_TOKEN)

        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=messages,
            max_tokens=1000
        )

        return response.choices[0].message.content or "Je n'ai pas pu générer de réponse."

    except Exception as error:
        print("ERREUR GHOST IA :", repr(error))
        traceback.print_exc()
        return "GHOST IA rencontre un problème technique. Réessaie dans quelques instants."

app = gr.ChatInterface(
    fn=ghost,
    title="👻 GHOST IA GN",
    description="Ton assistant intelligent créé en Guinée 🇬🇳"
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.launch(
        server_name="0.0.0.0",
        server_port=port
    )
