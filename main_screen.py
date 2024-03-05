#main_screen.py
import tkinter as tk
from tkinter import ttk
from screeninfo import get_monitors
from modules.check_monitor import Check_Screen

class Magoa(tk.Tk):
    def __init__(self, check_screen):
        super().__init__()  # Inicializa a classe base tk.Tk
        self.check_screen = check_screen  # Chama a função de captura Obs: Sem uso no momento
        self.list_themes = ["winnative", "clam", "alt", "default", "classic", "vista", "xpnative"]
        self.selected_theme = self.list_themes[0]
        self.style = ttk.Style()

    # Configuração da janela principal
    def main_ui(self):
        # Configuração da janela principal
        ttk.Style().theme_use(self.selected_theme) # Seleciona o tema do aplicativo
        # Centralização da janela principal no monitor principal
        x_pos, y_pos = self.check_screen.monitor_A  # Obtém as posições do monitor A
        x_win, y_win = 1280, 720  # Obtém as dimensões da janela principal
        x_center = int((x_pos / 2) - (x_win / 2))
        y_center = int((y_pos / 2) - (y_win / 2))  # Obtém as posição do centro da janela principal
        self.title("MagoaTube")  # Define o título da janela
        self.geometry(f"{x_win}x{y_win}+{x_center}+{y_center}")  # Define posição da janela principal no centro do monitor principal
        self.url_input_main = tk.StringVar()

        # -------------------- / BOX Frames Inicio / ------------------------
        # --> "Frame Principal" para adicionar os widgets
        # Definir a grade principal para redimensionar com a janela
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Frame principal que contém todos os outros frames
        self.main_frame = ttk.Frame(self, borderwidth=2, relief="groove")
        self.main_frame.grid(sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Definir as proporções de redimensionamento dos frames Levando em conta a resolução do tamanho da janela principal
        self.main_frame.grid_rowconfigure(0, minsize=42) # Define a largura mínima da linha 0 do grid 
        self.main_frame.grid_rowconfigure(1, minsize=588)  # Define a largura mínima da linha 1 do grid
        self.main_frame.grid_rowconfigure(2, minsize=50)  # Define o tamanho mínimo da linha 2 do grid
        self.main_frame.grid_rowconfigure(3, minsize=40)  # Define o tamanho mínimo da linha 3 do grid

        # Frame superior para o menu URL
        self.superior_bar_frame = ttk.Frame(self.main_frame, height=50, borderwidth=2, relief="groove",)
        self.superior_bar_frame.grid(row=0, column=0, sticky="nsew")

        # Frame de área de reserva
        self.reserve_area_frame = ttk.Frame(self.main_frame, borderwidth=2, relief="groove")
        self.reserve_area_frame.grid(row=1, column=0, sticky="nsew")

        # Frame de botões de controle
        self.control_buttons_frame = ttk.Frame(self.main_frame, height=50, borderwidth=2, relief="groove")
        self.control_buttons_frame.grid(row=2, column=0, sticky="nsew")

        # Frame de status bar inferior
        self.lower_stats_frame = ttk.Frame(self.main_frame, height=50, borderwidth=2, relief="groove")
        self.lower_stats_frame.grid(row=3, column=0, sticky="nsew")
        # -------------------- / Box Frames Fim / ---------------------------

        # -------------------- / Frame Borda Superior Url - Inicio / ------------------------
        # Input do URL do vídeo
        self.url_input_bar = ttk.Entry(self.superior_bar_frame, textvariable=self.url_input_main, width=100)
        self.url_input_bar.grid(row=0, column=0, sticky="nsew",pady=4)

        # Label do url visível ou não
        self.url_input_bar.bind("<FocusIn>", self.handle_focus_in)
        self.url_input_bar.bind("<FocusOut>", self.handle_focus_out)

        # Posicionamento inicial da label que indica que o campo está vazio.
        self.empty_url_label = ttk.Label(self.url_input_bar, text="Insira o URL aqui", font="arial 9", background="white", foreground="gray")
        self.empty_url_label.place(x=2, y=3)
        self.empty_url_label.bind("<Button-1>", lambda event: self.url_input_bar.focus()) # ao clicar na label seleciona o input a baixo

        # Botão Select Url
        self.button_select_url_main = ttk.Button(self.superior_bar_frame, text="Select", style="TButton", command=self.select_url_main,width=9)
        self.button_select_url_main.grid(row=0, column=1, sticky="nsew", padx=5,pady=4)

        # Combobox select resolução do vídeo
        self.combobox_resolution_main = ttk.Combobox(self.superior_bar_frame, textvariable=self.url_input_main, width=28, state="readonly")
        self.combobox_resolution_main.grid(row=0, column=3, sticky="nsew", padx=50,pady=4)
        # -------------------- / Frame Borda Superior Url - Fim / ---------------------------

        # -------------------- / Frame Principal Inicio / ------------------------
        # Adicionar Botão Player VLC TELA
        self.button_play_vlc = ttk.Button(self.control_buttons_frame, text="Play VLC", style="Large.TButton", command=self.play_vlc_video)
        self.button_play_vlc.pack(side="left", padx=50, pady=0)

        # Adicionar Botão Player VLC TELA
        self.button_playnow = ttk.Button(self.control_buttons_frame, text="Play Now", style="Large.TButton", command=self.play_vlc_video)
        self.button_playnow.pack(side="left", padx=125, pady=0)

        # Adicionar Botão Player VLC TELA
        self.button_novo = ttk.Button(self.control_buttons_frame, text="Novo", style="Large.TButton", command=self.play_vlc_video)
        self.button_novo.pack(side="right", padx=50, pady=0)

        # Adicionar Botão Player VLC TELA
        self.button_downloader = ttk.Button(self.control_buttons_frame, text="Downloader", style="Large.TButton", command=self.play_vlc_video)
        self.button_downloader.pack(side="right", padx=125, pady=0)
        # -------------------- / Frame Principal Fim / ---------------------------

        # -------------------- / Frame Status Bar - Inicio / ------------------------
        # Criando o texto Combobox para selecionar o tema do aplicativo
        label_text = ttk.Label(self.lower_stats_frame, text="Escolha um tema")
        label_text.place(x=1033, y=3)  # Coloca o texto acima do Combobox com um pequeno espaço superior

        # Combobox para selecionar o tema do aplicativo
        self.combobox_theme = ttk.Combobox(self.lower_stats_frame, values=self.list_themes, state="readonly", width=12, justify='center', style='TCombobox')
        self.combobox_theme.place(x=1140,y=1)
        self.combobox_theme.current(0)  # Definindo o primeiro tema da lista como o tema atual
        self.combobox_theme.bind("<<ComboboxSelected>>", self.change_theme)

        # Configuração dos botões
        self.style.configure('Large.TButton', font=('Adobe Fan Heiti Sts Seminegrito', 12, 'normal'))  # Configura

        # Adiciona um Botão SAIR ao Frame principal
        self.button = ttk.Button(self.lower_stats_frame, text="Fechar Tudo", style="TButton", command=self.exit_main)
        self.button.pack(side="top", padx=5, pady=3)
        # -------------------- / Frame Status Bar - Fim/ ---------------------------

    def select_url_main(self):
        print("Chamada Botão Select Url")

    def change_theme(self, event):
        selected_theme = self.combobox_theme.get()
        ttk.Style().theme_use(selected_theme)

    def play_vlc_video(self):
        print("Chamando Painel Player VLC TELA")

    # fechar aplicativo botão Sair
    def exit_main(self):
        self.destroy()  # Fecha a aplicação
        print("Fechando...")  # Ação ao clicar no botão

    # Função para verificar e atualizar a visibilidade do label
    def handle_focus_in(self, event):
        # A label é ocultada quando o campo está selecionado.
        self.empty_url_label.place_forget()

    def handle_focus_out(self, event):
        # Se o campo estiver vazio após perder o foco, a label é mostrada.
        if not self.url_input_bar.get().strip():
            self.empty_url_label.place(x=2, y=4)
        else:
            self.empty_url_label.place_forget()
