import tkinter as tk
from gui.main_window import MainWindow
from gui.settings_window import SettingsWindow
from services.webdental import gerar_relatorio
from services.whatsapp import enviar_planilha_para_slack


def main():
    root = tk.Tk()

    def executar_envio(data_inicio, data_fim):
        print(f"Enviando mensagens de {data_inicio} até {data_fim}...")
        enviar_planilha_para_slack()  # Agora efetivamente dispara o envio

    def abrir_configuracoes():
        SettingsWindow(root)

    app = MainWindow(
        root,
        on_execute_callback=executar_envio,
        on_open_settings_callback=abrir_configuracoes
    )
    app.pack(fill="both", expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()
