from django.views import generic
from .models import Promoter
from .forms import PromoterForm
from django.urls import reverse_lazy


class PromoterListView(generic.ListView):
    model = Promoter
    template_name = "promoter_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset


class PromoterCreteView(generic.CreateView):
    model = Promoter
    template_name = "promoter_form.html"
    form_class = PromoterForm
    success_url = reverse_lazy("promoter:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "tile": "Novo Promotor",
                "button_text": "Salvar",
                "cancel_url": reverse_lazy("promoter:list"),
            }
        )
        return context


class PromoterUpdateView(generic.UpdateView):
    model = Promoter
    template_name = "promoter_form.html"
    form_class = PromoterForm
    success_url = reverse_lazy("promoter:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "tile": "Editar Produto",
                "button_text": "Atualizar",
                "cancel_url": reverse_lazy("promoter:list"),
            }
        )
        return context


class PromoterDeleteView(generic.DeleteView):
    model = Promoter
    success_url = reverse_lazy("promoter:list")
