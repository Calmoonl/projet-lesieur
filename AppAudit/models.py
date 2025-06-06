from django.db import models
from django.contrib.auth.models import User


class Ligne(models.Model):
    numero_ligne = models.CharField(max_length=10)

    class Meta:
        indexes = [models.Index(fields=['numero_ligne'])]

    def __str__(self):
        return f"Ligne {self.numero_ligne}"


class Machine(models.Model):
    designation = models.TextField()
    ligne = models.ForeignKey(Ligne, on_delete=models.CASCADE, related_name='machines')

    def __str__(self):
        return self.designation


class Photo(models.Model):
    titre = models.CharField(max_length=255)
    image = models.ImageField(upload_to='photos/')
    description = models.TextField(blank=True, null=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre


class Standard(models.Model):
    designation = models.TextField()
    unite = models.TextField(null=True, blank=True)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='standards')
    description = models.TextField(null=True, blank=True)
    rep = models.TextField(null=True, blank=True)
    photo = models.ForeignKey(Photo, null=True, blank=True, on_delete=models.SET_NULL, related_name="standards")

    def __str__(self):
        return self.designation


class Format(models.Model):
    nom = models.CharField(max_length=255)
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, related_name="formats")
    valeur_attendue = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Audit(models.Model):
    STATUT_CHOICES = [
        ('EN_COURS', 'En cours'),
        ('TERMINE', 'Terminé'),
        ('NON_ATTRIBUE', 'Pas attribué'),
    ]

    RESULTAT_CHOICES = [
        ('REUSSI', 'Réussi'),
        ('ECHOUE', 'Échoué'),
    ]

    duree = models.DurationField()
    niveau = models.CharField(max_length=50)
    itineraire = models.TextField()
    auditeur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audits')
    date_prevu = models.DateField()
    date_realisee = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='NON_ATTRIBUE')
    resultat = models.CharField(max_length=20, choices=RESULTAT_CHOICES, null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=['niveau']), models.Index(fields=['date_prevu'])]

    def __str__(self):
        return f"Audit {self.id} - {self.date_prevu}"


class StandardAudit(models.Model):
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, related_name='standard_audits')
    audit = models.ForeignKey(Audit, on_delete=models.CASCADE, related_name='standard_audits')
    commentaire = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.standard.designation} - Audit {self.audit.id}"
