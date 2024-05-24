from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
import re
import json
from django.http import HttpResponseForbidden
from functools import wraps
from .models import Candidat, Categorie, CustomUser
def verify_super_user(user):
    return user.is_authenticated and user.is_staff

@login_required(login_url="/login")
def home(request):
    
    return render(request, "home.html",{'isadmin':request.user.is_staff})
@login_required(login_url="/login")
def votes(request):
    
    categorie = Categorie.objects.all()
    context = {
        'isadmin':request.user.is_staff,
        'categories':categorie
    }
    return render(request,"votes.html",context )
@login_required(login_url="/login")
def categorie(request, categorie):
    categorie = Categorie.objects.filter(name= categorie)[0]
    candidats = Candidat.objects.filter(categorie = categorie)
    context = {
        'isadmin':request.user.is_staff,
        "candidats":candidats,
        "categorie":categorie
    }
    return render(request,"categorie.html", context)
@login_required(login_url="/login")
def update_votes(request, categorie, candidat):

    try:
        categorie_name = categorie
        candidat_name = candidat
        categorie = Categorie.objects.get(name=categorie_name)
        candidat_obj = Candidat.objects.get(name=candidat_name, categorie=categorie)
    except:
        return redirect(f'/categories/{categorie_name}')

    user = request.user

    votes = user.votes if hasattr(user, 'votes') else {}
    
    if votes.get(categorie_name) == candidat_name:
        return redirect(f'/categories/{categorie_name}')
    
    # Ancien candidat de cette catégorie, s'il existe
    ancien_candidat_name = votes.get(categorie_name)
    if ancien_candidat_name:
        try:
            ancien_candidat = Candidat.objects.get(name=ancien_candidat_name, categorie=categorie)
            ancien_candidat.NombreVotes -= 1
            ancien_candidat.save()
        except Candidat.DoesNotExist:
            pass

    votes[categorie_name] = candidat_name
    user.votes = votes
    user.save()

    candidat_obj.NombreVotes += 1
    candidat_obj.save()

    return redirect(f'/categories/{categorie_name}')




@login_required(login_url='/')
@user_passes_test(verify_super_user, login_url='/')
def admin_panel(request):
    return render(request, "adminPanel.html", {"user": request.user, "isadmin": request.user.is_staff})

@login_required(login_url='/')
@user_passes_test(verify_super_user, login_url='/')
def add_categorie(request):
    check = False
    if request.method == "POST":
        name = request.POST.get('nom')
        image = request.FILES.get('photo')
        categorie = Categorie(name=name, image=image)
        categorie.save()
        check = True
    return render(request, "addCategories.html", {"user": request.user, "isadmin": request.user.is_staff, "check": check})

@login_required(login_url='/')
@user_passes_test(verify_super_user, login_url='/')
def add_candidat(request):
    check = False
    if request.method == "POST":
        name = request.POST.get('nom')
        categorie_id = request.POST.get('categorie')
        image = request.FILES.get('photo')
        categorie = get_object_or_404(Categorie, id=categorie_id)
        candidat = Candidat(name=name, categorie=categorie, image=image)
        candidat.save()
        check = True
    categories = Categorie.objects.all()
    return render(request, "addCandidats.html", {"categories": categories, "user": request.user, "isadmin": request.user.is_staff, "check": check})

@login_required(login_url='/')
@user_passes_test(verify_super_user, login_url='/')
def add_user(request):
    check = False
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = CustomUser(username=username, password=make_password(password), is_staff=False)
        user.save()
        check= True
    return render(request, "addUsers.html", {"post": "add-users", "user": request.user, "isadmin": request.user.is_staff, "check": check})

@login_required(login_url='/')
@user_passes_test(verify_super_user, login_url='/')
def add_admin(request):
    check = False
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = CustomUser(username=username, password=make_password(password), is_staff=True)
        user.save()
        check= True
    return render(request, "addUsers.html", {"post": "add-admin", "user": request.user, "isadmin": request.user.is_staff, "check": check})

@login_required(login_url='/')
@user_passes_test(verify_super_user, login_url='/')
def view_results(request):
    categories = Categorie.objects.all()
    candidats_par_categorie = {}
    top_five_candidates_by_category = {}

    for categorie in categories:
        candidats = Candidat.objects.filter(categorie=categorie).order_by('-NombreVotes')
        candidats_par_categorie[categorie.name] = candidats
        top_five_candidates_by_category[categorie.name] = candidats[:5]

    return render(request, "results.html", {
        "candidats_par_categorie": candidats_par_categorie,
        "top_five_candidates_by_category": top_five_candidates_by_category,
        "user": request.user,
        "isadmin": request.user.is_staff
    })

def log_(request):
    if request.method == "POST":
        name = request.POST.get("username")
        password = request.POST.get("password")
        user =  authenticate(request, username=name, password = password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request,"login.html",{"error":"Les infos ne mactch pas veuillez reessayer"})
    return render(request,"login.html" )

def log_out(request):
    logout(request)
    return redirect("home")
