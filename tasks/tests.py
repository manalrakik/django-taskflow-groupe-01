from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task


class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.task = Task.objects.create(
            titre='Tâche de test',
            description='Description de test',
            statut='a_faire',
            priorite='moyenne',
            auteur=self.user
        )

    def test_task_creation(self):
        """Vérifie qu'une tâche est bien créée avec les bonnes valeurs"""
        self.assertEqual(self.task.titre, 'Tâche de test')
        self.assertEqual(self.task.statut, 'a_faire')
        self.assertEqual(self.task.auteur, self.user)

    def test_task_str_representation(self):
        """Vérifie que __str__ renvoie bien le titre"""
        self.assertEqual(str(self.task), 'Tâche de test')


class TaskViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.task = Task.objects.create(
            titre='Tâche visible',
            description='Description',
            statut='a_faire',
            priorite='haute',
            auteur=self.user
        )

    def test_home_page_status_code(self):
        """Vérifie que la page d'accueil répond correctement"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_about_page_status_code(self):
        """Vérifie que la page à propos répond correctement"""
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_task_list_view(self):
        """Vérifie qu'un utilisateur connecté voit bien sa liste de tâches"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tâche visible')

    def test_task_detail_view(self):
        """Vérifie qu'un utilisateur connecté peut voir le détail de sa propre tâche"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('task_detail', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tâche visible')

    def test_task_create_requires_login(self):
        """Vérifie qu'un utilisateur non connecté est redirigé s'il essaie de créer une tâche"""
        response = self.client.get(reverse('task_create'))
        self.assertNotEqual(response.status_code, 200)

    def test_task_create_logged_in(self):
        """Vérifie qu'un utilisateur connecté peut créer une tâche"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('task_create'), {
            'titre': 'Nouvelle tâche créée',
            'description': 'Description test',
            'statut': 'a_faire',
            'priorite': 'basse',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(titre='Nouvelle tâche créée').exists())

    def test_task_update(self):
        """Vérifie qu'un utilisateur connecté peut modifier une tâche"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('task_update', args=[self.task.pk]), {
            'titre': 'Tâche modifiée',
            'description': 'Description modifiée',
            'statut': 'en_cours',
            'priorite': 'haute',
        })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.titre, 'Tâche modifiée')

    def test_task_delete(self):
        """Vérifie qu'un utilisateur connecté peut supprimer une tâche"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('task_delete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_user_cannot_access_others_task(self):
        """Vérifie qu'un utilisateur ne peut pas consulter la tâche d'un autre utilisateur"""
        other_user = User.objects.create_user(username='otheruser', password='otherpass123')
        self.client.login(username='otheruser', password='otherpass123')
        response = self.client.get(reverse('task_detail', args=[self.task.pk]))
        self.assertEqual(response.status_code, 403)

    def test_user_list_only_shows_own_tasks(self):
        """Vérifie qu'un utilisateur ne voit que ses propres tâches dans la liste"""
        other_user = User.objects.create_user(username='otheruser', password='otherpass123')
        Task.objects.create(
            titre='Tâche d\'un autre utilisateur',
            statut='a_faire',
            priorite='basse',
            auteur=other_user
        )
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('task_list'))
        self.assertContains(response, 'Tâche visible')
        self.assertNotContains(response, 'Tâche d\'un autre utilisateur')