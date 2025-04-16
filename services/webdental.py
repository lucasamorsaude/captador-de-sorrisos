#services/webdental.py

import json
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
import urllib.parse
import traceback

# Carregar configurações de login
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

USUARIO = config["usuario"]
SENHA = config["senha"]




def gerar_relatorio(data_inicio=None, data_fim=None):
    # Pega a data atual
    hoje = datetime.today()
    dia_da_semana = hoje.weekday()  # 0 = segunda, 1 = terça, ..., 5 = sexta, 6 = sábado, 7 = domingo

    # Lógica para determinar data_inicio e data_fim
    if dia_da_semana == 0:  # Segunda-feira
        data_fim = hoje - timedelta(days=2)  # Sexta-feira
        data_inicio = hoje - timedelta(days=3)  # Sábado
    elif dia_da_semana in [1, 2, 3, 4]:  # De terça a sexta-feira
        data_fim = hoje - timedelta(days=1)  # Ontem
        data_inicio = hoje - timedelta(days=1)  # Anteontem
    # Caso seja sábado ou domingo, não gera relatório
    elif dia_da_semana in [5, 6]:  # Sábado ou Domingo
        print("Não há relatório a ser gerado hoje. Esperando até segunda-feira.")
        return

    # Formatar as datas
    data_inicio = data_inicio.strftime("%d/%m/%Y")
    data_fim = data_fim.strftime("%d/%m/%Y")
    
    print(f"🔄 Gerando relatório de {data_inicio} até {data_fim}...")

    profile_dir = os.path.abspath("whatsapp_profile")
    os.makedirs(profile_dir, exist_ok=True)

    # Opções do navegador
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument(f'--user-data-dir={profile_dir}')
    

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    wait = WebDriverWait(driver, 20)

    try:
        print("🔐 Acessando login...")
        driver.get("https://sistema.webdentalsolucoes.io/index.php?lar=1536&alt=703")
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='usuario']")))

        driver.find_element(By.XPATH, "//input[@name='usuario']").send_keys(USUARIO)
        driver.find_element(By.XPATH, "//input[@name='senha']").send_keys(SENHA)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="unidade_login"]'))
        ).click()

        time.sleep(1)

        driver.find_element(By.ID, "btn_entrar").click()


        print("✅ Login feito, iniciando...")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[3]/div[2]/ul/li[9]/a'))
        ).click()


        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[3]/div[1]/div/span/div/div[2]/div[16]'))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "TB_iframeContent"))
        )

        

        print("🗓️ Preenchendo datas...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "dtini"))
        ).send_keys(formatar_data(data_inicio))

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "dtfim"))
        ).send_keys(formatar_data(data_fim))

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='s2id_tipo']/a"))
        ).click()
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='select2-drop']/div/input"))
        ).send_keys("Detalhado", Keys.RETURN)

        # Clica no botão "Gerar"
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='frel']/div[2]/a"))
        ).click()

        print("📊 Gerando relatório...")
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(10)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


        print("📥 Extraindo dados da tabela...")

        tabela = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/div[1]/table"))
        )
        linhas = tabela.find_elements(By.TAG_NAME, "tr")

        dados = []
        nomes_vistos = set()

        for linha in linhas:
            try:
                nome = linha.find_element(By.XPATH, "./td[1]/a").text
                telefone = linha.find_element(By.XPATH, "./td[2]").text.replace("-", "")

                if nome in nomes_vistos:
                    continue
                
                nomes_vistos.add(nome)
                mensagem = f"""Olá {nome} Tudo bem?😊
                
Passando para relembrar o orçamento que você fez conosco 💬
                
Estamos com ótimas condições para te ajudar a iniciar seu tratamento 💙
                
Quer entender melhor? Aproveita esse momento para garantir o cuidado que você merece!😉"""

                link = url_mensagem_whatsapp(telefone, mensagem)

                dados.append([nome, telefone, link])

            except Exception:
                continue  
        
        # Salva os dados no Excel
        df = pd.DataFrame(dados, columns=["Nome", "Telefone", "Link"])
        caminho_planilha = "data/relatorio_efetivados.xlsx"
        df.to_excel(caminho_planilha, index=False)

        total_encontrados = len(dados)
        print(f"✅ Planilha gerada com sucesso! {total_encontrados} pessoas encontradas.")
        return {
            "sucesso": True,
            "mensagem": f"Relatório gerado com sucesso! {total_encontrados} pessoas encontradas.",
            "total_encontrados": total_encontrados
        }


    except TimeoutException:
        print("⏰ Timeout! A página demorou demais para responder.")
    except Exception as e:
    
        return {
            "sucesso": False,
            "mensagem": "Erro ao gerar o relatório. Verifique os logs.",
            "erro": str(e)
        }
    finally:
        driver.quit()
        print("🧹 Navegador fechado.")

def formatar_data(data):
    """ Remove as barras e retorna a data no formato DDMMYYYY """
    return data.replace("/", "")

def url_mensagem_whatsapp(numero, mensagem):
    """ Gera um link de mensagem do WhatsApp """
    numero = "+55" + numero.replace("-", "").strip()
    mensagem = urllib.parse.quote(mensagem)
    return f"https://web.whatsapp.com/send?phone={numero}&text={mensagem}"

gerar_relatorio()