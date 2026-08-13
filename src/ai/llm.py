from ollama import chat

def ask_vama(prompt):

    response = chat(
        model="qwen3:8b",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    return response['message']['content']