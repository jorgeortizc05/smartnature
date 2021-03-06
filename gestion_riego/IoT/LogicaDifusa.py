# import os
# import sys
# #Las configuraciones esta en el proyecto princial, necesito estar alli, asi que primero
# #print(sys.path) veo mi path, estoy dentro de de varias carpetas de la raiz
# #asi que dejo posicionarme en el proyecto raiz como ha continuacion
# PROJECT_ROOT = sys.path.insert(0,"/casaortiz/django/smartnature")
# #print("Tu base es:", PROJECT_ROOT)
# from django.core.asgi import get_asgi_application
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# application = get_asgi_application()  # modulo para importar los settings django y trabajar con modelos

import time
from datetime import datetime, timedelta

import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
import sys
import matplotlib.pyplot as plt

from gestion_riego.models import Sensor
from django.db.models import Sum, Avg, Max, Min
from django.db.models.functions import Coalesce
from datetime import datetime, timedelta
from config.ubicacion_archivo import imagen_fuzzy1, imagen_fuzzy4, imagen_fuzzy3
import time


# Permite el calculo de la logica difusa de 1, 3 y 4 variables.
class LogicaDifusa:

    def fuzzy_logic_1_variables(self, par_humedad_suelo, id_historial_riego, desea_grafica):
        try:
            humedad_suelo = ctrl.Antecedent(np.arange(0, 1024, 1), 'humedad_suelo')
            tiempo_riego = ctrl.Consequent(np.arange(-2, 18, 1), 'tiempo_riego')

            # Auto-membership function population is possible with .automf(3, 5, or 7)
            humedad_suelo['seco'] = fuzz.trimf(humedad_suelo.universe, [0, 100, 200])
            humedad_suelo['semi_seco'] = fuzz.trimf(humedad_suelo.universe, [120, 310, 500])
            humedad_suelo['humedo'] = fuzz.trimf(humedad_suelo.universe, [450, 572, 694])
            humedad_suelo['semi_humedo'] = fuzz.trimf(humedad_suelo.universe, [658, 725, 792])
            humedad_suelo['encharcado'] = fuzz.trimf(humedad_suelo.universe, [750, 887, 1024])

            # Custom membership functions can be built interactively with a familiar,
            # Pythonic API
            tiempo_riego['nada'] = fuzz.trimf(tiempo_riego.universe, [-2, -1, 0])
            tiempo_riego['poco'] = fuzz.trimf(tiempo_riego.universe, [0, 2, 4])
            tiempo_riego['medio'] = fuzz.trimf(tiempo_riego.universe, [3, 6, 9])
            tiempo_riego['bastante'] = fuzz.trimf(tiempo_riego.universe, [7, 9, 12])
            tiempo_riego['mucho'] = fuzz.trapmf(tiempo_riego.universe, [10, 13, 17, 17])

            rule1 = ctrl.Rule(humedad_suelo['encharcado'], tiempo_riego['nada'])
            rule2 = ctrl.Rule(humedad_suelo['semi_humedo'], tiempo_riego['poco'])
            rule3 = ctrl.Rule(humedad_suelo['humedo'], tiempo_riego['medio'])
            rule4 = ctrl.Rule(humedad_suelo['semi_seco'], tiempo_riego['bastante'])
            rule5 = ctrl.Rule(humedad_suelo['seco'], tiempo_riego['mucho'])

            tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
            tipping = ctrl.ControlSystemSimulation(tipping_ctrl)
            tipping.input['humedad_suelo'] = par_humedad_suelo
            tipping.compute()
            minutos_riego = tipping.output['tiempo_riego']
            if desea_grafica:
                grafica = tiempo_riego.view(sim=tipping)
                plt.savefig(self.ubicacion_imagen_fuzzy1() + id_historial_riego)
                plt.close(grafica)
            if minutos_riego > 0:
                return minutos_riego
            else:
                return 0
        except Exception:
            print("Fuera de rango en las entradas de variables de humedad: ", sys.exc_info()[1], ' humedad suelo:',
                  par_humedad_suelo)
            return 0;

    def fuzzy_logic_3_variables(self, par_humedad_suelo, par_humedad_ambiental, par_temperatura_ambiental,
                                id_historial_riego, desea_grafica):
        try:
            humedad_suelo = ctrl.Antecedent(np.arange(0, 1024, 1), 'humedad_suelo')
            temperatura_ambiental = ctrl.Antecedent(np.arange(5, 46, 1), 'temperatura_ambiental')
            humedad_ambiental = ctrl.Antecedent(np.arange(0, 101, 1), 'humedad_ambiental')
            tiempo_riego = ctrl.Consequent(np.arange(-2, 18, 1), 'tiempo_riego')

            # Auto-membership function population is possible with .automf(3, 5, or 7)
            humedad_suelo['seco'] = fuzz.trimf(humedad_suelo.universe, [0, 100, 200])
            humedad_suelo['semi_seco'] = fuzz.trimf(humedad_suelo.universe, [120, 310, 500])
            humedad_suelo['humedo'] = fuzz.trimf(humedad_suelo.universe, [450, 572, 694])
            humedad_suelo['semi_humedo'] = fuzz.trimf(humedad_suelo.universe, [658, 725, 792])
            humedad_suelo['encharcado'] = fuzz.trimf(humedad_suelo.universe, [750, 887, 1024])

            temperatura_ambiental['baja'] = fuzz.trimf(temperatura_ambiental.universe, [5, 7, 10])
            temperatura_ambiental['media'] = fuzz.trimf(temperatura_ambiental.universe, [8, 17, 27])
            temperatura_ambiental['alta'] = fuzz.trimf(temperatura_ambiental.universe, [24, 34, 45])

            humedad_ambiental['baja'] = fuzz.trimf(humedad_ambiental.universe, [0, 16, 33])
            humedad_ambiental['media'] = fuzz.trimf(humedad_ambiental.universe, [16, 41, 66])
            humedad_ambiental['alta'] = fuzz.trimf(humedad_ambiental.universe, [41, 70, 100])

            # Custom membership functions can be built interactively with a familiar,
            # Pythonic API
            tiempo_riego['nada'] = fuzz.trimf(tiempo_riego.universe, [-2, -1, 0])
            tiempo_riego['poco'] = fuzz.trimf(tiempo_riego.universe, [0, 2, 4])
            tiempo_riego['medio'] = fuzz.trimf(tiempo_riego.universe, [3, 6, 9])
            tiempo_riego['bastante'] = fuzz.trimf(tiempo_riego.universe, [7, 9, 12])
            tiempo_riego['mucho'] = fuzz.trapmf(tiempo_riego.universe, [10, 13, 17, 17])
            rule1 = ctrl.Rule(humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'],
                              tiempo_riego['nada'])
            rule2 = ctrl.Rule(humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['media'],
                              tiempo_riego['nada'])
            rule3 = ctrl.Rule(humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'],
                              tiempo_riego['nada'])
            rule4 = ctrl.Rule(humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['baja'],
                              tiempo_riego['nada'])
            rule5 = ctrl.Rule(humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['media'],
                              tiempo_riego['nada'])
            rule6 = ctrl.Rule(humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['alta'],
                              tiempo_riego['nada'])
            rule7 = ctrl.Rule(humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'],
                              tiempo_riego['nada'])
            rule8 = ctrl.Rule(humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['media'],
                              tiempo_riego['nada'])
            rule9 = ctrl.Rule(humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'],
                              tiempo_riego['nada'])
            rule10 = ctrl.Rule(humedad_suelo['semi_humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'],
                               tiempo_riego['nada'])
            rule11 = ctrl.Rule(
                humedad_suelo['semi_humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['media'],
                tiempo_riego['nada'])
            rule12 = ctrl.Rule(humedad_suelo['semi_humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'],
                               tiempo_riego['nada'])
            rule13 = ctrl.Rule(
                humedad_suelo['semi_humedo'] & temperatura_ambiental['media'] & humedad_ambiental['baja'],
                tiempo_riego['poco'])
            rule14 = ctrl.Rule(
                humedad_suelo['semi_humedo'] & temperatura_ambiental['media'] & humedad_ambiental['media'],
                tiempo_riego['nada'])
            rule15 = ctrl.Rule(
                humedad_suelo['semi_humedo'] & temperatura_ambiental['media'] & humedad_ambiental['alta'],
                tiempo_riego['nada'])
            rule16 = ctrl.Rule(humedad_suelo['semi_humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'],
                               tiempo_riego['medio'])
            rule17 = ctrl.Rule(
                humedad_suelo['semi_humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['media'],
                tiempo_riego['poco'])
            rule18 = ctrl.Rule(humedad_suelo['semi_humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'],
                               tiempo_riego['nada'])
            rule19 = ctrl.Rule(humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'],
                               tiempo_riego['nada'])
            rule20 = ctrl.Rule(humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['media'],
                               tiempo_riego['nada'])
            rule21 = ctrl.Rule(humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'],
                               tiempo_riego['nada'])
            rule22 = ctrl.Rule(humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['baja'],
                               tiempo_riego['poco'])
            rule23 = ctrl.Rule(humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['media'],
                               tiempo_riego['poco'])
            rule24 = ctrl.Rule(humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['alta'],
                               tiempo_riego['nada'])
            rule25 = ctrl.Rule(humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'],
                               tiempo_riego['medio'])
            rule26 = ctrl.Rule(humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['media'],
                               tiempo_riego['poco'])
            rule27 = ctrl.Rule(humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'],
                               tiempo_riego['nada'])
            rule28 = ctrl.Rule(humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'],
                               tiempo_riego['poco'])
            rule29 = ctrl.Rule(humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['media'],
                               tiempo_riego['nada'])
            rule30 = ctrl.Rule(humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'],
                               tiempo_riego['nada'])
            rule31 = ctrl.Rule(humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['baja'],
                               tiempo_riego['bastante'])
            rule32 = ctrl.Rule(humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['media'],
                               tiempo_riego['medio'])
            rule33 = ctrl.Rule(humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['alta'],
                               tiempo_riego['poco'])
            rule34 = ctrl.Rule(humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'],
                               tiempo_riego['mucho'])
            rule35 = ctrl.Rule(humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['media'],
                               tiempo_riego['bastante'])
            rule36 = ctrl.Rule(humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'],
                               tiempo_riego['mucho'])
            rule37 = ctrl.Rule(humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'],
                               tiempo_riego['medio'])
            rule38 = ctrl.Rule(humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['media'],
                               tiempo_riego['medio'])
            rule39 = ctrl.Rule(humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'],
                               tiempo_riego['poco'])
            rule40 = ctrl.Rule(humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['baja'],
                               tiempo_riego['mucho'])
            rule41 = ctrl.Rule(humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['media'],
                               tiempo_riego['mucho'])
            rule42 = ctrl.Rule(humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['alta'],
                               tiempo_riego['bastante'])
            rule43 = ctrl.Rule(humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'],
                               tiempo_riego['mucho'])
            rule44 = ctrl.Rule(humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['media'],
                               tiempo_riego['mucho'])
            rule45 = ctrl.Rule(humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'],
                               tiempo_riego['mucho'])

            tipping_ctrl = ctrl.ControlSystem(
                [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14,
                 rule15,
                 rule16,
                 rule17, rule18, rule19, rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27, rule28, rule29,
                 rule30,
                 rule31, rule32, rule33, rule34, rule3, rule36,
                 rule37, rule38, rule39, rule40, rule41, rule42, rule43, rule44, rule45])
            tipping = ctrl.ControlSystemSimulation(tipping_ctrl)
            tipping.input['humedad_suelo'] = par_humedad_suelo
            tipping.input['humedad_ambiental'] = par_humedad_ambiental
            tipping.input['temperatura_ambiental'] = par_temperatura_ambiental
            tipping.compute()
            minutos_riego = tipping.output['tiempo_riego']
            if desea_grafica:
                grafica = tiempo_riego.view(sim=tipping)
                plt.savefig(self.ubicacion_imagen_fuzzy3() + id_historial_riego)
                plt.close(grafica)
            if minutos_riego > 0:
                return minutos_riego
            else:
                return 0
        except Exception:
            print("Fuera de rango: ", sys.exc_info()[1], ' humedad suelo:', par_humedad_suelo)
            print("Humd Ambiente: ", par_humedad_ambiental)
            print("Temp Ambiente: ", par_temperatura_ambiental)
            return 0;

    def fuzzy_logic_4_variables(self, par_humedad_suelo, par_humedad_ambiental, par_temperatura_ambiental,
                                par_evapo,
                                id_historial_riego, desea_grafica):
        try:
            humedad_suelo = ctrl.Antecedent(np.arange(0, 1024, 1), 'humedad_suelo')
            temperatura_ambiental = ctrl.Antecedent(np.arange(5, 46, 1), 'temperatura_ambiental')
            humedad_ambiental = ctrl.Antecedent(np.arange(0, 101, 1), 'humedad_ambiental')
            evapo = ctrl.Antecedent(np.arange(0, 9, 1), 'evapo')
            tiempo_riego = ctrl.Consequent(np.arange(-2, 18, 1), 'tiempo_riego')

            # Auto-membership function population is possible with .automf(3, 5, or 7)
            humedad_suelo['seco'] = fuzz.trimf(humedad_suelo.universe, [0, 100, 200])
            humedad_suelo['semi_seco'] = fuzz.trimf(humedad_suelo.universe, [120, 310, 500])
            humedad_suelo['humedo'] = fuzz.trimf(humedad_suelo.universe, [450, 572, 694])
            humedad_suelo['semi_encharcado'] = fuzz.trimf(humedad_suelo.universe, [658, 725, 792])
            humedad_suelo['encharcado'] = fuzz.trimf(humedad_suelo.universe, [750, 887, 1024])

            temperatura_ambiental['baja'] = fuzz.trimf(temperatura_ambiental.universe, [5, 7, 10])
            temperatura_ambiental['media'] = fuzz.trimf(temperatura_ambiental.universe, [8, 17, 27])
            temperatura_ambiental['alta'] = fuzz.trimf(temperatura_ambiental.universe, [24, 34, 45])

            humedad_ambiental['baja'] = fuzz.trimf(humedad_ambiental.universe, [0, 16, 33])
            humedad_ambiental['media'] = fuzz.trimf(humedad_ambiental.universe, [16, 41, 66])
            humedad_ambiental['alta'] = fuzz.trimf(humedad_ambiental.universe, [41, 70, 100])

            evapo['baja'] = fuzz.trimf(evapo.universe, [0, 2, 4])
            evapo['media'] = fuzz.trimf(evapo.universe, [2, 4, 6])
            evapo['alta'] = fuzz.trimf(evapo.universe, [4, 6, 8])

            # Custom membership functions can be built interactively with a familiar,
            # Pythonic API
            tiempo_riego['nada'] = fuzz.trimf(tiempo_riego.universe, [-2, -1, 0])
            tiempo_riego['poco'] = fuzz.trimf(tiempo_riego.universe, [0, 2, 4])
            tiempo_riego['medio'] = fuzz.trimf(tiempo_riego.universe, [3, 6, 9])
            tiempo_riego['bastante'] = fuzz.trimf(tiempo_riego.universe, [7, 9, 12])
            tiempo_riego['mucho'] = fuzz.trapmf(tiempo_riego.universe, [10, 13, 17, 17])
            rule1 = ctrl.Rule(
                humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['baja'],
                tiempo_riego['nada'])
            rule2 = ctrl.Rule(
                humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo[
                    'media'],
                tiempo_riego['nada'])
            rule3 = ctrl.Rule(
                humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['alta'],
                tiempo_riego['nada'])
            rule4 = ctrl.Rule(
                humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo[
                    'baja'],
                tiempo_riego['nada'])
            rule5 = ctrl.Rule(
                humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo[
                    'media'],
                tiempo_riego['nada'])
            rule6 = ctrl.Rule(
                humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo[
                    'alta'],
                tiempo_riego['nada'])
            rule7 = ctrl.Rule(
                humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['baja'],
                tiempo_riego['nada'])
            rule8 = ctrl.Rule(
                humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo[
                    'media'],
                tiempo_riego['nada'])
            rule9 = ctrl.Rule(
                humedad_suelo['encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['alta'],
                tiempo_riego['nada'])
            rule10 = ctrl.Rule(
                humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo[
                    'baja'],
                tiempo_riego['nada'])
            rule11 = ctrl.Rule(
                humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo[
                    'media'],
                tiempo_riego['nada'])
            rule12 = ctrl.Rule(
                humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo[
                    'alta'],
                tiempo_riego['nada'])
            rule13 = ctrl.Rule(
                humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo[
                    'baja'],
                tiempo_riego['nada'])
            rule14 = ctrl.Rule(
                humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo[
                    'media'],
                tiempo_riego['nada'])
            rule15 = ctrl.Rule(
                humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo[
                    'alta'],
                tiempo_riego['nada'])
            rule16 = ctrl.Rule(
                humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo[
                    'baja'],
                tiempo_riego['nada'])
            rule17 = ctrl.Rule(
                humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo[
                    'media'],
                tiempo_riego['nada'])
            rule18 = ctrl.Rule(
                humedad_suelo['encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo[
                    'alta'],
                tiempo_riego['nada'])
            rule19 = ctrl.Rule(
                humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['baja'],
                tiempo_riego['nada'])
            rule20 = ctrl.Rule(
                humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo[
                    'media'],
                tiempo_riego['nada'])
            rule21 = ctrl.Rule(
                humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['alta'],
                tiempo_riego['nada'])
            rule22 = ctrl.Rule(
                humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo[
                    'baja'],
                tiempo_riego['nada'])
            rule23 = ctrl.Rule(
                humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo[
                    'media'],
                tiempo_riego['nada'])
            rule24 = ctrl.Rule(
                humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo[
                    'alta'],
                tiempo_riego['nada'])
            rule25 = ctrl.Rule(
                humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['baja'],
                tiempo_riego['nada'])
            rule26 = ctrl.Rule(
                humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo[
                    'media'],
                tiempo_riego['nada'])
            rule27 = ctrl.Rule(
                humedad_suelo['encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['alta'],
                tiempo_riego['nada'])
            rule28 = ctrl.Rule(
                humedad_suelo['semi_encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo[
                    'baja'], tiempo_riego['nada'])
            rule29 = ctrl.Rule(
                humedad_suelo['semi_encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo[
                    'media'], tiempo_riego['nada'])
            rule30 = ctrl.Rule(
                humedad_suelo['semi_encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo[
                    'alta'], tiempo_riego['nada'])
            rule31 = ctrl.Rule(
                humedad_suelo['semi_encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo[
                    'baja'], tiempo_riego['nada'])
            rule32 = ctrl.Rule(
                humedad_suelo['semi_encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo[
                    'media'], tiempo_riego['nada'])
            rule33 = ctrl.Rule(
                humedad_suelo['semi_encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo[
                    'alta'], tiempo_riego['nada'])
            rule34 = ctrl.Rule(
                humedad_suelo['semi_encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo[
                    'baja'], tiempo_riego['nada'])
            rule35 = ctrl.Rule(
                humedad_suelo['semi_encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo[
                    'media'], tiempo_riego['nada'])
            rule36 = ctrl.Rule(
                humedad_suelo['semi_encharcado'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo[
                    'alta'], tiempo_riego['nada'])
            rule37 = ctrl.Rule(
                humedad_suelo['semi_encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo[
                    'baja'], tiempo_riego['nada'])
            rule38 = ctrl.Rule(
                humedad_suelo['semi_encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo[
                    'media'], tiempo_riego['nada'])
            rule39 = ctrl.Rule(
                humedad_suelo['semi_encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo[
                    'alta'], tiempo_riego['poco'])
            rule40 = ctrl.Rule(
                humedad_suelo['semi_encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo[
                    'baja'], tiempo_riego['nada'])
            rule41 = ctrl.Rule(
                humedad_suelo['semi_encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo[
                    'media'], tiempo_riego['nada'])
            rule42 = ctrl.Rule(
                humedad_suelo['semi_encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo[
                    'alta'], tiempo_riego['nada'])
            rule43 = ctrl.Rule(
                humedad_suelo['semi_encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo[
                    'baja'], tiempo_riego['nada'])
            rule44 = ctrl.Rule(
                humedad_suelo['semi_encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo[
                    'media'], tiempo_riego['nada'])
            rule45 = ctrl.Rule(
                humedad_suelo['semi_encharcado'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo[
                    'alta'], tiempo_riego['nada'])
            rule46 = ctrl.Rule(
                humedad_suelo['semi_encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo[
                    'baja'], tiempo_riego['nada'])
            rule47 = ctrl.Rule(
                humedad_suelo['semi_encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo[
                    'media'], tiempo_riego['nada'])
            rule48 = ctrl.Rule(
                humedad_suelo['semi_encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo[
                    'alta'], tiempo_riego['medio'])
            rule49 = ctrl.Rule(
                humedad_suelo['semi_encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo[
                    'baja'], tiempo_riego['nada'])
            rule50 = ctrl.Rule(
                humedad_suelo['semi_encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo[
                    'media'], tiempo_riego['nada'])
            rule51 = ctrl.Rule(
                humedad_suelo['semi_encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo[
                    'alta'], tiempo_riego['poco'])
            rule52 = ctrl.Rule(
                humedad_suelo['semi_encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo[
                    'baja'], tiempo_riego['nada'])
            rule53 = ctrl.Rule(
                humedad_suelo['semi_encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo[
                    'media'], tiempo_riego['nada'])
            rule54 = ctrl.Rule(
                humedad_suelo['semi_encharcado'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo[
                    'alta'], tiempo_riego['nada'])
            rule55 = ctrl.Rule(
                humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['baja'],
                tiempo_riego['nada'])
            rule56 = ctrl.Rule(
                humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['media'],
                tiempo_riego['nada'])
            rule57 = ctrl.Rule(
                humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['alta'],
                tiempo_riego['poco'])
            rule58 = ctrl.Rule(
                humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo['baja'],
                tiempo_riego['nada'])
            rule59 = ctrl.Rule(
                humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo['media'],
                tiempo_riego['nada'])
            rule60 = ctrl.Rule(
                humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo['alta'],
                tiempo_riego['nada'])
            rule61 = ctrl.Rule(
                humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['baja'],
                tiempo_riego['nada'])
            rule62 = ctrl.Rule(
                humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['media'],
                tiempo_riego['nada'])
            rule63 = ctrl.Rule(
                humedad_suelo['humedo'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['alta'],
                tiempo_riego['nada'])
            rule64 = ctrl.Rule(
                humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo['baja'],
                tiempo_riego['nada'])
            rule65 = ctrl.Rule(
                humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo['media'],
                tiempo_riego['nada'])
            rule66 = ctrl.Rule(
                humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo['alta'],
                tiempo_riego['poco'])
            rule67 = ctrl.Rule(
                humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo['baja'],
                tiempo_riego['nada'])
            rule68 = ctrl.Rule(
                humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo['media'],
                tiempo_riego['nada'])
            rule69 = ctrl.Rule(
                humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo['alta'],
                tiempo_riego['poco'])
            rule70 = ctrl.Rule(
                humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo['baja'],
                tiempo_riego['nada'])
            rule71 = ctrl.Rule(
                humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo['media'],
                tiempo_riego['nada'])
            rule72 = ctrl.Rule(
                humedad_suelo['humedo'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo['alta'],
                tiempo_riego['nada'])
            rule73 = ctrl.Rule(
                humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['baja'],
                tiempo_riego['nada'])
            rule74 = ctrl.Rule(
                humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['media'],
                tiempo_riego['nada'])
            rule75 = ctrl.Rule(
                humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['alta'],
                tiempo_riego['medio'])
            rule76 = ctrl.Rule(
                humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo['baja'],
                tiempo_riego['nada'])
            rule77 = ctrl.Rule(
                humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo['media'],
                tiempo_riego['nada'])
            rule78 = ctrl.Rule(
                humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo['alta'],
                tiempo_riego['poco'])
            rule79 = ctrl.Rule(
                humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['baja'],
                tiempo_riego['nada'])
            rule80 = ctrl.Rule(
                humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['media'],
                tiempo_riego['nada'])
            rule81 = ctrl.Rule(
                humedad_suelo['humedo'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['alta'],
                tiempo_riego['poco'])
            rule82 = ctrl.Rule(
                humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['baja'],
                tiempo_riego['nada'])
            rule83 = ctrl.Rule(
                humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['media'],
                tiempo_riego['nada'])
            rule84 = ctrl.Rule(
                humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['alta'],
                tiempo_riego['poco'])
            rule85 = ctrl.Rule(
                humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo['baja'],
                tiempo_riego['nada'])
            rule86 = ctrl.Rule(
                humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo[
                    'media'],
                tiempo_riego['nada'])
            rule87 = ctrl.Rule(
                humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo['alta'],
                tiempo_riego['nada'])
            rule88 = ctrl.Rule(
                humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['baja'],
                tiempo_riego['nada'])
            rule89 = ctrl.Rule(
                humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['media'],
                tiempo_riego['nada'])
            rule90 = ctrl.Rule(
                humedad_suelo['semi_seco'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['alta'],
                tiempo_riego['nada'])
            rule91 = ctrl.Rule(
                humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo['baja'],
                tiempo_riego['nada'])
            rule92 = ctrl.Rule(
                humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo[
                    'media'],
                tiempo_riego['medio'])
            rule93 = ctrl.Rule(
                humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo['alta'],
                tiempo_riego['bastante'])
            rule94 = ctrl.Rule(
                humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo[
                    'baja'],
                tiempo_riego['nada'])
            rule95 = ctrl.Rule(
                humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo[
                    'media'],
                tiempo_riego['poco'])
            rule96 = ctrl.Rule(
                humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo[
                    'alta'],
                tiempo_riego['medio'])
            rule97 = ctrl.Rule(
                humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo['baja'],
                tiempo_riego['nada'])
            rule98 = ctrl.Rule(
                humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo[
                    'media'],
                tiempo_riego['nada'])
            rule99 = ctrl.Rule(
                humedad_suelo['semi_seco'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo['alta'],
                tiempo_riego['poco'])
            rule100 = ctrl.Rule(
                humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['baja'],
                tiempo_riego['poco'])
            rule101 = ctrl.Rule(
                humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['media'],
                tiempo_riego['medio'])
            rule102 = ctrl.Rule(
                humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['alta'],
                tiempo_riego['mucho'])
            rule103 = ctrl.Rule(
                humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo['baja'],
                tiempo_riego['poco'])
            rule104 = ctrl.Rule(
                humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo[
                    'media'],
                tiempo_riego['medio'])
            rule105 = ctrl.Rule(
                humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo['alta'],
                tiempo_riego['bastante'])
            rule106 = ctrl.Rule(
                humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['baja'],
                tiempo_riego['poco'])
            rule107 = ctrl.Rule(
                humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['media'],
                tiempo_riego['medio'])
            rule108 = ctrl.Rule(
                humedad_suelo['semi_seco'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['alta'],
                tiempo_riego['bastante'])
            rule109 = ctrl.Rule(
                humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['baja'],
                tiempo_riego['nada'])
            rule110 = ctrl.Rule(
                humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['media'],
                tiempo_riego['poco'])
            rule111 = ctrl.Rule(
                humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['baja'] & evapo['alta'],
                tiempo_riego['medio'])
            rule112 = ctrl.Rule(
                humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo['baja'],
                tiempo_riego['nada'])
            rule113 = ctrl.Rule(
                humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo['media'],
                tiempo_riego['poco'])
            rule114 = ctrl.Rule(
                humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['media'] & evapo['alta'],
                tiempo_riego['medio'])
            rule115 = ctrl.Rule(
                humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['baja'],
                tiempo_riego['nada'])
            rule116 = ctrl.Rule(
                humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['media'],
                tiempo_riego['nada'])
            rule117 = ctrl.Rule(
                humedad_suelo['seco'] & temperatura_ambiental['baja'] & humedad_ambiental['alta'] & evapo['alta'],
                tiempo_riego['poco'])
            rule118 = ctrl.Rule(
                humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo['baja'],
                tiempo_riego['medio'])
            rule119 = ctrl.Rule(
                humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo['media'],
                tiempo_riego['bastante'])
            rule120 = ctrl.Rule(
                humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['baja'] & evapo['alta'],
                tiempo_riego['mucho'])
            rule121 = ctrl.Rule(
                humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo['baja'],
                tiempo_riego['medio'])
            rule122 = ctrl.Rule(
                humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo['media'],
                tiempo_riego['bastante'])
            rule123 = ctrl.Rule(
                humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['media'] & evapo['alta'],
                tiempo_riego['mucho'])
            rule124 = ctrl.Rule(
                humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo['baja'],
                tiempo_riego['poco'])
            rule125 = ctrl.Rule(
                humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo['media'],
                tiempo_riego['medio'])
            rule126 = ctrl.Rule(
                humedad_suelo['seco'] & temperatura_ambiental['media'] & humedad_ambiental['alta'] & evapo['alta'],
                tiempo_riego['bastante'])
            rule127 = ctrl.Rule(
                humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['baja'],
                tiempo_riego['medio'])
            rule128 = ctrl.Rule(
                humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['media'],
                tiempo_riego['bastante'])
            rule129 = ctrl.Rule(
                humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['baja'] & evapo['alta'],
                tiempo_riego['mucho'])
            rule130 = ctrl.Rule(
                humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo['baja'],
                tiempo_riego['medio'])
            rule131 = ctrl.Rule(
                humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo['media'],
                tiempo_riego['bastante'])
            rule132 = ctrl.Rule(
                humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['media'] & evapo['alta'],
                tiempo_riego['mucho'])
            rule133 = ctrl.Rule(
                humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['baja'],
                tiempo_riego['medio'])
            rule134 = ctrl.Rule(
                humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['media'],
                tiempo_riego['bastante'])
            rule135 = ctrl.Rule(
                humedad_suelo['seco'] & temperatura_ambiental['alta'] & humedad_ambiental['alta'] & evapo['alta'],
                tiempo_riego['mucho'])

            cadena_reglas = [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12,
                             rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20, rule21, rule22, rule23,
                             rule24, rule25, rule26, rule27, rule28, rule29, rule30, rule31, rule32, rule33, rule34,
                             rule35, rule36, rule37, rule38, rule39, rule40, rule41, rule42, rule43, rule44, rule45,
                             rule46, rule47, rule48, rule49, rule50, rule51, rule52, rule53, rule54, rule55, rule56,
                             rule57, rule58, rule59, rule60, rule61, rule62, rule63, rule64, rule65, rule66, rule67,
                             rule68, rule69, rule70, rule71, rule72, rule73, rule74, rule75, rule76, rule77, rule78,
                             rule79, rule80, rule81, rule82, rule83, rule84, rule85, rule86, rule87, rule88, rule89,
                             rule90, rule91, rule92, rule93, rule94, rule95, rule96, rule97, rule98, rule99, rule100,
                             rule101, rule102, rule103, rule104, rule105, rule106, rule107, rule108, rule109, rule110,
                             rule111, rule112, rule113, rule114, rule115, rule116, rule117, rule118, rule119, rule120,
                             rule121, rule122, rule123, rule124, rule125, rule126, rule127, rule128, rule129, rule130,
                             rule131, rule132, rule133, rule134, rule135]

            tipping_ctrl = ctrl.ControlSystem(cadena_reglas)
            tipping = ctrl.ControlSystemSimulation(tipping_ctrl)
            tipping.input['humedad_suelo'] = par_humedad_suelo
            tipping.input['temperatura_ambiental'] = par_temperatura_ambiental
            tipping.input['humedad_ambiental'] = par_humedad_ambiental
            tipping.input['evapo'] = par_evapo
            tipping.compute()
            minutos_riego = tipping.output['tiempo_riego']
            if desea_grafica:
                grafica = tiempo_riego.view(sim=tipping)
                plt.savefig(self.ubicacion_imagen_fuzzy4() + id_historial_riego)
                plt.close(grafica)
            if minutos_riego > 0:
                return minutos_riego
            else:
                return 0
        except Exception:
            print("Fuera de rango: ", sys.exc_info()[1], ' humedad suelo:', par_humedad_suelo)
            print("Humd Ambiente: ", par_humedad_ambiental)
            print("Temp Ambiente: ", par_temperatura_ambiental)
            print("Evapotranspiracion: ", par_evapo)
            return 0;

    def ubicacion_imagen_fuzzy1(self):
        return imagen_fuzzy1

    def ubicacion_imagen_fuzzy3(self):
        return imagen_fuzzy3

    def ubicacion_imagen_fuzzy4(self):
        return imagen_fuzzy4


# Procesa datos de los sensores recolectados del dispositivo
class CalcularVariableEntrada:
    # Calcula el promedio de los sensores tanto de humedad del suelo, temperatura y humedad ambiental
    def calcular_promedio_sensor(self, fecha_desde, fecha_hasta, codigo_sensor, tipo_sensor):
        d_fecha_desde = datetime.strptime(fecha_desde, '%d/%m/%Y %H:%M:%S')
        d_fecha_hasta = datetime.strptime(fecha_hasta, '%d/%m/%Y %H:%M:%S')
        calcular_promedio = Sensor.objects.filter(fecha_registro__range=(d_fecha_desde, d_fecha_hasta),
                                                  codigo_sensor=codigo_sensor, tipo_sensor=tipo_sensor).aggregate(
            r=Coalesce(Avg('value'), 0)).get('r')

        return calcular_promedio

    # Funciona para obtener el valor máximo ya sea de humedad de suelo, temperatura y humedad ambiental
    def calcular_max_sensor(self, fecha_desde, fecha_hasta, codigo_sensor, tipo_sensor):
        d_fecha_desde = datetime.strptime(fecha_desde, '%d/%m/%Y %H:%M:%S')
        d_fecha_hasta = datetime.strptime(fecha_hasta, '%d/%m/%Y %H:%M:%S')
        calcular_max_sensor = Sensor.objects.filter(fecha_registro__range=(d_fecha_desde, d_fecha_hasta),
                                                    codigo_sensor=codigo_sensor, tipo_sensor=tipo_sensor).aggregate(
            r=Coalesce(Max('value'), 0)).get('r')

        return calcular_max_sensor

    # Funciona para obtener el valor mínimo de un sensor tanto de humedad de suelo, temperatura y humedad ambiental
    def calcular_min_sensor(self, fecha_desde, fecha_hasta, codigo_sensor, tipo_sensor):
        d_fecha_desde = datetime.strptime(fecha_desde, '%d/%m/%Y %H:%M:%S')
        d_fecha_hasta = datetime.strptime(fecha_hasta, '%d/%m/%Y %H:%M:%S')
        calcular_min_sensor = Sensor.objects.filter(fecha_registro__range=(d_fecha_desde, d_fecha_hasta),
                                                    codigo_sensor=codigo_sensor, tipo_sensor=tipo_sensor).aggregate(
            r=Coalesce(Min('value'), 0)).get('r')

        return calcular_min_sensor

    # Funcion para la obtencion de la evapotranspiracion. Fuente: https://hidrologia.usal.es/temas/Evapotransp.pdf
    def calcular_evapotranspiracion(self, R0, tmed, tdmax, tdmin):
        et0 = 0.0023 * (tmed + 17.78) * (R0) * (tdmax - tdmin) ** (0.5)
        return et0

# Para realizar pruebas esta clase, descomentar.
# fuzzy = LogicaDifusa()
# fuzzy.fuzzy_logic_1_variables_image(234.5, '10000')
