import os
import gradio as gr
from huggingface_hub import InferenceClient

client = InferenceClient(
    api_key=os.environ.get("HF_TOKEN")
)

def ghost(message, history):
    messages = [
        {
            "role": "system",
            "content": "Tu es GHOST IA GN, une intelligence artificielle généraliste créée par Ibrahim Diallo en Guinée. Tu réponds en français simple, avec précision, politesse et intelligence. Tu aides dans les études, les sciences, la technologie et la vie quotidienne."
        }
    ]

    for user, assistant in history:
        messages.append({"role": "user", "content": user})
        messages.append({"role": "assistant", "content": assistant})

    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="Qwen/Qwen2.5-7B-Instruct",
        messages=messages,
        max_tokens=1000
    )

    return response.choices[0].message.content

app = gr.ChatInterface(
    fn=ghost,
    title="👻 GHOST IA GN",
    description="Ton assistant intelligent créé en Guinée 🇬🇳"
)

app.launch()
