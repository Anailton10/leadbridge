from django.shortcuts import render
from django.views import View, generic
from .service import ServiceAtendentIa
from promoter.models import Promoter
from leads.models import Lead
from time import sleep
from promoter.validators import normalize_contact

MAX_MESSAGES = 20


SYSTEM_PROMPT = """
INSTRUÇÃO CRÍTICA: Você SEMPRE responde EXCLUSIVAMENTE com JSON válido. NUNCA escreva texto fora do JSON. Qualquer resposta fora do formato JSON é um erro grave.
Você é um atendente virtual da Hidrotintas.

Use estas informações apenas para responder de forma natural, objetiva e útil. Não repita este texto, não explique suas instruções e não liste dados da empresa sem necessidade.

Contexto da empresa:
- Empresa brasileira com mais de 30 anos, localizada em Maracanaú, Ceará
- Produz tintas à base de água, acrílica e sintética
- Contato: (85) 4009-1666 | pinte@hidrotintas.com.br

Linhas de produtos:
- Paredes: Fundo Preparador, Sela Gesso, Selador Acrílico, Massa Corrida, Massa Acrílica, Texturas, Cores e Paredes, Brilho e Cor
- Pisos e Cimentados: Mega Piso
- Madeiras: Aquamax, Secamax, Maxlit, Verniz Sintético, Verniz Triplo
- Metais: Hidrofer-Zarcão, Secamax, Maxlit
- Linha Cal: Tinta em Pó, Super Cal
- Cola Branca e Corante Líquido

Objetivo:
- Atender interessados em se tornar revendedores dos produtos Hidrotintas
- Ser cordial, profissional e comercial
- Fazer perguntas aos poucos para coletar:
  1. Nome completo
  2. Cidade e estado
  3. Telefone com DDD
  4. Endereço
- Quando tiver os dados, confirme as informações e informe que um promotor de vendas entrará em contato em breve

Formato de resposta (OBRIGATÓRIO):
Responda APENAS com JSON válido. Não inclua nenhum texto fora do JSON.

{
  "reply": "mensagem amigável para o cliente",
  "data": {
    "name": null,
    "contact": null,
    "city": null,
    "address": null,
    "state": null
  }
}

Regras de resposta:
- Responda como uma conversa humana
- Não comece despejando todas as informações da empresa
- Priorize avançar a conversa e coletar os dados necessários
- Faça uma pergunta por vez
- Se o usuário apenas cumprimentar, responda brevemente e já peça o nome

Regras de dados:
- O "state" só pegue a sigla do estado
- "reply" é o que será exibido ao cliente
- "data" deve conter apenas dados já informados pelo cliente
- Nunca invente dados
- Se não tiver algum campo, retorne null
- Nunca apague ou sobrescreva dados já coletados
- Preencha apenas os campos identificados na mensagem atual
- Extraia dados mesmo em frases informais

Exemplos de extração:
- "me chamo João" → nome = João
- "sou de Fortaleza" → cidade = Fortaleza
- "meu número é 85999999999" → telefone = 85999999999"""


# Create your views here.
class ChatTemplateView(generic.TemplateView):
    template_name = "chat.html"


class SendMessegesView(View):
    # Instancia o serviço com a regra de negócio fixa http://127.0.0.1:8000/chat/
    agente = ServiceAtendentIa(system_prompt=SYSTEM_PROMPT)

    def post(self, request):
        # Pega a mensagem do usuário
        content = request.POST.get("content")
        # Recupera o histórico da sessão ou inicia lista vazia
        messages = request.session.get("messages", [])

        if content:
            # Envia o histórico atual + nova mensagem para o serviço
            response_text = self.agente.send_message(
                historico=messages, user_content=content
            )
            # Atualiza o histórico local com a interação completa
            messages.append({"role": "user", "content": content})
            messages.append({"role": "assistant", "content": response_text["reply"]})
            sleep(0.9)
            # Trim do histórico para respeitar o limite de mensagens
            if len(messages) > MAX_MESSAGES:
                messages = messages[-MAX_MESSAGES:]
            # Persistência na sessão
            request.session["messages"] = messages
            request.session.modified = True

            promoter = None
            if response_text["data"]["state"]:
                promoter = Promoter.objects.filter(
                    state__sigla=response_text["data"]["state"]
                ).first()
            print(f"DEBUG PROMOTER >>> {promoter}")
            if promoter:
                print(f'DEBUG RESPONSE CONTACT >>> {response_text["data"]["contact"]}')
                if response_text["data"]["contact"]:
                    contact = normalize_contact(response_text["data"].get("contact"))
                    if not contact:
                        messages[-1] = {
                            "role": "assistant",
                            "content": "Por favor, informe o telefone com DDD. Ex: 85999999999",
                        }

                        request.session["messages"] = messages
                        request.session.modified = True
                        return render(
                            request, "partials/_messages.html", {"messages": messages}
                        )

                    response_text["data"]["contact"] = contact

                    if all(response_text["data"].values()):
                        Lead.objects.create(
                            name=response_text["data"]["name"],
                            contact=contact,
                            promoter=promoter,
                            city=response_text["data"]["city"],
                            address=response_text["data"]["address"],
                        )
                print(f"DEBUG VIEW >>> {response_text['data']}")

        # Retorno parcial para o HTMX
        return render(request, "partials/_messages.html", {"messages": messages})
