from django.urls import path
from . import views

app_name = "promoter"
urlpatterns = [
    path("list/", views.PromoterListView.as_view(), name="list"),
    path("create/", views.PromoterCreteView.as_view(), name="create"),
    path("<int:pk>/update/", views.PromoterUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.PromoterDeleteView.as_view(), name="delete"),
]
