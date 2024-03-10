#main_screen.py
import tkinter as tk
from tkinter import ttk
import importlib
from screeninfo import get_monitors
from modules.check_monitor import Check_Screen
from modules.manager_db import DatabaseManager
from modules.data_video import extract_video_info
import modules.data_view as data_view
from tkinter import messagebox
from modules.path_tree import root_path, database_path

class Magoa(tk.Tk):
    def __init__(self, check_screen, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Inicializa a classe base tk.Tk
        self.check_screen = check_screen  # Chama a função de captura Obs: Sem uso no momento
        self.list_themes = ["winnative", "clam", "alt", "default", "classic", "vista", "xpnative"]
        self.selected_theme = self.list_themes[0]
        self.style = ttk.Style()
        self.url_input_bar = tk.StringVar()
        self.extract_video_info = extract_video_info # Chama a função de processamento de ví
        self.app_data_view_active = False
        self.db_manager = DatabaseManager(database_path)

    def select_url_main(self):
        url_input = self.url_input_bar.get().strip()
        self.button_detalhes()
        if not url_input:
            messagebox.showerror("Erro", "URL do vídeo não informada.")
            return
        # Chama process_video_info para processar a URL. Esta função agora deverá
        # lidar com todas as verificações e inserções necessárias.
        video_id = self.extract_video_info(url_input)  # Mantém apenas esta chamada
        self.atualizar_combobox_titulos()
        if video_id is None:
            messagebox.showerror("Erro", "Não foi possível processar o vídeo. Verifique se a URL é válida.")
        #else:
            #messagebox.showinfo("Sucesso", f"Vídeo processado com sucesso. ID do Vídeo: {video_id}")

    def atualizar_combobox_titulos(self):
        videos = self.db_manager.buscar_titulos_e_ids_videos()
        # Atualização para usar títulos como texto e ids como valores internos do combobox
        self.combobox_resolution_main['values'] = [video['title'] for video in videos]
        if videos:
            self.combobox_resolution_main.current(0)

    def combobox_selection_event(self, event=None):
        selected_index = self.combobox_resolution_main.current()  # Obtém o índice selecionado
        videos = self.db_manager.buscar_titulos_e_ids_videos()  # Busca novamente os dados para sincronizar com o índice
        if videos and 0 <= selected_index < len(videos):
            selected_video_id = videos[selected_index]['id']
            # Agora você tem o ID do vídeo selecionado e pode utilizá-lo conforme necessário
            video_info = self.db_manager.buscar_informacoes_video_pelo_titulo(videos[selected_index]['title'])  # Método a ser implementado
            #stream_progressive = self.db_manager.buscar_informacoes_video_pelo_titulo*(progressive_streams[selected_index]['title'])
            self.update_video_details_ui(video_info)  # Este método já deve estar implementado para atualizar a UI com as informações do vídeo

    def limpar_widget(self, nome_widget, tipo):
        if tipo == 'entry':
            self.app_data_view.widgets[nome_widget].delete(0, tk.END)
        elif tipo == 'text':
            self.app_data_view.widgets[nome_widget].delete("1.0", tk.END)

    def update_video_details_ui(self, video_info):
        if hasattr(self, 'app_data_view') and video_info:
            # Atualiza os widgets de entrada de texto com informações do vídeo
            # Exemplo de atualização direta para alguns campos, ajuste conforme necessário
            if 'id' in video_info:
                self.limpar_widget('video_id', 'entry')
                self.app_data_view.widgets['video_id'].insert(0, video_info['id'])

            if 'url' in video_info:
                self.limpar_widget('url', 'entry')
                self.app_data_view.widgets['url'].insert(0, video_info['url'])

            if 'title' in video_info:
                self.limpar_widget('Titulo', 'entry')
                self.app_data_view.widgets['Titulo'].insert(0, video_info['title'])

            if 'description' in video_info:
                self.limpar_widget('descricao', 'text')
                self.app_data_view.widgets['descricao'].insert("1.0", video_info['description'])
            # Continue para outros campos conforme necessário

    def show_video_info(self, video_info):
        if hasattr(self, 'app_data_view'):
            campos_simples = {
                'id': ('video_id', 'entry'),
                'url': ('url', 'entry'),
                'title': ('Titulo', 'entry'),
                'description': ('descricao', 'text'),
                'Audio_e_Video': ('resolução', 'text'),
                'file_extension.': ('file_extension', 'text'),
                'file_size.': ('file_size', 'entry'),
                'download_url.': ('download_url', 'text'),
                # Campos adicionados com base nos arquivos de código
                'codec.': ('codec', 'text'),  # Presente em streams progressivos e adaptativos
                'Audio_Qualit': ('audio_quality', 'text'),  # Qualidade de áudio para streams adaptativos
                'Audio': ('audio', 'entry'),  # Identificador genérico para campos de áudio
                'extension_Audio': ('extension_audio', 'text'),  # Extensão de arquivo para áudio
                'codec_audio': ('codec_audio', 'text'),  # Codec usado para áudio
                'size_audio': ('size_audio', 'entry'),  # Tamanho do arquivo de áudio
                'download Audio': ('download_audio_url', 'text'),  # URL para download de áudio
                'Video': ('video', 'entry'),  # Identificador genérico para campos de vídeo
                'resolution': ('resolution', 'text'),  # Resolução para vídeo
                'fps': ('fps', 'entry'),  # Frames por segundo
                'size_video': ('size_video', 'entry'),  # Tamanho do arquivo de vídeo
                'extension_Video': ('extension_video', 'text'),  # Extensão de arquivo para vídeo
                'codec_video': ('codec_video', 'text'),  # Codec usado para vídeo
                'download Video': ('download_video_url', 'text'),  # URL para download de vídeo
                'thumb': ('thumbnail_url', 'text'),  # URL da miniatura do vídeo
    }
            # Exemplo de como atualizar widgets para streams progressivos e adaptativos
            # Esta seção precisa ser adaptada conforme a estrutura dos seus dados
            if 'progressive_streams' in video_info and video_info['progressive_streams']:
                stream = video_info['progressive_streams'][0]  # Exemplo: usar o primeiro stream
                self.app_data_view.widgets['Audio e Video'].delete(0, tk.END)
                self.app_data_view.widgets['Audio e Video'].insert(0, stream.get('codec'))

                self.app_data_view.widgets['file_extension.'].delete(0, tk.END)
                self.app_data_view.widgets['file_extension.'].insert(0, stream.get('file_extension'))

                self.app_data_view.widgets['file_size.'].delete(0, tk.END)
                self.app_data_view.widgets['file_size.'].insert(0, stream.get('file_size'))

                self.app_data_view.widgets['download_url.'].delete(0, tk.END)
                self.app_data_view.widgets['download_url.'].insert(0, stream.get('download_url'))

            # Exemplo para streams adaptativos
            if 'adaptive_streams' in video_info and video_info['adaptive_streams']:
                audio_stream = video_info['adaptive_streams']['audio'][0]  # Exemplo: usar o primeiro stream de áudio
                video_stream = video_info['adaptive_streams']['video'][0]  # Exemplo: usar o primeiro stream de vídeo

                self.app_data_view.widgets['Audio'].delete(0, tk.END)
                self.app_data_view.widgets['Audio'].insert(0, audio_stream.get('codec_audio'))

                self.app_data_view.widgets['extension_Audio'].delete(0, tk.END)
                self.app_data_view.widgets['extension_Audio'].insert(0, audio_stream.get('file_extension'))

                self.app_data_view.widgets['size_audio'].delete(0, tk.END)
                self.app_data_view.widgets['size_audio'].insert(0, audio_stream.get('file_size'))

                self.app_data_view.widgets['download Audio'].delete(0, tk.END)
                self.app_data_view.widgets['download Audio'].insert(0, audio_stream.get('download_url'))

                self.app_data_view.widgets['Video'].delete(0, tk.END)
                self.app_data_view.widgets['Video'].insert(0, video_stream.get('codec_video'))

                self.app_data_view.widgets['resolution'].delete(0, tk.END)
                self.app_data_view.widgets['resolution'].insert(0, video_stream.get('resolution'))

                self.app_data_view.widgets['fps'].delete(0, tk.END)
                self.app_data_view.widgets['fps'].insert(0, video_stream.get('fps'))

                self.app_data_view.widgets['size_video'].delete(0, tk.END)
                self.app_data_view.widgets['size_video'].insert(0, video_stream.get('file_size'))

                self.app_data_view.widgets['extension_Video'].delete(0, tk.END)
                self.app_data_view.widgets['extension_Video'].insert(0, video_stream.get('file_extension'))

                self.app_data_view.widgets['download Video'].delete(0, tk.END)
                self.app_data_view.widgets['download Video'].insert(0, video_stream.get('download_url'))

            # Atualização de Thumbnail
            if 'thumbnails' in video_info and video_info['thumbnails']:
                # Exemplo: usar a URL da primeira miniatura disponível
                thumb_url = video_info['thumbnails'][0].get('url')
                self.app_data_view.widgets['thumb'].delete(0, tk.END)
                self.app_data_view.widgets['thumb'].insert(0, thumb_url)

        else:
            print("app_data_view não está disponível.")

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
        self.main_frame = ttk.Frame(self, borderwidth=2, relief="groove")
        self.main_frame.grid(sticky="nsew")

        # -------------------- / BOX Frames Inicio / ------------------------
        # --> "Frame Principal" para adicionar os widgets
        # Definir a grade principal para redimensionar com a janela
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Frame principal que contém todos os outros frames
        #self.main_frame = ttk.Frame(self, borderwidth=2, relief="groove")
        #self.main_frame.grid(sticky="nsew")
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
        self.url_input_bar = ttk.Entry(self.superior_bar_frame, textvariable=self.url_input_bar, width=100)
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
        self.combobox_resolution_main = ttk.Combobox(self.superior_bar_frame, textvariable=self.atualizar_combobox_titulos, width=28, state="readonly")
        self.combobox_resolution_main.grid(row=0, column=3, sticky="nsew", padx=50,pady=4)
        self.atualizar_combobox_titulos()
        self.combobox_resolution_main.bind("<<ComboboxSelected>>", self.combobox_selection_event)

        # -------------------- / Frame Borda Superior Url - Fim / ---------------------------

        # -------------------- / Frame Principal Inicio / ------------------------
        # Adicionar Botão Player VLC TELA
        self.button_play_vlc = ttk.Button(self.control_buttons_frame, text="Play VLC", style="Large.TButton", command=self.play_vlc_video)
        self.button_play_vlc.pack(side="left", padx=50, pady=0)

        # Adicionar Botão Player VLC TELA
        self.button_playnow = ttk.Button(self.control_buttons_frame, text="Play Now", style="Large.TButton", command=self.play_vlc_video)
        self.button_playnow.pack(side="left", padx=125, pady=0)

        # Adicionar Botão Player VLC TELA
        self.button_details = ttk.Button(self.control_buttons_frame, text="Detalhes", style="Large.TButton", command=self.button_detalhes)
        self.button_details.pack(side="right", padx=50, pady=0)

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

    def button_detalhes(self):
        # Primeiro, limpe o frame de reserva para remover widgets existentes
        for widget in self.reserve_area_frame.winfo_children():
            widget.destroy()
        # Recarregar o módulo para aplicar as mudanças
        importlib.reload(data_view)
        # Cria a nova instância de SeuApp dentro do frame limpo com o código atualizado
        self.app_data_view = data_view.SeuApp(self.reserve_area_frame)

    def on_combobox_select(self, event):
        selected_title = self.combobox_resolution_main.get()
        video_info = self.db_manager.buscar_informacoes_video_pelo_titulo(selected_title)
        if video_info:
            self.atualizar_ui_com_info_video(video_info)

    def change_theme(self, event):
        selected_theme = self.combobox_theme.get()
        ttk.Style().theme_use(selected_theme)

    def play_vlc_video(self):
        # Obter o valor atual da variável de controle url_input_bar
        url_atual = self.url_input_bar.get()
        # Primeiro, limpa o conteúdo existente do widget 'url'
        self.app_data_view.widgets['url'].delete(0, tk.END)
        # Em seguida, insere o valor obtido no widget 'url'
        self.app_data_view.widgets['url'].insert(0, url_atual)
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
