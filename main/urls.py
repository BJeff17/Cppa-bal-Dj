from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name='home' ),
    path("login", log_, name="login"),
    path('logout', log_out, name="logout"),
    path("votes", votes, name='votes'),
    path("categories/<str:categorie>", categorie, name="categorie"),
    path("categories/<str:categorie>/<str:candidat>/", update_votes, name="votes"),
    # --------------admin panel--------------
    path('adminPanel/', admin_panel, name='admin_panel'),
    path('addCategorie/', add_categorie, name='add_categorie'),
    path('addCandidat/', add_candidat, name='add_candidat'),
    path('addUser/', add_user, name='add_user'),
    path('addAdmin/', add_admin, name='add_admin'),
    path('results/', view_results, name='results')
]
