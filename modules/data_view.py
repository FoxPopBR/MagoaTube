# data_view.py
import tkinter as tk
from tkinter import ttk
from .path_tree import root_path, database_path

class SeuApp(tk.Tk):
    def __init__(self, parent):
        #super().__init__()
        self.main_frame = ttk.Frame(parent)
        self.main_frame.grid(sticky='nsew')
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        self.create_widgets(self.main_frame)

    def create_widgets(self, frame):
        self.widgets = {}
        # Configuração customizada para cada campo
        fields_config = {
            #Video info
            'video_id': {'width': 7, 'height': 1, 'row': 0, 'column': 0},
            'url': {'width': 25, 'height': 1, 'row': 0, 'column': 1},
            'Titulo': {'width': 30, 'height': 1, 'row': 0, 'column': 2,'columnspan': 4},
            # Video progressive
            'Audio_e_Video': {'width': 15, 'height': 1, 'row': 0, 'column': 6},
            'file_extension.': {'width': 5, 'height': 1, 'row': 0, 'column': 7},
            'file_size.': {'width': 8, 'height': 1, 'row': 0, 'column': 8},
            'download_url.': {'width': 10, 'height': 1, 'row': 0, 'column': 9, 'columnspan': 2},
            'codec.': {'width': 10, 'height': 1, 'row': 0, 'column': 11},
            #'resolution.': {'width': 10, 'height': 1, 'row': 4, 'column': 2, 'columnspan': 2},
            #'fps.': {'width': 5, 'height': 1, 'row': 4, 'column': 4},

            # Audio adaptative
            'Audio_Qualit': {'width': 5, 'height': 1, 'row': 4, 'column': 0},
            'Audio': {'width': 15, 'height': 1, 'row': 4, 'column': 1},
            'extension_Audio': {'width': 5, 'height': 1, 'row': 4, 'column': 2},
            'codec_audio': {'width': 10, 'height': 1, 'row': 6, 'column': 0},
            'size_audio': {'width': 10, 'height': 1, 'row': 6, 'column': 2},
            'download Audio': {'width': 15, 'height': 1, 'row': 6, 'column': 1},


            # Video adaptative
            'Video': {'width': 10, 'height': 1, 'row': 4, 'column': 7, 'columnspan': 2},
            'resolution': {'width': 10, 'height': 1, 'row': 4, 'column': 10},
            'fps': {'width': 5, 'height': 1, 'row': 4, 'column': 9},
            'size_video': {'width': 5, 'height': 1, 'row': 6, 'column': 10},
            'extension_Video': {'width': 5, 'height': 1, 'row': 4, 'column': 11},
            'codec_video': {'width': 10, 'height': 1, 'row': 6, 'column': 11},
            'download_Video': {'width': 15, 'height': 1, 'row': 6, 'column': 7, 'columnspan': 3},


            #Painel Descrição e Thumbnail+
            'descricao': {'width': 25, 'height': 15, 'row': 12, 'column': 0, 'rowspan':5, 'columnspan': 3},
            'thumb': {'width': 25, 'height': 15, 'row': 12, 'column': 7, 'rowspan': 4, 'columnspan': 5}

            #'audio_quality': {'width': 5, 'height': 1, 'row': 6, 'column': 13}
        }
        style = ttk.Style()
        style.configure('DataView.TLabel', font=('Helvetica', 8))

        # Espaçadores
        space1 = ttk.Frame(frame, height=50, width=500)  # Ajuste 'height' e 'width' conforme necessário
        space1.grid(row=2, column=0, columnspan=12)  # Ajuste 'row' e 'column' para posicionar o espaçador

        space2 = ttk.Frame(frame, height=50, width=500)  # Ajuste 'height' e 'width' conforme necessário
        space2.grid(row=10, column=0, columnspan=12)  # Ajuste 'row' e 'column' para posicionar o espaçador

        for field, config in fields_config.items():
            label = ttk.Label(frame, text=field.replace('_', ' ').capitalize() + ":", style='DataView.TLabel')
            label.grid(row=config['row'], column=config['column'], sticky='w', pady=2, padx=10)

            if config['height'] == 1:
                text_widget = ttk.Entry(frame, font=('Helvetica', 9), width=config['width'])
            else:
                text_widget = tk.Text(frame, height=config['height'], width=config['width'], font=('Helvetica', 8))

            # Definindo valores padrão para rowspan e columnspan
            rowspan = config.get('rowspan', 1)
            columnspan = config.get('columnspan', 1)

            text_widget.grid(row=config['row']+1, column=config['column'], rowspan=rowspan, columnspan=columnspan, sticky='nsew', pady=2, padx=5)
            self.widgets[field] = text_widget

    def atualizar_widgets(self, dados):
        for chave, valor in dados.items():
            if chave in self.widgets:
                widget = self.widgets[chave]
                if isinstance(widget, ttk.Entry):
                    widget.delete(0, tk.END)
                    widget.insert(0, valor)
                elif isinstance(widget, tk.Text):
                    widget.delete("1.0", tk.END)
                    widget.insert("1.0", valor)
