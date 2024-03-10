import os
import json

locating = os.path.dirname(os.path.realpath(__file__)) # caminho desse arquivo pasta modules
path_root = os.path.dirname(locating) # caiminho registrado como raiz do projeto
json_file_path = os.path.join(path_root, 'path_config.json') # cominho do arquivo JSON com os endereços dos arquivos do projeto
database_path = os.path.join(path_root, 'dados.db') # caminho do

# Cria um dicionário com as informações do caminho
path_info = {
    "root_directory": path_root,
    "database_path": database_path,
    "path_json_config": json_file_path
}


if not os.path.exists(json_file_path):
    # Salva as informações no arquivo JSON
    with open(json_file_path, 'w') as json_file:
        json.dump(path_info, json_file, indent=4)

with open(json_file_path, 'r') as json_path:
    loaded_json_path = json.load(json_path)

#path_link1 = loaded_json_path["label_do_caminho"] # apontar para um endereço especifico usando label que contem o caminho do arquivo JSON

root_path = loaded_json_path["root_directory"]
database_path = loaded_json_path["database_path"]
json_config_path = loaded_json_path["path_json_config"]

