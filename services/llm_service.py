import os
import ollama
from groq import Groq


def build_prompt(question, context):
    prompt = f"""
You are an Enterprise Knowledge Assistant.

Answer ONLY using the provided context.

If the answer is not present in the context,
reply:

"I don't have enough information to answer this."

Context:
{context}

Question:
{question}

Answer:
"""
    return prompt


def ask_question_to_ollama(prompt):
    response = ollama.chat(
        model="llama3.1",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


def ask_question_to_groq(prompt, message_history):
    client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )

    messages = []

    for message in message_history:
        messages.append({
            "role": "user" if message["message_by"] == "user" else "assistant",
            "content": message["message"]
        })

    messages.append({
        "role": "user",
        "content": prompt
    })

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    return response.choices[0].message.content