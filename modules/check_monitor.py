
from screeninfo import get_monitors

class Check_Screen():
    def __init__(self):
        self.check_monitor = get_monitors()  # Obtém a lista de monitoras disponíveis
        self.uni_monitor = len(self.check_monitor)  # Obtém o número de monitoras disponíveis

    def update_monitor(self):
        # Variáveis para armazenar as resoluções dos monitores
        self.monitor_detect = self.uni_monitor  # Salva quantos monitores foram detectados
        self.monitor_A = None
        self.monitor_B = None
        self.monitor_C = None
        self.monitor_D = None
        self.center_A = None
        sec_monitor_count = 0  # Inicializa a contagem dos monitores secundários
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