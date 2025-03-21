import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import urllib.parse  # Para codificar a mensagem corretamente

# 📥 Carregar os dados do CSV
df = pd.read_csv("sorteio_apadrinhamento.csv", dtype=str)

# 📌 Converter para string e remover .0 logo após a leitura
df["TelefoneV"] = df["TelefoneV"].astype(str).apply(lambda x: x[:-2] if x.endswith(".0") else x)

# 📌 Ler os arquivos de mensagens
with open("masc.txt", "r", encoding="utf-8") as file:
    msg_masc = file.read()

with open("fem.txt", "r", encoding="utf-8") as file:
    msg_fem = file.read()

# 📌 Configuração do navegador
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=./whatsapp_profile")  # Mantém login salvo
driver = webdriver.Chrome(options=options)

# 🔗 Abrir WhatsApp Web
driver.get("https://web.whatsapp.com")
input("Pressione Enter após escanear o QR Code...")  # Aguarda login manual

# ⏳ Tempo de espera para garantir que a página carregue
time.sleep(10)

# 📌 Função para esperar a confirmação de envio da mensagem
def esperar_envio():
    max_tempo = 20  # Tempo máximo de espera (segundos)
    tempo_esperado = 0

    while tempo_esperado < max_tempo:
        try:
            # Se o botão de envio ainda estiver visível, aguarde
            send_button = driver.find_elements(By.XPATH, "//span[@data-icon='send']")
            if not send_button:  # Se não encontrou o botão, significa que a mensagem foi enviada
                return True
        except:
            pass

        time.sleep(1)
        tempo_esperado += 1

    print("⚠️ Tempo limite atingido. Prosseguindo para o próximo envio.")
    return False  # Se passou do tempo, continua o programa

# 📌 Contador de progresso
total_mensagens = len(df)
mensagens_enviadas = 0
mensagens_erros = 0

# 📌 Iterar sobre cada linha do CSV para enviar mensagens personalizadas
for index, row in df.iterrows():
    numero = row["TelefoneV"]
    nome_veterano = row["Veterano"].split()[0] 
    nome_calouro = row["Calouro"]
    grr_calouro = row["GRR"]
    genero_veterano = row["GeneroV"]

    # 🔹 Escolher a mensagem correta com as variáveis preenchidas
    if genero_veterano == "Masculino":
        mensagem = msg_masc.format(nome_veterano=nome_veterano, nome_calouro=nome_calouro, grr_calouro=grr_calouro)
    else:
        mensagem = msg_fem.format(nome_veterano=nome_veterano, nome_calouro=nome_calouro, grr_calouro=grr_calouro)

    # 🔄 Substituir quebras de linha por %0A para funcionar no WhatsApp Web
    mensagem = urllib.parse.quote(mensagem)
    
    # 🔗 Abrir a conversa no WhatsApp Web
    driver.get(f"https://web.whatsapp.com/send?phone={numero}&text={mensagem}")
    time.sleep(20)  # Esperar carregamento

    try:
        # 📩 Tentar encontrar e clicar no botão de envio
        send_button = driver.find_element(By.XPATH, "//span[@data-icon='send']")
        send_button.click()
        time.sleep(5)
        print(f"✅ Mensagem enviada para {nome_veterano} ({numero})")

        # 🕒 Esperar a confirmação do envio antes de prosseguir
        if esperar_envio():
            mensagens_enviadas += 1
            print(f"✅ Confirmação de envio recebida para {nome_veterano} ({numero})!")
        else:
            mensagens_erros += 1
            print(f"⚠️ Mensagem para {nome_veterano} pode não ter sido enviada corretamente.")

    except Exception as e:
        mensagens_erros += 1
        print(f"⚠️ Erro ao enviar mensagem para {nome_veterano} ({numero})")

    # 📊 Mostrar progresso
    print(f"📨 {mensagens_enviadas} mensagens enviadas e {mensagens_erros} mensagens não enviadas ({mensagens_enviadas + mensagens_erros}) de {total_mensagens}")


# ⏳ Aguardar antes de fechar
time.sleep(5)
driver.quit()

print("🚀 Envio de mensagens concluído!")
