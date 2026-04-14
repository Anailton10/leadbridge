from django.views import generic, View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Lead


# Create your views here.
class LeadsListView(LoginRequiredMixin, generic.ListView):
    model = Lead
    template_name = "leads_list.html"
    context_object_name = "leads"


class LeadsListPartialView(LoginRequiredMixin, View):
    def get(self, request):
        leads = Lead.objects.select_related("promoter__state")
        return render(request, "partials/_leads_table.html", {"leads": leads})
