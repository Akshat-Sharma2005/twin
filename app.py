
from openai import OpenAI
from context import TWIN_SYSTEM_PROMPT
from tools import tools, handle_tool_calls
from styles import CSS, JS, EXAMPLES
from dotenv import load_dotenv
import gradio as gr
import os

load_dotenv(override=True)

groq_api_key = os.getenv('GROQ_API_KEY')

if groq_api_key:
    print(f"GROQ API Key exists and begins {groq_api_key[:4]}")
else:
    print("GROQ API Key not set")

MODEL_NAME = "openai/gpt-oss-120b"

groq = OpenAI(
    api_key=groq_api_key,
    base_url="https://api.groq.com/openai/v1",
)

system = [{"role": "system", "content": TWIN_SYSTEM_PROMPT}]


def chat(message, history):
    history = [{"role": h["role"], "content": h["content"]} for h in history]
    messages = system + history + [{"role": "user", "content": message}]
    response = groq.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)
    while response.choices[0].finish_reason == "tool_calls":
        reply_message = response.choices[0].message
        tool_calls = reply_message.tool_calls
        results = handle_tool_calls(tool_calls)
        messages.append(reply_message)
        messages.extend(results)
        response = groq.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)
    return response.choices[0].message.content

if __name__ == "__main__":
    gr.ChatInterface(
        chat,
        examples=EXAMPLES,
        title="Digital Twin",
        description="Talk to my AI twin about my career",
        chatbot=gr.Chatbot(show_label=False),
    ).launch(
        css=CSS,
        js=JS,
        theme=gr.themes.Base(),
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860)),
    )