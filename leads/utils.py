from urllib.parse import quote


# -*- coding: utf-8 -*-
class WhatsAppService:

    @staticmethod
    def format_phone(phone: str) -> str:
        digits = "".join(filter(str.isdigit, phone))

        if len(digits) == 11:
            return f"{digits[2:4]}{digits[4:9]}{digits[9:]}"

        return phone

    @classmethod
    def build_message(cls, lead):
        telefone = cls.format_phone(lead.contact)

        mensagem = (
            f"Olá {lead.promoter.name}, tudo bem?\n\n"
            f"Novo lead:\n\n"
            f"👤 {lead.name}\n"
            f"📍 {lead.city}\n"
            f"🏠 {lead.address}\n"
            f"📞 {telefone}"
        )

        return quote(mensagem.strip(), safe="")

    @classmethod
    def build_link(cls, lead):
        msg = cls.build_message(lead)
        numero = "".join(filter(str.isdigit, lead.promoter.contact))

        return f"https://api.whatsapp.com/send?phone={numero}&text={msg}&type=phone_number&app_absent=0"
