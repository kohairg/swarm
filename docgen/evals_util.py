from dataclasses import dataclass
from openai import OpenAI

@dataclass
class BoolEvalResult:
    value: bool

def evaluate_with_llm_bool(system_prompt: str, user_prompt: str) -> BoolEvalResult:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    result = response.choices[0].message.content.strip().lower() == "true"
    return BoolEvalResult(value=result) 