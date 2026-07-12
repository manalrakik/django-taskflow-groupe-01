from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task
from django import forms
from django import forms
from django.core.exceptions import PermissionDenied


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
        return Task.objects.filter(auteur=self.request.user)
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