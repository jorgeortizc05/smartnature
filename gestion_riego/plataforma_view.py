from django.shortcuts import render, redirect
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy
from .models import Plataforma
from .forms import PlataformaForm
import serial, json

#Vistas basadas en clases
#Recomendable y haca a la aplicacion facilmente escalable
class PlataformaCreate(CreateView):
    model = Plataforma
    form_class = PlataformaForm
    template_name = 'gestion_riego/plataforma/plataforma_create.html'
    success_url = reverse_lazy('plataforma_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nueva Plataforma'
        context['entity'] = 'Plataforma'
        context['list_url'] = reverse_lazy('plataforma_list')
        context['action'] = 'add'
        #context['object_list'] = Device.objects.all()
        return context
    

class PlataformaUpdate(UpdateView):
    model = Plataforma
    form_class = PlataformaForm
    template_name = 'gestion_riego/plataforma/plataforma_create.html'
    success_url = reverse_lazy('plataforma_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Plataforma'
        context['entity'] = 'Plataforma'
        context['list_url'] = reverse_lazy('plataforma_list')
        context['action'] = 'add'
        #context['object_list'] = Device.objects.all()
        return context

class PlataformaDelete(DeleteView):
    model = Plataforma
    template_name = 'gestion_riego/plataforma/plataforma_verificacion.html'
    success_url = reverse_lazy('plataforma_list')

class PlataformaList(ListView):
    model = Plataforma
    template_name = 'gestion_riego/plataforma/plataforma_list.html'