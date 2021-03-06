from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, TemplateView
from django.http import JsonResponse
from gestion_riego.forms import PlataformaForm
from gestion_riego.models import Plataforma
from gestion_riego.serializers import PlataformaSerializer
from rest_framework import viewsets


# Vistas basadas en clases
# Recomendable y haca a la aplicacion facilmente escalable
class PlataformaCreateView(CreateView):
    model = Plataforma
    form_class = PlataformaForm
    template_name = 'gestion_riego/plataforma/plataforma_create.html'
    success_url = reverse_lazy('gestion_riego:plataforma_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            print(action)
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nueva Plataforma'
        context['entity'] = 'Plataforma'
        context['list_url'] = reverse_lazy('gestion_riego:plataforma_list')
        context['action'] = 'add'
        # context['object_list'] = Device.objects.all()
        return context


class PlataformaUpdateView(UpdateView):
    model = Plataforma
    form_class = PlataformaForm
    template_name = 'gestion_riego/plataforma/plataforma_create.html'
    success_url = reverse_lazy('gestion_riego:plataforma_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            print(action)
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Plataforma'
        context['entity'] = 'Plataforma'
        context['list_url'] = reverse_lazy('gestion_riego:plataforma_list')
        context['action'] = 'edit'
        # context['object_list'] = Device.objects.all()
        return context


class PlataformaDeleteView(DeleteView):
    model = Plataforma
    template_name = 'gestion_riego/plataforma/plataforma_verificacion.html'
    success_url = reverse_lazy('gestion_riego:plataforma_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Plataforma'
        context['entity'] = 'Plataforma'
        context['list_url'] = reverse_lazy('gestion_riego:plataforma_list')
        # context['object_list'] = Device.objects.all()
        return context


class PlataformaListView(TemplateView):
    model = Plataforma
    template_name = 'gestion_riego/plataforma/plataforma_list.html'

    @method_decorator(
        csrf_exempt)  # para el post desabilito la protección, recuerda que sin la csrf no podra procesar info
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'load_plataformas':
                data = []
                for i in Plataforma.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Plataformas'
        context['entity'] = 'Plataforma'
        context['create_url'] = reverse_lazy('gestion_riego:plataforma_create')
        context['list_url'] = reverse_lazy('gestion_riego:plataforma_list')
        # context['object_list'] = Device.objects.all()
        return context


class PlataformaViewSet(viewsets.ModelViewSet):
    serializer_class = PlataformaSerializer
    queryset = Plataforma.objects.all()
