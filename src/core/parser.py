import json

from core.command import Command

def parse_llm_response(response: str) -> Command:
    data  = json.loads(response)

    return Command(
        intent= data['intent'],
        entity= data.get('entity')
    )