# main.py

from services.webdental import gerar_relatorio
from services.slack import enviar_planilha_para_slack

def main():
    # Passa as datas ou deixa que a função gerar_relatorio defina automaticamente
    resultado_relatorio = gerar_relatorio()

    if resultado_relatorio["sucesso"]:
        print(resultado_relatorio["mensagem"])

        # Chama a função para enviar a planilha para o Slack
        enviar_planilha_para_slack()
    else:
        print(f"Erro ao gerar o relatório: {resultado_relatorio['mensagem']}")

if __name__ == "__main__":
    main()
