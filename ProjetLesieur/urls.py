"""
URL configuration for ProjetLesieur project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from AppAudit.views import login_view,logout_view,import_users,list_users,delete_user,dashboard,import_xl_view,standards, dashboardUser, userAudit,operateurs,audits,historique_audits,planning,parametres,auditPrevuUser
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Auth
    path('',login_view,name="login"),
    path('logout',logout_view,name="logout"),
    # Admin
    path('dashboard', dashboard,name="dashboard"),
    path('standards', standards,name="standards"),
    path('audits', audits,name="audits"),
    path('historique_audits', historique_audits,name="historique_audits"),
    path('operateurs', operateurs,name="operateurs"),
    path('planning', planning,name="planning"),
    path('parametres', parametres,name="parametres"),
    # Auditeur
    path('dashboardUser', dashboardUser,name="dashboardUser"),
    path('userAudit', userAudit,name="userAudit"),
    path('auditPrevuUser', auditPrevuUser,name="auditPrevuUser"),
    path('admin/', admin.site.urls),
    # Utilitaires
    path('import_xl', import_xl_view,name="import_xl"),
   # Création des utilisateurs pour conenxion avec l'AD
    path('api/import-users/', import_users),
   # Listes des utilisateurs pour lien ave l'AD
   path('api/users/', list_users),
   # Supprimer des anciens utilisateurs lien avec l'AD 
   path('api/users/<str:username>/', delete_user),
]

# Ne marche que si on est en debug 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)