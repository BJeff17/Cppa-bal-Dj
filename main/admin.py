from django.contrib import admin
from .models import Candidat, Categorie
from .models import CustomUser

# Register your models here.
admin.site.register(Categorie)
admin.site.register(Candidat)

admin.site.register(CustomUser)
