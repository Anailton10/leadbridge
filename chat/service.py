from openai import OpenAI
from django.conf import settings
import re
import json

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=settings.GROQ_API_KEY,
)


def _blank_data():
    return {
        "name": None,
        "city": None,
        "state": None,
        "contact": None,
        "address": None,
    }


class ServiceAtendentIa:
    def __init__(self, system_prompt: str):
        self.system_prompt = system_prompt

    def send_message(self, historico: list[dict], user_content: str):
        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.system_prompt},  # type: ignore
                    *historico,  # type: ignore
                    {"role": "user", "content": user_content},
                ],
                model="llama-3.3-70b-versatile",
            )
            response_text = response.choices[0].message.content
            match = re.search(r"\{.*\}", response_text, re.DOTALL)
            if not match:
                return {
                    "reply": "Não entendi, pode repetir?",
                    "data": _blank_data(),
                }
            response_text = match.group()
            if not response_text:
                return {
                    "reply": "Erro ao processar sua solicitação.",
                    "data": _blank_data(),
                }
            parsed = json.loads(response_text)  # type: ignore
            data = _blank_data()
            data.update(parsed.get("data") or {})
            return dict(reply=parsed.get("reply", "Tudo bem?"), data=data)
        except Exception as e:
            print(f"Erro na API: {e}")
            return {
                "reply": "Erro ao processar sua solicitação.",
                "data": _blank_data(),
            }
