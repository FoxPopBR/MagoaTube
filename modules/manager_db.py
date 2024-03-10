import sqlite3
#from sqlite3 import IntegrityError, OperationalError
from tkinter import messagebox
from .path_tree import root_path, database_path


class DatabaseManager:
    def __init__(self, database_path):
        self.db_path = database_path
        self.conectar_db()  # Garantindo que a conexão seja testada ao iniciar
        self.inicializar_db()

    def conectar_db(self):
        #print ("Iniciando conexão ao banco de dados...")
        try:
            return sqlite3.connect(database_path)
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None

    #Usa o titulo do video selecionado no combobox para obter informações sobre o vídeo tabela Videos
    def buscar_informacoes_video_pelo_titulo(self, titulo):
        conn = self.conectar_db()
        video_info = {}
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM videos WHERE title = ?", (titulo,))
            row = cursor.fetchone()
            if row:
                video_info = {'id': row[0], 'url': row[1], 'title': row[2], 'description': row[4]}  # Add all needed fields
        except Exception as e:
            print(f"Error fetching video information: {e}")
        finally:
            conn.close()
        return video_info

    def buscar_info_completa_por_titulo(self, titulo):
        conn = self.conectar_db()
        if conn is None:
            return {}

        try:
            video_info = {}
            streams_progressivos = []
            streams_adaptativos = []
            miniaturas = []

            # Buscar informações do vídeo na tabela videos
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM videos WHERE title = ?", (titulo,))
            row = cursor.fetchone()
            if row:
                video_info = {
                    'id': row[0], 'url': row[1], 'title': row[2], 'description': row[3],
                    'views': row[4], 'likes': row[5], 'dislikes': row[6], 'upload_date': row[7], 'uploader': row[8]
                }
                id_video = row[0]

                # Buscar streams progressivos
                cursor.execute("SELECT * FROM progressive_streams WHERE video_id = ?", (id_video,))
                for row in cursor.fetchall():
                    streams_progressivos.append({
                        'format_id': row[2], 'download_url': row[3], 'file_extension': row[4],
                        'resolution': row[5], 'fps': row[6], 'codec': row[7], 'bitrate': row[8], 'file_size': row[9]
                    })

                # Buscar streams adaptativos
                cursor.execute("SELECT * FROM adaptive_streams WHERE video_id = ?", (id_video,))
                for row in cursor.fetchall():
                    streams_adaptativos.append({
                        'format_id': row[2], 'download_url': row[3], 'file_extension': row[4],
                        'resolution': row[5], 'fps': row[6], 'codec': row[7], 'bitrate': row[8], 'file_size': row[9],
                        'audio_quality': row[10]
                    })

                # Buscar miniaturas
                cursor.execute("SELECT * FROM thumbnails WHERE video_id = ?", (id_video,))
                for row in cursor.fetchall():
                    miniaturas.append({'url': row[2], 'width': row[3], 'height': row[4]})

            return {
                'video': video_info,
                'progressive_streams': streams_progressivos,
                'adaptive_streams': streams_adaptativos,
                'thumbnails': miniaturas
            }
        except Exception as e:
            print(f"Erro ao buscar informações completas do vídeo: {e}")
            return {}
        finally:
            conn.close()



    # Atualiza conteudo do banco de dados id e titulo
    def buscar_titulos_e_ids_videos(self):
        conn = self.conectar_db()
        if conn is None:
            return []

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title FROM videos")
            videos = [{'id': video[0], 'title': video[1]} for video in cursor.fetchall()]
            return videos
        except sqlite3.Error as e:
            print(f"Erro ao buscar títulos e IDs dos vídeos: {e}")
            return []
        finally:
            conn.close()



    def verificar_existencia_video(self, url, titulo):
        print("Verificando existência do vídeo...")
        conn = self.conectar_db()
        if conn is None:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM videos WHERE url=? AND title=?", (url, titulo))
            result = cursor.fetchone()
            if result:
                messagebox.showinfo("Informação", "Esse vídeo já está cadastrado")
                return True
            else:
                print("Iniciando processo de salvamento de dados")
                return False
        except sqlite3.Error as e:
            print(f"Erro ao verificar a existência do vídeo: {e}")
            return False
        finally:
            conn.close()

    def inserir_video(self, video_info, streams_progressivos, streams_adaptativos, miniaturas):
        print("Inserindo vídeo chamado...")
        conn = self.conectar_db()
        if conn is None:
            print("Não foi possível conectar ao banco de dados.")
            return None
        print ("conexão concluída com sucesso! Iniciando processo de salvamento de dados...")
        try:
            cursor = conn.cursor()
            # Insere informações do vídeo
            cursor.execute('''INSERT INTO videos (url, title, duration, description, views, likes, dislikes, upload_date, uploader)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (video_info['url'], video_info['title'], video_info['duration'], video_info['description'], 
                            video_info['views'], video_info['likes'], video_info['dislikes'], video_info['upload_date'], 
                            video_info['uploader']))
            video_id = cursor.lastrowid

            # Insere streams progressivos
            for stream in streams_progressivos:
                cursor.execute('''INSERT INTO progressive_streams (video_id, format_id, download_url, file_extension, resolution, fps, codec, bitrate, file_size)
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                               (video_id, stream['format_id'], stream['download_url'], stream['file_extension'], 
                                stream['resolution'], stream['fps'], stream['codec'], stream['bitrate'], stream['file_size']))

            # Insere streams adaptativos
            for stream in streams_adaptativos:
                cursor.execute('''INSERT INTO adaptive_streams (video_id, format_id, download_url, file_extension, resolution, fps, codec, bitrate, file_size, audio_quality)
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                               (video_id, stream['format_id'], stream['download_url'], stream['file_extension'], 
                                stream['resolution'], stream['fps'], stream['codec'], stream['bitrate'], stream['file_size'], 
                                stream['audio_quality']))

            # Insere miniaturas
            for thumbnail in miniaturas:
                cursor.execute('''INSERT INTO thumbnails (video_id, url, width, height)
                                  VALUES (?, ?, ?, ?)''',
                               (video_id, thumbnail['url'], thumbnail['width'], thumbnail['height']))

            conn.commit()
            return video_id

        except sqlite3.Error as e:
            print(f"Erro ao inserir dados no banco de dados: {e}")
            return None
        finally:
            conn.close()

    def buscar_titulos_videos(self):
        conn = self.conectar_db()
        if conn is None:
            return []

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT title FROM videos")
            titulos = [titulo[0] for titulo in cursor.fetchall()]
            return titulos
        except sqlite3.Error as e:
            print(f"Erro ao buscar títulos dos vídeos: {e}")
            return []
        finally:
            conn.close()

    # Criando tabela de bando de dados.db
    def inicializar_db(self):
        #print ("Iniciando processo de criação de banco de dados")
        conn = self.conectar_db()
        if conn is None:
            return

        try:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                title TEXT,
                duration INTEGER,
                description TEXT,
                views INTEGER,
                likes INTEGER,
                dislikes INTEGER,
                upload_date TEXT,
                uploader TEXT)
            ''')

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS progressive_streams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id INTEGER,
                format_id TEXT,
                download_url TEXT,
                type TEXT,
                file_extension TEXT,
                resolution TEXT,
                fps INTEGER,
                codec TEXT,
                bitrate INTEGER,
                file_size INTEGER,
                FOREIGN KEY(video_id) REFERENCES videos(id))
            ''')

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS adaptive_streams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id INTEGER,
                format_id TEXT,
                download_url TEXT,
                type TEXT,
                file_extension TEXT,
                resolution TEXT,
                fps INTEGER,
                codec TEXT,
                bitrate INTEGER,
                file_size INTEGER,
                audio_quality INTEGER,
                FOREIGN KEY(video_id) REFERENCES videos(id))
            ''')

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS thumbnails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id INTEGER,
                url TEXT,
                width INTEGER,
                height INTEGER,
                FOREIGN KEY(video_id) REFERENCES videos(id))
            ''')
            conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao inicializar o banco de dados: {e}")
        finally:
            conn.close()