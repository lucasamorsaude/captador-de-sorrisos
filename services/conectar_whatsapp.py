import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def conectar_whatsapp():
    try:
        print("🔄 Conectando ao WhatsApp Web...")

        # Cria a pasta do perfil se não existir
        profile_dir = os.path.abspath("whatsapp_profile")
        os.makedirs(profile_dir, exist_ok=True)

        options = Options()
        options.add_argument(f'--user-data-dir={profile_dir}')
        options.add_experimental_option("detach", True)  # Deixa o navegador aberto após script encerrar

        driver = webdriver.Chrome(service=Service(), options=options)
        driver.get("https://web.whatsapp.com")

        print("✅ WhatsApp carregado. Escaneie o QR Code (se necessário).")
        print("ℹ️ Aguarde... o script continuará quando o navegador for fechado.")

        # Espera até o navegador ser fechado pelo usuário
        while True:
            try:
                _ = driver.title  # tenta acessar algo do driver
                time.sleep(1)
            except:
                
                break  # se der erro, o navegador foi fechado

        print("✅ Navegador fechado. Conexão finalizada.")

    except Exception as e:
        print(f"❌ Erro ao conectar ao WhatsApp: {e}")
