from django.views import generic, View
from django.shortcuts import render

from .models import Lead


# Create your views here.
class LeadsListView(generic.ListView):
    model = Lead
    template_name = "leads_list.html"
    context_object_name = "leads"


class LeadsListPartialView(View):
    def get(self, request):
        leads = Lead.objects.select_related("promoter__state")
        return render(request, "partials/_leads_table.html", {"leads": leads})
