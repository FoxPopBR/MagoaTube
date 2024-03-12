#modules\data_video.py
import yt_dlp
from .manager_db import DatabaseManager
from .path_tree import root_path, database_path

# Em data_video.py, após criar a instância de DatabaseManager
db_manager = DatabaseManager(database_path)
#db_manager.inicializar_db()  # Garante que todas as tabelas necessárias existam
inserir_video = db_manager.inserir_video

# Variáveis para a tabela 'videos'
video_url = None
video_title = None
video_duration = None
video_description = None
video_views = None
video_likes = None
video_dislikes = None
video_upload_date = None
video_uploader = None

# Variáveis para a tabela 'progressive_streams'
prog_stream_video_id = None
prog_stream_format_id = None
prog_stream_download_url = None
prog_stream_type = "Audio e Video"  # tipo fixo para streams progressivos
prog_stream_file_extension = None
prog_stream_resolution = None
prog_stream_fps = None
prog_stream_codec = None
prog_stream_bitrate = None
prog_stream_file_size_pro = 0

# Variáveis para a tabela 'adaptive_streams'
adapt_stream_video_id = None
adapt_stream_format_id = None
adapt_stream_download_url = None
adapt_stream_type = None  # será 'audio' ou 'video'
adapt_stream_file_extension = None
adapt_stream_resolution = None
adapt_stream_fps = None
adapt_stream_codec = None
adapt_stream_bitrate = None
adapt_stream_file_size_adp = None
adapt_stream_audio_quality = None

# Variáveis para a tabela 'thumbnails'
thumb_video_id = None
thumb_url = None
thumb_width = None
thumb_height = None

def extract_video_info(url):
    global video_url, video_title, video_duration, video_description, video_views, video_likes, video_dislikes, video_upload_date, video_uploader
    global prog_stream_format_id, prog_stream_download_url, prog_stream_type, prog_stream_file_extension, prog_stream_resolution, prog_stream_fps, prog_stream_codec, prog_stream_bitrate, prog_stream_file_size_pro
    global adapt_stream_format_id, adapt_stream_download_url, adapt_stream_type, adapt_stream_file_extension, adapt_stream_resolution, adapt_stream_fps, adapt_stream_codec, adapt_stream_bitrate, adapt_stream_file_size_adp, adapt_stream_audio_quality
    global thumb_url, thumb_width, thumb_height
    video_url = url
    ydl_opts = {
        'format': 'bestaudio/best',
        #'outtmpl': '%(id)s.%(ext)s',
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=False)
            video_info = {
                'url': info_dict.get('webpage_url', ''),
                'title': info_dict.get('title', ''),
                'duration': info_dict.get('duration', 0),
                'description': info_dict.get('description', ''),
                'views': info_dict.get('view_count', 0),
                'likes': info_dict.get('like_count', 0),
                'dislikes': 0,  # Supondo que dislikes não são mais fornecidos
                'upload_date': info_dict.get('upload_date', ''),
                'uploader': info_dict.get('uploader', ''),
            }

            streams_progressivos = [{
                'format_id': stream.get('format_id', ''),
                'download_url': stream.get('url', ''),
                'file_extension': stream.get('ext', ''),
                'resolution': stream.get('resolution', ''),
                'fps': stream.get('fps', 0),
                'codec': stream.get('vcodec', ''),
                'bitrate': stream.get('tbr', 0),
                'file_size_pro': stream.get('file_size_pro', 0),
            } for stream in info_dict.get('formats', []) if stream.get('acodec') != 'none']

            streams_adaptativos = [{
                'format_id': stream.get('format_id', ''),
                'download_url': stream.get('url', ''),
                'file_extension': stream.get('ext', ''),
                'resolution': stream.get('resolution', ''),
                'fps': stream.get('fps', 0),
                'codec': stream.get('vcodec', ''),
                'bitrate': stream.get('tbr', 0),
                'file_size_adp': stream.get('file_size_adp', 0),
                'audio_quality': stream.get('asr', 0),
            } for stream in info_dict.get('formats', []) if stream.get('acodec') == 'none']

            miniaturas = [{
                'url': thumb.get('url', ''),
                'width': thumb.get('width', 0),
                'height': thumb.get('height', 0),
            } for thumb in info_dict.get('thumbnails', [])]

            process_video_info(video_info, streams_progressivos, streams_adaptativos, miniaturas)
            return True
        except Exception as e:
            print(f"Erro ao extrair informações do vídeo: {e}")
            return False

def process_video_info(video_info, streams_progressivos, streams_adaptativos, miniaturas):
    # Primeiro, verifica se o vídeo já existe no banco de dados
    existe = db_manager.verificar_existencia_video(video_info['url'], video_info['title'])
    if existe:
        print("Esse vídeo já está cadastrado.")
        return None  # Retorna None para indicar que não houve necessidade de inserção
    # Tenta inserir o vídeo e captura o ID do vídeo inserido.
    video_id = db_manager.inserir_video(video_info, streams_progressivos, streams_adaptativos, miniaturas)

    # Verifica se a inserção foi bem-sucedida.
    if video_id:
        print(f"Vídeo ID: {video_id} inserido com sucesso.")
        return video_id
    else:
        print("Falha ao inserir o vídeo no banco de dados.")
        return None