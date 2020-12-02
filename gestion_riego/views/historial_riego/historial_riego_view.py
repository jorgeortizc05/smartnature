from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from rest_framework import viewsets
from gestion_riego.serializers import HistorialRiegoSerializer

from gestion_riego.models import HistorialRiego


# Vistas basadas en clases
# Recomendable y haca a la aplicacion facilmente escalable
class HistorialRiegoListView(ListView):
    model = HistorialRiego
    template_name = 'gestion_riego/historial_riego/historial_riego.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all().order_by('id')

    #Listar con ajax
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in HistorialRiego.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False) #como uso coleccion de satos agrego safe=False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Riego'
        context['entity'] = 'HistorialRiego'
        context['list_url'] = reverse_lazy('gestion_riego:historial_riego')
        return context

class HistorialRiegoViewSet(viewsets.ModelViewSet):
    serializer_class = HistorialRiegoSerializer
    queryset = HistorialRiego.objects.all().order_by('id') #ordenados por id