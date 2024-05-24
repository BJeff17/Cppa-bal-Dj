from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField
class Categorie(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="Img/", blank= True)
    def __str__(self):
        return self.name
class Candidat(models.Model):
    name = models.CharField(max_length=200)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="Candidats/", blank=True)
    NombreVotes = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    votes = models.JSONField(default=dict, blank=True)