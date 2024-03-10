import tkinter as tk
from tkinter import ttk
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
from pytube import Playlist
import re
import threading

def process_video(video_id, selected_language, title):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[selected_language])
        save_transcript(transcript, title, True, selected_language)
        save_transcript(transcript, f"{title}-Sem-Tempo", False, selected_language)
    except Exception as e:
        print(f"Erro ao processar vídeo ID {video_id}: {e}")

def is_playlist(url):
    return 'list=' in url

def get_playlist_videos(url):
    playlist = Playlist(url)
    return list(playlist.video_urls)

def main():
    video_url = url_entry.get()
    selected_index = idiomas_descricao.index(language_combobox.get())
    selected_language = idiomas_codigo[selected_index]

    if is_playlist(video_url):
        video_urls = get_playlist_videos(video_url)
        video_ids = [get_video_id(url) for url in video_urls]
        for video_url in video_urls:
            video_id = get_video_id(video_url)
            yt = YouTube(video_url)
            title = yt.title.replace(' ', '-')
            threading.Thread(target=process_video, args=(video_id, selected_language, title)).start()
    else:
        video_id = get_video_id(video_url)
        yt = YouTube(video_url)
        title = yt.title.replace(' ', '-')
        threading.Thread(target=process_video, args=(video_id, selected_language, title)).start()

# Listas de idiomas
idiomas_descricao = [
    "Afrikaans (af)", "Akan (ak)", "Albanian (sq)", "Amharic (am)", "Arabic (ar)",
    "Armenian (hy)", "Assamese (as)", "Aymara (ay)", "Azerbaijani (az)", "Bangla (bn)",
    "Basque (eu)", "Belarusian (be)", "Bhojpuri (bho)", "Bosnian (bs)", "Bulgarian (bg)",
    "Burmese (my)", "Catalan (ca)", "Cebuano (ceb)", "Chinese (Simplified) (zh-Hans)", "Chinese (Traditional) (zh-Hant)",
    "Corsican (co)", "Croatian (hr)", "Czech (cs)", "Danish (da)", "Divehi (dv)",
    "Dutch (nl)", "English (en)", "Esperanto (eo)", "Estonian (et)", "Ewe (ee)",
    "Filipino (fil)", "Finnish (fi)", "French (fr)", "Galician (gl)", "Ganda (lg)",
    "Georgian (ka)", "German (de)", "Greek (el)", "Guarani (gn)", "Gujarati (gu)",
    "Haitian Creole (ht)", "Hausa (ha)", "Hawaiian (haw)", "Hebrew (iw)", "Hindi (hi)",
    "Hmong (hmn)", "Hungarian (hu)", "Icelandic (is)", "Igbo (ig)", "Indonesian (id)",
    "Irish (ga)", "Italian (it)", "Japanese (ja)", "Javanese (jv)", "Kannada (kn)",
    "Kazakh (kk)", "Khmer (km)", "Kinyarwanda (rw)", "Korean (ko)", "Krio (kri)",
    "Kurdish (ku)", "Kyrgyz (ky)", "Lao (lo)", "Latin (la)", "Latvian (lv)",
    "Lingala (ln)", "Lithuanian (lt)", "Luxembourgish (lb)", "Macedonian (mk)", "Malagasy (mg)",
    "Malay (ms)", "Malayalam (ml)", "Maltese (mt)", "Māori (mi)", "Marathi (mr)",
    "Mongolian (mn)", "Nepali (ne)", "Northern Sotho (nso)", "Norwegian (no)", "Nyanja (ny)",
    "Odia (or)", "Oromo (om)", "Pashto (ps)", "Persian (fa)", "Polish (pl)",
    "Portuguese (pt)", "Punjabi (pa)", "Quechua (qu)", "Romanian (ro)", "Russian (ru)",
    "Samoan (sm)", "Sanskrit (sa)", "Scottish Gaelic (gd)", "Serbian (sr)", "Shona (sn)",
    "Sindhi (sd)", "Sinhala (si)", "Slovak (sk)", "Slovenian (sl)", "Somali (so)",
    "Southern Sotho (st)", "Spanish (es)", "Sundanese (su)", "Swahili (sw)", "Swedish (sv)",
    "Tajik (tg)", "Tamil (ta)", "Tatar (tt)", "Telugu (te)", "Thai (th)",
    "Tigrinya (ti)", "Tsonga (ts)", "Turkish (tr)", "Turkmen (tk)", "Ukrainian (uk)",
    "Urdu (ur)", "Uyghur (ug)", "Uzbek (uz)", "Vietnamese (vi)", "Welsh (cy)",
    "Western Frisian (fy)", "Xhosa (xh)", "Yiddish (yi)", "Yoruba (yo)", "Zulu (zu)"
]


