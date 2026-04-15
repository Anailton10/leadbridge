from django.urls import path
from . import views

app_name = "leads"
urlpatterns = [
    path("", views.LeadsListView.as_view(), name="list"),
    path("list/partial/", views.LeadsListPartialView.as_view(), name="list_partial"),
]
