from django import forms
from .models import Promoter


class PromoterForm(forms.ModelForm):
    class Meta:
        model = Promoter
        fields = ["name", "last_name", "state", "contact"]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full bg-gray-700 border-none rounded-lg px-3 py-2 focus:ring-0",
                    "placeholder": "Nome",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "w-full bg-gray-700 border-none rounded-lg px-3 py-2 focus:ring-0",
                    "placeholder": "Sobrenome",
                }
            ),
            "state": forms.Select(
                attrs={
                    "class": "w-full bg-gray-700 border-none rounded-lg px-3 py-2 focus:ring-0"
                }
            ),
            "contact": forms.TextInput(
                attrs={
                    "class": "w-full bg-gray-700 border-none rounded-lg px-3 py-2 focus:ring-0",
                    "placeholder": "(xx) xxxxx-xxxx",
                }
            ),
        }

    def clean_contact(self):
        contact = self.cleaned_data.get("contact")

        # exemplo simples (ajusta conforme seu validate_phone)
        if contact and len(contact) < 10:
            raise forms.ValidationError("Telefone inválido")

        return contact
