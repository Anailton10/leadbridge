from django.db import models
from core.models.base import BaseModel
from promoter.validators import validate_phone
from promoter.models import Promoter
from .utils import WhatsAppService


# Create your models here.
class Lead(BaseModel):
    name = models.CharField(max_length=70)
    contact = models.CharField(max_length=13, validators=[validate_phone])
    promoter = models.ForeignKey(Promoter, on_delete=models.PROTECT)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=100)

    @property
    def whatsapp_link(self):
        return WhatsAppService.build_link(self)

    def __str__(self):
        return f"({self.name} - {self.city})"
