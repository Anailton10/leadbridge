from django.urls import path

from . import views

urlpatterns = [
    path("", views.ChatTemplateView.as_view(), name="chat"),
    path("send/", views.SendMessegesView.as_view(), name="send"),
]
