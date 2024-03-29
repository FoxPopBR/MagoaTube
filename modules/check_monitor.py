
from screeninfo import get_monitors
import sys
import os

# Encontra a pasta raiz do arquivo em execução
def find_path_main():

    find_path = os.path.abspath(sys.argv[0])
    print("find_path ",find_path)

    root_path = os.path.dirname(find_path)
    print ("root_path",root_path)

# Configurações de monitores e resoluções encontradas, salvas em variáveis.
class Check_Screen():
    def __init__(self):
        self.check_monitor = get_monitors()  # Obtém a lista de monitoras disponíveis
        self.uni_monitor = len(self.check_monitor)  # Conta o número de monitoras disponíveis

    def update_monitor(self):
        # Variáveis para armazenar as resoluções dos monitores
        self.monitor_detect = self.uni_monitor  # Salva quantos monitores foram detectados
        self.monitor_A = None   # Monitor A sempre é o monitor principal detectado
        self.monitor_B = None
        self.monitor_C = None
        self.monitor_D = None
        self.center_A = None
        sec_monitor_count = 0  # Variável que armazena a quantidade de monitoras detectadas
        #Inicia verificação de monitores disponíveis, e salva resoluções dos monitor
        for monitor in self.check_monitor:
            if monitor.is_primary:
                self.monitor_A = (monitor.width, monitor.height)
            else:
                if sec_monitor_count == 0:
                    self.monitor_B = (monitor.width, monitor.height)
                elif sec_monitor_count == 1:
                    self.monitor_C = (monitor.width, monitor.height)
                elif sec_monitor_count == 2:
                    self.monitor_D = (monitor.width, monitor.height)

        # confirmação de saida
        print("Monitores detectados: ", self.uni_monitor)
        print("Monitor A: ", self.monitor_A)
        if self.monitor_B != None:
            print("Monitor B: ", self.monitor_B)
        if self.monitor_C!= None:
            print("Monitor C: ", self.monitor_C)
        if self.monitor_D!= None:
            print("Monitor D: ", self.monitor_D)
