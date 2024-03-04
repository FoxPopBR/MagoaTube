import tkinter as tk
from tkinter import messagebox
import yt_dlp as youtube_dl
import subprocess
import os
import sys
import threading

# Configuração do logging removida para brevidade

import sys

def find_vlc_path():
    # Obtém o diretório do executável em execução
    exe_dir = os.path.dirname(sys.argv[0])
    vlc_folder = "vlc"
    vlc_path = os.path.join(exe_dir, vlc_folder, "vlc-portable.exe")
    if os.path.isfile(vlc_path):
        print("VLC encontrado: " + vlc_path)
        return vlc_path
    # Se a pasta do VLC não for encontrada, exibe uma mensagem de aviso
    messagebox.showwarning("Aviso", "Pasta do VLC não encontrada. Por favor, verifique se o VLC está instalado.")
    return None



def play_youtube_video(url):
    try:
        with youtube_dl.YoutubeDL({'noplaylist': True, 'format': 'best'}) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_url = info_dict.get('url', None)
            video_title = info_dict.get('title', 'Vídeo do YouTube')  # Obtém o título do vídeo, se disponível

        vlc_path = find_vlc_path()
        if vlc_path:
            # Inicia a reprodução do vídeo em uma nova thread
            thread = threading.Thread(target=play_video_threaded, args=(vlc_path, video_url, video_title))
            thread.start()
    except Exception as e:
        messagebox.showerror("Erro", "Houve um problema ao reproduzir o vídeo. Verifique o log para mais detalhes.")

def play_video_threaded(vlc_path, video_url, video_title):
    try:
        subprocess.call([vlc_path, video_url, '--meta-title', video_title])
    except Exception as e:
        messagebox.showerror("Erro", "Houve um problema ao reproduzir o vídeo. Verifique o log para mais detalhes.")

def on_submit():
    url = url_entry.get()
    play_youtube_video(url)

# Cria a janela principal
root = tk.Tk()
root.geometry("720x480")
root.title("Reproduzir Vídeo do YouTube")

# Cria um campo de entrada para a URL
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=20)

# Cria um botão para enviar a URL
submit_btn = tk.Button(root, text="Enviar", command=on_submit)
submit_btn.pack(pady=10)

root.mainloop()
