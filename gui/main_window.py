# gui/main_window.py

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from utils.logger import StatusLogger
from datetime import datetime, timedelta
from services import gerar_relatorio
import threading
import sys


class MainWindow(tk.Frame):
    def __init__(self, master, on_execute_callback, on_open_settings_callback):
        super().__init__(master)

        self.master = master
        self.on_execute_callback = on_execute_callback
        self.on_open_settings_callback = on_open_settings_callback

        self.logger = StatusLogger()
        self.root = master

        self._setup_ui()

    def _setup_ui(self):
        self.root.iconbitmap("dente.ico")
        self.root.geometry("500x415")
        self.root.configure(bg="#f4f4f4")
        self.root.title("Captador de Sorrisos")

        # Centralizar a janela
        self.root.update_idletasks()
        largura_janela = self.root.winfo_width()
        altura_janela = self.root.winfo_height()
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)
        self.root.geometry(f"+{pos_x}+{pos_y}")

        # Datas
        self.dates_frame = tk.Frame(self.root, bg="#f4f4f4")
        self.dates_frame.pack(pady=10)

        self.start_date_label = tk.Label(self.dates_frame, text="Início:", bg="#f4f4f4", font=("Arial", 12))
        self.start_date_label.grid(row=0, column=0, padx=5)

        self.start_date_entry = ttk.Entry(self.dates_frame, font=("Arial", 12), justify="center", width=12)
        self.start_date_entry.grid(row=1, column=0, padx=5)

        self.end_date_label = tk.Label(self.dates_frame, text="Final:", bg="#f4f4f4", font=("Arial", 12))
        self.end_date_label.grid(row=0, column=1, padx=5)

        self.end_date_entry = ttk.Entry(self.dates_frame, font=("Arial", 12), justify="center", width=12)
        self.end_date_entry.grid(row=1, column=1, padx=5)

        ontem = datetime.today() - timedelta(days=1)
        anteontem = datetime.today() - timedelta(days=1)

        self.start_date_entry.insert(0, anteontem.strftime("%d/%m/%Y"))
        self.end_date_entry.insert(0, ontem.strftime("%d/%m/%Y"))

        # Botões
        self.buttons_frame = tk.Frame(self.root, bg="#f4f4f4")
        self.buttons_frame.pack(pady=15)

        self.botao_gerar = ttk.Button(
            self.buttons_frame, text="Gerar Planilha", command=self._gerar_relatorio
        )
        self.botao_gerar.grid(row=0, column=0, padx=10)

        self.botao_enviar = ttk.Button(
            self.buttons_frame, text="Iniciar Envio", command=self._envio_whatsapp
        )
        self.botao_enviar.grid(row=0, column=1, padx=10)

        self.settings_button = ttk.Button(
            self.buttons_frame, text="⚙️ Configurações", command=self.on_open_settings_callback
        )
        self.settings_button.grid(row=0, column=2, padx=10)

        # Barra de progresso
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)

        # Status
        self.status_label = tk.Label(self.root, text="Status: Aguardando...", bg="#f4f4f4", font=("Arial", 10))
        self.status_label.pack(pady=5)

        # Console de logs (abaixo do status)
        self.console_text = tk.Text(self.root, height=10, width=60, font=("Courier", 10), state="disabled", bg="#f9f9f9")
        self.console_text.pack(pady=(0, 10))

        # Redireciona stdout e stderr pro console da interface
        sys.stdout = ConsoleRedirect(self.console_text)
        sys.stderr = ConsoleRedirect(self.console_text)

        # Autor
        self.autor_label = tk.Label(self.root, text="L.M.", bg="#f4f4f4", fg="#333333", font=("Arial", 7))
        self.autor_label.pack(pady=5)

    def _gerar_relatorio(self):
        def tarefa():
            try:
                data_inicio_str = self.start_date_entry.get()
                data_fim_str = self.end_date_entry.get()

                self.root.after(0, lambda: self.atualizar_status("Gerando planilha..."))
                self.root.after(0, lambda: self.botao_gerar.config(state="disabled"))
                self.root.after(0, lambda: self.botao_enviar.config(state="disabled"))

                resultado = gerar_relatorio(data_inicio_str, data_fim_str)

                if resultado and resultado.get("sucesso"):
                    self.root.after(0, lambda: self.atualizar_status("Planilha gerada com sucesso."))
                else:
                    self.root.after(0, lambda: self.atualizar_status(f"Erro: {resultado.get('mensagem')}"))
            except Exception as e:
                erro_msg = str(e)
                self.root.after(0, lambda: messagebox.showerror("Erro", f"Ocorreu um erro ao executar: {erro_msg}"))
                self.root.after(0, lambda: self.atualizar_status(f"Erro: {erro_msg}"))
            finally:
                self.root.after(0, lambda: self.botao_gerar.config(state="normal"))
                self.root.after(0, lambda: self.botao_enviar.config(state="normal"))

        threading.Thread(target=tarefa).start()

    def _envio_whatsapp(self):
        def tarefa():
            try:
                data_inicio_str = self.start_date_entry.get()
                data_fim_str = self.end_date_entry.get()

                self.root.after(0, lambda: self.atualizar_status("Iniciando envio de mensagens..."))
                self.root.after(0, lambda: self.botao_enviar.config(state="disabled"))
                self.root.after(0, lambda: self.botao_gerar.config(state="disabled"))

                self.on_execute_callback(data_inicio_str, data_fim_str)

                self.root.after(0, lambda: self.atualizar_status("Mensagens enviadas com sucesso."))
            except Exception as e:
                erro_msg = str(e)
                self.root.after(0, lambda: messagebox.showerror("Erro", f"Ocorreu um erro durante o envio: {erro_msg}"))
                self.root.after(0, lambda: self.atualizar_status(f"Erro: {erro_msg}"))
            finally:
                self.root.after(0, lambda: self.botao_enviar.config(state="normal"))
                self.root.after(0, lambda: self.botao_gerar.config(state="normal"))

        threading.Thread(target=tarefa).start()

    def atualizar_status(self, mensagem):
        self.status_label.config(text=f"Status: {mensagem}")
        self.logger.log(mensagem)
        self.adicionar_ao_console(mensagem)

    def atualizar_progresso(self, valor):
        self.progress['value'] = valor
        self.root.update_idletasks()

    def adicionar_ao_console(self, mensagem):
        self.console_text.config(state="normal")
        self.console_text.insert(tk.END, f"{mensagem}\n")
        self.console_text.see(tk.END)  # Scroll automático pro final
        self.console_text.config(state="disabled")


class ConsoleRedirect:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.config(state="normal")
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)
        self.text_widget.config(state="disabled")

    def flush(self):
        pass  # Necessário para compatibilidade com sys.stdout