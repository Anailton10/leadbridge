from google import genai
from google.genai import types
from django.conf import settings
import json

client = genai.Client(api_key=settings.GEMINI_API_KEY)


class AgenteIa:
    def __init__(self, system_prompt: str):
        self.config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.7,
        )

    def send_message(self, historico: list, user_content: str):
        try:
            chat_history = []
            for m in historico:
                # Extrai o texto de forma segura
                msg_text = m.get("parts", [{}])[0].get("text", "")

                # CORREÇÃO: Usa o construtor Part(text=...) em vez de from_text()
                chat_history.append(
                    types.Content(
                        role=m.get("role"),
                        parts=[types.Part(text=msg_text)],  # Uso de keyword argument
                    )
                )

            chat = client.chats.create(
                model="gemini-2.5-flash",
                config=self.config,
                history=chat_history,
            )

            # O método send_message aceita a string direta para o turno atual
            response = chat.send_message(user_content)
            parsed = json.loads(response.text)  # type: ignore
            return dict(reply=parsed["reply"], data=parsed["data"])
        except Exception as e:
            print(f"Erro na API Gemini: {e}")
            return {
                "reply": "Erro ao processar sua solicitação.",
                "data": {
                    "name": None,
                    "city": None,
                    "state": None,
                    "contact": None,
                    "address": None,
                },
            }
