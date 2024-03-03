#main.py
import tkinter as tk
from main_screen import Magoa, Check_Screen
# Incia verificação de monitores disponíveis, e salva resoluções dos monitores e outros
check_screen = Check_Screen()
check_screen.update_monitor()

if __name__ == "__main__":
    app = Magoa(check_screen)
    app.main_ui()  # Executa a janela principal
    app.mainloop()