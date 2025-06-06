from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate,logout as auth_logout,login as auth_login
import json
import pandas as pd
from .models import Standard,Machine, Format,Audit,StandardAudit,Ligne,Photo
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group
from datetime import datetime
import locale
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserImportSerializer
from rest_framework import status



locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# ------------------------------------------
# Fonction
# ------------------------------------------
def get_lignes(filtre_ligne=None):
    lignes_list = []
    # Récupération des lignes
    if filtre_ligne : 
        objets_lignes = Ligne.objects.filter(numero_ligne=filtre_ligne)
    else : 
        objets_lignes = Ligne.objects.all()

    for ligne in objets_lignes:
        machines_list = []
        # Récupération de toutes les machines
        for machine in Machine.objects.filter(ligne=ligne):
            standards_list = []
            # Récupération des standards en fonction des machines
            for s in Standard.objects.filter(machine=machine):
                formats = Format.objects.filter(standard=s).values()
                standard_dict = {
                    "id": s.id,
                    "rep" : s.rep,
                    "designation": s.designation,
                    "unite": s.unite,
                    "description": s.description,
                    "photo": {
                        "url": s.photo.image.url if s.photo else None,
                        "titre": s.photo.titre if s.photo else None,
                        "description": s.photo.description if s.photo else None,
                        "date_ajout": s.photo.date_ajout if s.photo else None,
                    },
                    "formats": list(formats)
                }
                standards_list.append(standard_dict)
            # Liaison machines/standards dans un json
            machine_dict = {
                "id": machine.id,
                "designation": machine.designation,
                "standards": standards_list
            }
            machines_list.append(machine_dict)
        
        ligne_dict = {
            "id" : ligne.id,
            "num_ligne" : ligne.numero_ligne,
            "machines" : machines_list
        }
        lignes_list.append(ligne_dict)
    return lignes_list

# ------------------------------------------
#
# Templates
#
# ------------------------------------------

# ------------------------------------------
# Login 
# ------------------------------------------
@never_cache
def login_view(request):
    context ={}
    # Si la requête est GET et l'utilisateur est déjà connecté
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        redirect_url = "/dashboardUser" if request.user.groups.filter(name="Auditeur").exists() else "/dashboard"
        return redirect(redirect_url)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = authenticate(request, username=data["login"], password=data["mdp"])
            if user is not None :
                auth_login(request,user)
                print(user.groups.all())
                if any("Auditeur" in g.name for g in user.groups.all()):
                    return JsonResponse({"success" :True ,"redirect_url": "/dashboardUser"})  
                else :
                    return JsonResponse({"success" :True ,"redirect_url": "/dashboard"})         
            else :
                return JsonResponse({"success" :False, "message": "Identifiant et/ou mot de passe erroné(s) "})         

        except Exception as e:
            print(f"Erreur : {e}")

    context["site"] = "Coudekerque-Branche"
    return render(request,"login.html",context=context)

def logout_view(request):
    auth_logout(request)
    request.session.flush()
    return redirect('/')

# ------------------------------------------
# Vue admin
# ------------------------------------------
@never_cache
@login_required(login_url="/")
def dashboard(request):
    user = request.user
    context = {"data": {
        "prenom": user.first_name,
        "nom": user.last_name,
        "username" : user.username,
        "audits_en_retard": 5,
        "minutes_arret": 62,
        "rendement": 76
    }}
    context["site"] = "Coudekerque-Branche"
    return render(request, "dashboard.html", context=context)
    
@never_cache
@login_required(login_url="/")
def standards(request):
    context={}
    context["site"] = "Coudekerque-Branche"
    #context['lignes'] = get_lignes()
    ligne_list = []
    ligne_list = get_lignes()
    context["lignes"] = ligne_list
    #print(context)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            match data["fonction"] :
                case "filtre_standard":
                    try : 
                        ligne_list = get_lignes(data["filtre_ligne"])
                        print(ligne_list)
                        return JsonResponse({"lignes": ligne_list}, status=200)
                        context["lignes"] = ligne_list
                        print(context)
                        return render(request, "standards.html",context=context)
                    except Exception as e :
                        print(e)
                case "ajout_ligne":
                    #print(data["ligne"])
                    Ligne.objects.create(numero_ligne=data["ligne"])
                case "ajout_machine":
                    #print(data["ligne"] + data["machine"])
                    ligne = Ligne.objects.get(numero_ligne=data["ligne"])
                    Machine.objects.create(ligne=ligne,designation=data["machine"])
                case "ajout_standard":
                    print("Ajout standard")
                    Standard.objects.create(designation=data["designation"],valeur_attendue=data["valeur_attendue"],unite=data["unite"],machine=Machine.objects.get(id=int(data["machine"])))
        except Exception as e :
            print(e)
    #print(context)
    return render(request, "standards.html",context=context)

@never_cache
@login_required(login_url="/")
def audits(request):
    context = {}
    audit_list = []
    audit_dict = {}
    audits = Audit.objects.all()
    for audit in audits :
        audit_dict = {
                "id": audit.id,
                "date_prevu": audit.date_prevu,
                "date_realisee": audit.date_realisee,
                "statut" : audit.statut,
                "resultat" : audit.resultat,
                "auditeur" : audit.auditeur.get_full_name()
            }
        audit_list.append(audit_dict)
        
    context["audit_list"] = audit_list
    context["site"] = "Coudekerque-Branche"
    return render(request,"audits.html",context=context)

