from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy
from gestion_riego.models import Persona
from gestion_riego.forms import PersonaForm


# Vistas basadas en clases
# Recomendable y haca a la aplicacion facilmente escalable
class PersonaCreateView(CreateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'gestion_riego/persona/persona_create.html'
    success_url = reverse_lazy('gestion_riego:persona_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nueva Persona'
        context['entity'] = 'Persona'
        context['list_url'] = reverse_lazy('gestion_riego:persona_list')
        context['action'] = 'add'
        # context['object_list'] = Device.objects.all()
        return context


class PersonaUpdateView(UpdateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'gestion_riego/persona/persona_create.html'
    success_url = reverse_lazy('gestion_riego:persona_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Persona'
        context['entity'] = 'Persona'
        context['list_url'] = reverse_lazy('gestion_riego:persona_list')
        context['action'] = 'edit'
        # context['object_list'] = Device.objects.all()
        return context


class PersonaDeleteView(DeleteView):
    model = Persona
    template_name = 'gestion_riego/persona/persona_verificacion.html'
    success_url = reverse_lazy('gestion_riego:persona_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class PersonaListView(ListView):
    model = Persona
    template_name = 'gestion_riego/persona/persona_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Personas'
        context['create_url'] = reverse_lazy('gestion_riego:persona_create')
        context['list_url'] = reverse_lazy('gestion_riego:persona_list')
        # context['object_list'] = Device.objects.all()
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    """
    def get_queryset(self):
        return self.model.objects.all()[:2] #Trae solo dos objetos"""
