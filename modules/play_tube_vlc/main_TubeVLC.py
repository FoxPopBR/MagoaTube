import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import yt_dlp as youtube_dl
import subprocess
import os
import threading

def get_video_resolutions(url):
    if not url:
        messagebox.showerror("Erro", "Por favor, insira uma URL antes de verificar.")
        return []
    try:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'quiet': True,
            'noplaylist': True,
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(url, download=False)
            formats = meta.get('formats', [meta])
        progressive_formats = [f"{fmt['format_id']} - {fmt['resolution']}" for fmt in formats if fmt.get('acodec') != 'none' and fmt.get('vcodec') != 'none']
        return progressive_formats
    except Exception as e:
        messagebox.showerror("Erro", "Falha ao obter resoluções: " + str(e))
        return []

def find_vlc_path():
    exe_dir = os.path.dirname(os.path.abspath(__file__))
    vlc_path = os.path.join(exe_dir, "vlc", "vlc-portable.exe")
    if os.path.isfile(vlc_path):
        return vlc_path
    messagebox.showwarning("Aviso", "Pasta do VLC não encontrada. Por favor, verifique se o VLC está instalado.")
    return None

def play_youtube_video(url, format_id):
    if not url or not format_id:
        messagebox.showerror("Erro", "Por favor, selecione uma URL e uma resolução antes de enviar.")
        return
    vlc_path = find_vlc_path()
    if vlc_path:
        ydl_opts = {
            'format': format_id,
            'quiet': True,
            'noplaylist': True,
            'outtmpl': '%(title)s.%(ext)s',
            'merge_output_format': 'mkv'
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_url = info_dict.get('url', None)
            video_title = info_dict.get('title', None)
        thread = threading.Thread(target=play_video_threaded, args=(vlc_path, video_url, video_title))
        thread.start()

def play_video_threaded(vlc_path, video_url, video_title):
    try:
        subprocess.call([vlc_path, video_url, '--meta-title', video_title])
    except Exception as e:
        messagebox.showerror("Erro", "Houve um problema ao reproduzir o vídeo: " + str(e))

def on_submit():
    if not url_entry.get() or not box_video_resolution.get():
        messagebox.showerror("Erro", "Por favor, insira uma URL e selecione uma resolução antes de enviar.")
        return
    selected_format = box_video_resolution.get().split(' - ')[0]
    play_youtube_video(url_entry.get(), selected_format)

def url_check():
    url = url_entry.get()
    resolutions = get_video_resolutions(url)
    if resolutions:
        box_video_resolution['values'] = resolutions
        box_video_resolution.current(0)

# Código a baixo para testes! Esse é um arquivo de Módulo e não será executado diretamente.
root = tk.Tk()
root.geometry("720x480")
root.title("Reproduzir Vídeo do YouTube")

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=20)

check_url = tk.Button(root, text="check url", command=url_check)
check_url.place(x=550, y=12)

submit_btn = tk.Button(root, text="Enviar", command=on_submit)
submit_btn.pack(pady=10)

box_video_resolution = ttk.Combobox(root, width=50, state="readonly")
box_video_resolution.pack(pady=10)

root.mainloop()