idiomas_codigo = [
    "af", "ak", "sq", "am", "ar", "hy", "as", "ay", "az", "bn",
    "eu", "be", "bho", "bs", "bg", "my", "ca", "ceb", "zh-Hans", "zh-Hant",
    "co", "hr", "cs", "da", "dv", "nl", "en", "eo", "et", "ee",
    "fil", "fi", "fr", "gl", "lg", "ka", "de", "el", "gn", "gu",
    "ht", "ha", "haw", "iw", "hi", "hmn", "hu", "is", "ig", "id",
    "ga", "it", "ja", "jv", "kn", "kk", "km", "rw", "ko", "kri",
    "ku", "ky", "lo", "la", "lv", "ln", "lt", "lb", "mk", "mg",
    "ms", "ml", "mt", "mi", "mr", "mn", "ne", "nso", "no", "ny",
    "or", "om", "ps", "fa", "pl", "pt", "pa", "qu", "ro", "ru",
    "sm", "sa", "gd", "sr", "sn", "sd", "si", "sk", "sl", "so",
    "st", "es", "su", "sw", "sv", "tg", "ta", "tt", "te", "th",
    "ti", "ts", "tr", "tk", "uk", "ur", "ug", "uz", "vi", "cy",
    "fy", "xh", "yi", "yo", "zu"
]

def get_video_id(url):
    regex = r"(?<=v=)[^&#]+"
    matches = re.search(regex, url)
    return matches.group(0) if matches else None

def save_transcript(transcript, title, include_time, language):
    filename = f"{title.replace(' ', '-')}-{language}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        for entry in transcript:
            text = entry['text']
            if text is not None:
                if include_time:
                    file.write(f"{text} (Tempo: {entry['start']}s)\n")
                else:
                    file.write(f"{text}\n")
    print(f"Transcrição salva em {filename}")

def fetch_and_save_transcript():
    video_url = url_entry.get()
    selected_index = idiomas_descricao.index(language_combobox.get())
    selected_language = idiomas_codigo[selected_index]
    video_id = get_video_id(video_url)
    yt = YouTube(video_url)
    title = yt.title.replace(' ', '-')

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[selected_language])
        save_transcript(transcript, title, True, selected_language)
        save_transcript(transcript, f"{title}-Sem-Tempo", False, selected_language)
    except Exception as e:
        print(f"Erro ao obter transcrição: {e}")

# Criando a janela principal
root = tk.Tk()
root.title("Transcritor de Vídeos do YouTube")

# Adicionando entrada de texto para URL
tk.Label(root, text="Insira o link do vídeo do YouTube:").pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()

# Adicionando ComboBox para seleção de idioma
tk.Label(root, text="Selecione o idioma da transcrição:").pack()
language_combobox = ttk.Combobox(root, values=idiomas_descricao, state="readonly")
language_combobox.pack()
language_combobox.set("Portuguese (pt)")  # Idioma padrão

# Adicionando botão de enviar
submit_button = tk.Button(root, text="Transcrever", command=main)
submit_button.pack()

root.mainloop()
