from django.db import models

from core.models.base import BaseModel

from .validators import validate_phone


class State(BaseModel):
    name = models.CharField(max_length=20, unique=True)
    sigla = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.name


class Promoter(BaseModel):
    name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    state = models.ForeignKey(State, on_delete=models.PROTECT)
    contact = models.CharField(max_length=13, validators=[validate_phone])

    def __str__(self):
        return f"{self.name} {self.last_name}"
