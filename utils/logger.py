import os
import datetime

class StatusLogger:
    def __init__(self):
        agora = datetime.datetime.now()
        timestamp = agora.strftime("%Y-%m-%d")
        self.log_file = f"data/logs/log_{timestamp}.txt"
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write("### LOG DE EXECUÇÃO ###\n")

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("[%d/%m/%Y %H:%M:%S]")
        full_message = f"{timestamp} {message}\n"
        with open(self.log_file, "a", encoding="utf-8") as file:
            file.write(full_message)
