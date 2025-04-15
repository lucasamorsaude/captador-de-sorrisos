# gui/settings_window.py

import tkinter as tk
from tkinter import ttk
from gui.settings import Settings
from services.conectar_whatsapp import conectar_whatsapp
import threading

class SettingsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Configurações")
        self.geometry("300x280")
        self.resizable(False, False)

        self.settings = Settings()

        # Widgets
        self.create_widgets()

        self.update_idletasks()
        largura_janela = self.winfo_width()
        altura_janela = self.winfo_height()

        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()

        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)

        self.geometry(f"+{pos_x}+{pos_y}")

    def create_widgets(self):
        # Usuário
        tk.Label(self, text="Usuário:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.usuario_entry = ttk.Entry(self, width=30)
        self.usuario_entry.insert(0, self.settings.get("usuario"))
        self.usuario_entry.grid(row=0, column=1)

        # Senha
        tk.Label(self, text="Senha:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.senha_entry = ttk.Entry(self, width=30, show="*")
        self.senha_entry.insert(0, self.settings.get("senha"))
        self.senha_entry.grid(row=1, column=1)

        # Delay
        tk.Label(self, text="Delay (s):").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.delay_spinbox = ttk.Spinbox(self, from_=1, to=60, width=5)
        self.delay_spinbox.set(self.settings.get("delay_envio"))
        self.delay_spinbox.grid(row=2, column=1, sticky="w")

        # Conectar Whatsapp
        conectar_btn = ttk.Button(self, text="Conectar Whatsapp", command=self.conectar_whatsapp)
        conectar_btn.grid(row=3, column=0, columnspan=2, pady=20)

        # Botões
        salvar_btn = ttk.Button(self, text="Salvar", command=self.salvar)
        salvar_btn.grid(row=4, column=0, columnspan=2, pady=20)

    def salvar(self):
        self.settings.set("usuario", self.usuario_entry.get())
        self.settings.set("senha", self.senha_entry.get())
        self.settings.set("delay_envio", int(self.delay_spinbox.get()))
        self.settings.save()
        self.destroy()


    def conectar_whatsapp(self):
        thread = threading.Thread(target=conectar_whatsapp)
        thread.daemon = True  # Encerrar junto com o programa, se necessário
        thread.start()

