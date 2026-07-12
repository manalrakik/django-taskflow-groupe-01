from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUT_CHOICES = [
        ('a_faire', 'À faire'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminée'),
    ]
    PRIORITE_CHOICES = [
        ('basse', 'Basse'),
        ('moyenne', 'Moyenne'),
        ('haute', 'Haute'),
    ]

    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='a_faire')
    priorite = models.CharField(max_length=20, choices=PRIORITE_CHOICES, default='moyenne')
    date_limite = models.DateField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titre