from django.shortcuts import render
from django.views import View, generic
from time import sleep
from .service import AgenteIa
from promoter.models import Promoter

MAX_MESSAGES = 20
SYSTEM_PROMPT = """Você é um atendente virtual da Hidrotintas.

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
- Quando tiver os dados, confirme as informações e informe que um promotor de vendas entrará em contato em breve

Formato de resposta (OBRIGATÓRIO):
Responda APENAS com JSON válido. Não inclua nenhum texto fora do JSON.

{
  "reply": "mensagem amigável para o cliente",
  "data": {
    "nome": null,
    "cidade": null,
    "estado": null
    "telefone": null
  }
}

Regras de resposta:
- Responda como uma conversa humana
- Não comece despejando todas as informações da empresa
- Priorize avançar a conversa e coletar os dados necessários
- Faça uma pergunta por vez
- Se o usuário apenas cumprimentar, responda brevemente e já peça o nome

Regras de dados:
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
    # Instancia o serviço com a regra de negócio fixa
    agente = AgenteIa(system_prompt=SYSTEM_PROMPT)

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
            # Pequena pausa para o efeito de "digitando..." ficar perceptível
            sleep(0.9)
            # Atualiza o histórico local com a interação completa
            messages.append({"role": "user", "parts": [{"text": content}]})
            messages.append(
                {"role": "model", "parts": [{"text": response_text["reply"]}]}
            )
            # Trim do histórico para respeitar o limite de mensagens
            if len(messages) > MAX_MESSAGES:
                messages = messages[-MAX_MESSAGES:]
            # Persistência na sessão
            request.session["messages"] = messages
            request.session.modified = True
            promoter = Promoter.objects.filter(
                state__sigla=response_text["data"]["estado"]
            ).first()
            wpp = None
            if promoter:
                msg = f"Olá {promoter.name}, segue o contato para uma visita Interessado: {response_text['data']['nome']} - Numero para contato {response_text['data']['telefone']} - cidade {response_text['data']['cidade']}"
                wpp = f"https://wa.me/{promoter.contact}?text={msg}"
        # Retorno parcial para o HTMX
        return render(
            request, "partials/_messages.html", {"messages": messages, "wpp": wpp}
        )