@never_cache
@login_required(login_url="/")
def historique_audits(request):
    context = {}
    context["site"] = "Coudekerque-Branche"
    audit_list = []
    audit_dict = {}
    audits = Audit.objects.filter(statut = "TERMINE")
    for audit in audits :
        audit_dict = {
                "id": audit.id,
                "date_prevu": audit.date_prevu,
                "date_realisee": audit.date_realisee,
                "statut" : audit.statut,
                "resultat" : audit.resultat,
                "auditeur" : audit.auditeur.get_full_name()
            }
        audit_list.append(audit_dict)
        
    context["audit_list"] = audit_list

    print(context)

    return render(request,"historique_audits.html",context=context)

@never_cache
@login_required(login_url="/")
def operateurs(request):
    context = {}
    users =  User.objects.all()
    user_dict = []
    for user in users :
        user_info = {
            "nom_prenom": "Administrateur" if user.username == "Admin" else f"{user.first_name} {user.last_name}",
            "mail" : user.email,
            "groups" : ", ".join(group.name for group in user.groups.all())
        }
        user_dict.append(user_info)
    
    context["operateurs"] = user_dict
    context["site"] = "Coudekerque-Branche"

    print(context)

    return render(request,"operateurs.html",context=context)

@never_cache
@login_required(login_url="/")
def planning(request):
    context = {}
    context["site"] = "Coudekerque-Branche"
    return render(request,"planning.html",context=context)

@never_cache
@login_required(login_url="/")
def parametres(request):
    context = {}
    photo = Photo.objects.first()
    context["site"] = "Coudekerque-Branche"
    context["photo"] = photo
    print(context)
    return render(request,"parametres.html",context=context)

# ------------------------------------------
# Vue auditeur
# ------------------------------------------
@never_cache
@login_required(login_url="/")
def dashboardUser(request):
    context = {}
    # user = request.user
    # context = {"data": {
    #     "site": "Coudekerque-Branche",
    #     "prenom": user.first_name,
    #     "nom": user.last_name,
    #     "username" : user.username,
    #     "audits_en_retard": 5,
    #     "minutes_arret": 62,
    #     "rendement": 76
    # }}
    context["site"] = "Coudekerque-Branche"
    return render(request, "dashboard_user.html", context=context)

@never_cache
@login_required(login_url="/")
def auditPrevuUser(request):
    context = {}
    context["site"] = "Coudekerque-Branche"
    liste_audits = []
    for audit in Audit.objects.filter(auditeur=request.user):
        # for audit_standard in StandardAudit.objects.filter(audit = audit):
        #     for standard in Standard.objects.filter(designation = standard):
        liste_audits.append(audit)
    context["audits"] = liste_audits
    return render(request, "audit_prevu_user.html", context=context)

@never_cache
@login_required(login_url="/")
def userAudit(request):

    date_aujourdhui = datetime.now()
    date_formatee = date_aujourdhui.strftime("%d %B %Y")

    context = {"date": date_formatee,
                1: {
                    "machine": "Etiqueteuse",
                    "standard": "Selettes",
                    "Valeurs": {
                        "isio41l": "Cyan",
                        "isio42l": "Magenta"
                    },
                    "Instruction": "Situé à la base des bouteilles dans les machines.",
                    "photo": "Aucune"
                },
                2: {
                    "machine": "Etiqueteuse",
                    "standard": "Selettes",
                    "Valeurs": {
                        "isio41l": "Cyan",
                        "isio42l": "Magenta"
                    },
                    "Instruction": "Situé à la base des bouteilles dans les machines.",
                    "photo": "Aucune"
                },
                3: {
                    "machine": "Etiqueteuse",
                    "standard": "Selettes",
                    "Valeurs": {
                        "isio41l": "Cyan",
                        "isio42l": "Magenta"
                    },
                    "Instruction": "Situé à la base des bouteilles dans les machines.",
                    "photo": "Aucune"
                }
            }
    context["site"] = "Coudekerque-Branche"
    return render(request, "user_audit.html", context=context)

# ------------------
# Lien avec l'AD
# ------------------

# ------------------
# Création des utilisateurs depuis l'AD
# ------------------


@api_view(['POST'])
def import_users(request):
    serializer = UserImportSerializer(data=request.data, many=True)
    if serializer.is_valid():
        for user_data in serializer.validated_data:
            User.objects.update_or_create(
                username=user_data['username'],
                defaults={
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'email': user_data['email'],
                }
            )
        return Response({"status": "success"})
    return Response(serializer.errors, status=400)




# ------------------
# Lister les utilisateurs existants sur django 
# ------------------

@api_view(['GET'])
def list_users(request):
    users = User.objects.all().values_list('username', flat=True)
    return Response(users)

# ------------------
# Supprimer les utilisateurs
# ------------------
@api_view(['DELETE'])
def delete_user(request, username):
    try:
        user = User.objects.get(username=username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# test excel
def import_xl_view(request):
    context = {}
    try :   
        data = pd.read_excel("AppAudit/static/excel/AUDIT STANDARDS REGLAGES GE.xlsx",engine="openpyxl")
        data_html = data.head().to_html()
        print(data.head().to_json())
        context ={"data": data}
        
    except Exception as e :
        context ={"data": e}
        print(e)
    return render(request,"read_xl.html",context=context)