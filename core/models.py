from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import calendar
import datetime
from datetime import date, timedelta


class Machine(models.Model):
    nom = models.CharField(max_length=100)
    type = models.CharField(
    
          max_length=50,
          choices=[('tour', 'Tour'), ('perceuse', 'Perceuse')]
    )
    statut = models.CharField(
        max_length=20,
        choices=[
            ('operationnel', '🟢 Opérationnel'),
            ('en_panne', '🔴 En panne')
        ]
    )
    derniere_maintenance = models.DateField(null=True, blank=True)  # ← AJOUT ICI
    frequence_jours = models.PositiveIntegerField(default=30)  # fréquence en jours
    emplacement = models.CharField(max_length=100, blank=True)
    maintenances = models.ManyToManyField('PlanMaintenance', related_name="machines", blank=True)

    @property
    def prochaine_maintenance(self):
        if self.derniere_maintenance:
            return self.derniere_maintenance + timedelta(days=self.frequence_jours)
        return None

    @property
    def jours_restant(self):
        if self.prochaine_maintenance:
            return (self.prochaine_maintenance - date.today()).days
        return None

    @property
    def alerte_maintenance(self):
        if self.jours_restant is None:
            return "🔘 Inconnu"
        elif self.jours_restant < 0:
            return "🔴 En retard"
        elif self.jours_restant <= 7:
            return "🟡 Bientôt"
        else:
            return "🟢 OK"

    def __str__(self):
        return self.nom

class PieceRechange(models.Model):
    code = models.CharField(max_length=20, unique=True)
    designation = models.CharField(max_length=100)
    quantite_stock = models.PositiveIntegerField()
    seuil_alerte = models.PositiveIntegerField(default=5)
    prix_unitaire = models.DecimalField(max_digits=8, decimal_places=2)
    
    machines_compatibles = models.ManyToManyField(Machine)

    def __str__(self):
        return f"{self.code} - {self.designation}"

    def en_alerte(self):
        return self.quantite_stock <= self.seuil_alerte

class Intervention(models.Model):
    machine = models.ForeignKey('Machine', on_delete=models.CASCADE, related_name='interventions')
    technicien = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)

    date_planifiee = models.DateField(null=True, blank=True)  # Date prévue
    date_intervention = models.DateField(null=True, blank=True)  # Date réelle (remplie à la clôture)
    etat_final = models.CharField(max_length=200, blank=True)
    duree_total = models.IntegerField(null=True, blank=True)  # en minutes

    STATUT_CHOICES = (
        ('planifiee', 'Planifiée'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
    )
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='planifiee')
    terminee = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.machine.nom} - {self.date_planifiee}"

class Notification(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    type = models.CharField(max_length=50, choices=[('alerte', 'Alerte'), ('panne', 'Panne'), ('maintenance', 'Maintenance')])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.machine.nom} - {self.type}"

class MesureCapteur(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    date = models.DateTimeField()
    temperature = models.FloatField()
    vibration = models.FloatField()

    def __str__(self):
        return f"Capteurs {self.machine.nom} ({self.date})"    

    
class PlanMaintenance(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    machine = models.ForeignKey('Machine', on_delete=models.CASCADE)
    reglementaire = models.BooleanField(default=False)
    assignes = models.ManyToManyField(User, related_name='plans_assignes', blank=True)
    labels = models.CharField(max_length=255, blank=True)
    checklist = models.TextField(blank=True, null=True)

    temps_maintenance_minutes = models.PositiveIntegerField(default=0)
    temps_arret_minutes = models.PositiveIntegerField(default=0)

    frequence = models.IntegerField(default=1)
    unite = models.CharField(max_length=20, choices=[
        ('jours', 'Jours'),
        ('semaines', 'Semaines'),
        ('mois', 'Mois'),
        ('annees', 'Années')
    ])
    date_debut = models.DateField()
    date_fin = models.DateField(blank=True, null=True)
    periodicite = models.CharField(max_length=50, blank=True, null=True)


    def __str__(self):
        return f"Plan: {self.titre} ({self.machine.nom})"

    @property
    def prochaine_occurrence(self):
        if not self.periodicite or not self.frequence:
            return None

        if self.periodicite == 'quotidienne':
            return self.date_debut + timedelta(days=self.frequence)
        elif self.periodicite == 'hebdomadaire':
            return self.date_debut + timedelta(weeks=self.frequence)
        elif self.periodicite == 'mensuelle':
            next_date = self.date_debut
            for _ in range(self.frequence):
                month = next_date.month + 1
                year = next_date.year + month // 12
                month = month % 12
                if month == 0:
                    month = 12
                    year -= 1
                next_date = date(year, month, min(next_date.day, calendar.monthrange(year, month)[1]))
            return next_date
        elif self.periodicite == 'annuelle':
            return date(self.date_debut.year + self.frequence, self.date_debut.month, self.date_debut.day)
        return None