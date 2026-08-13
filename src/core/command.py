from dataclasses import dataclass

@dataclass
class Command:
    intent : str
    entity : str | None = None