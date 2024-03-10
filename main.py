#main.py
import modules.path_tree  # Precisa ser o primeiro módulo a ser importado, e precisa ser importado mesmo sem uso!
print("Root Project: ",modules.path_tree.root_path)
print("Database Project: ",modules.path_tree.database_path)
print("Json Config Path Project: ",modules.path_tree.json_config_path)
from modules.check_monitor import Check_Screen
check_screen = Check_Screen()
check_screen.update_monitor()
from main_screen import Magoa



if __name__ == "__main__":
    app = Magoa(check_screen)
    app.main_ui()  # Executa a janela principal
    app.mainloop()