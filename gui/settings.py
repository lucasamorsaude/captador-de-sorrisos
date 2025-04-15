# gui/settings.py

import json
import os

CONFIG_PATH = "config.json"

class Settings:
    def __init__(self):
        self.config = {
            "usuario": "",
            "senha": "",
            "delay_envio": 5
        }
        self.load()

    def load(self):
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as file:
                    self.config.update(json.load(file))
            except Exception as e:
                print(f"Erro ao carregar configurações: {e}")

    def save(self):
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as file:
                json.dump(self.config, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")

    def get(self, chave):
        return self.config.get(chave, "")

    def set(self, chave, valor):
        self.config[chave] = valor
