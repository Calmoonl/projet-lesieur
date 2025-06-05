from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from AppAudit.models import Audit  
import random

class Command(BaseCommand):
    help = "Attribue aléatoirement les audits non attribués à des utilisateurs"

    def handle(self, *args, **kwargs):
        audits = Audit.objects.filter(statut='NON_ATTRIBUE')
        utilisateurs = User.objects.all()

        if not utilisateurs.exists():
            self.stdout.write(" Aucun utilisateur disponible.")
            return

        if not audits.exists():
            self.stdout.write(" Tous les audits sont déjà attribués.")
            return

        for audit in audits:
            utilisateur = random.choice(utilisateurs)
            audit.auditeur = utilisateur
            audit.statut = 'EN_COURS'
            audit.save()
            self.stdout.write(f" Audit {audit.id} attribué à {utilisateur.username}")
