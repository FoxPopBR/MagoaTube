#main_screen.py
import tkinter as tk
from tkinter import ttk
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

class Magoa(tk.Tk):
    def __init__(self, check_screen):
        super().__init__()  # Inicializa a classe base tk.Tk
        self.check_screen = check_screen  # Chama a função de captura Obs: Sem uso no momento
        #self.main_ui()  # Chama a função de configuração da UI principal
    # main_ui é a função responsável pela configuração da janela principal
    def main_ui(self):
        #self.check_screen.update_monitor()
        x_pos, y_pos = self.check_screen.monitor_A  # Obtém as posições do monitor A
        x_win, y_win = 1280, 720  # Obtém as dimensões da janela principal
        x_center = int((x_pos / 2) - (x_win / 2))
        y_center = int((y_pos / 2) - (y_win / 2))  # Obtém as posição do centro da janela principal
        self.title("MagoaTube")  # Define o título da janela
        self.geometry(f"{x_win}x{y_win}+{x_center}+{y_center}")  # Define o tamanho da janela para 1280x720 pixels

        # Cria um Frame principal para adicionar os widgets
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)  # Faz com que o frame ocupe toda a janela

        ttk.Style().theme_use("plastik")
        style = ttk.Style()
        style.configure("New.TButton", foreground="blue", background="white", font=("Arial", 12, "bold"))
        # Adiciona um botão ao Frame principal
        self.button = ttk.Button(self.main_frame, text="Fechar Tudo", style="New.TButton", command=self.exit_main)
        self.button.pack(side="bottom", pady=50)  # Adiciona o botão ao frame com um pouco de espaço vertical

    # fechar aplicativo botão Sair
    def exit_main(self):
        self.destroy()  # Fecha a aplicação
        print("Fechando...")  # Ação ao clicar no botão
