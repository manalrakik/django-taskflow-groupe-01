from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task
from django import forms
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.utils import timezone


def home(request):
    return render(request, 'tasks/home.html')


def about(request):
    return render(request, 'tasks/about.html')

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    ordering = ['-date_creation']

    def get_queryset(self):
        queryset = Task.objects.filter(auteur=self.request.user)

        recherche = self.request.GET.get('q')
        if recherche:
            queryset = queryset.filter(titre__icontains=recherche)

        statut = self.request.GET.get('statut')
        if statut:
            queryset = queryset.filter(statut=statut)

        priorite = self.request.GET.get('priorite')
        if priorite:
            queryset = queryset.filter(priorite=priorite)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recherche'] = self.request.GET.get('q', '')
        context['statut_selectionne'] = self.request.GET.get('statut', '')
        context['priorite_selectionnee'] = self.request.GET.get('priorite', '')
        context['statut_choices'] = Task.STATUT_CHOICES
        context['priorite_choices'] = Task.PRIORITE_CHOICES
        return context
    
class DashboardView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/dashboard.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(auteur=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        taches = Task.objects.filter(auteur=self.request.user)
        aujourd_hui = timezone.now().date()

        context['total'] = taches.count()
        context['a_faire'] = taches.filter(statut='a_faire').count()
        context['en_cours'] = taches.filter(statut='en_cours').count()
        context['terminees'] = taches.filter(statut='termine').count()

        context['en_retard'] = taches.filter(
            date_limite__lt=aujourd_hui
        ).exclude(statut='termine').count()

        context['a_venir'] = taches.filter(
            date_limite__gte=aujourd_hui
        ).exclude(statut='termine').order_by('date_limite')[:5]

        return context
class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.auteur != self.request.user:
            raise PermissionDenied("Vous n'êtes pas autorisé à consulter cette tâche.")
        return obj

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['titre', 'description', 'statut', 'priorite', 'date_limite']
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['date_limite'].widget = forms.DateInput(attrs={'type': 'date'})
        return form

    def form_valid(self, form):
        form.instance.auteur = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['titre', 'description', 'statut', 'priorite', 'date_limite']
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['date_limite'].widget = forms.DateInput(attrs={'type': 'date'})
        return form

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.auteur != self.request.user:
            raise PermissionDenied("Vous n'êtes pas autorisé à modifier cette tâche.")
        return obj
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.auteur != self.request.user:
            raise PermissionDenied("Vous n'êtes pas autorisé à supprimer cette tâche.")
        return obj