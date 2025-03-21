# 🤖 WhatsApp Bot

Automação feita com Selenium para envio de mensagens personalizadas via WhatsApp Web durante o processo de apadrinhamento de calouros.

## 📂 Estrutura dos Arquivos

```
├── masc.txt                # Texto base para mensagem de padrinhos (masculino)
├── fem.txt                 # Texto base para mensagem de madrinhas (feminino)
├── sorteio_apadrinhamento.csv  # Arquivo com a lista de padrinhos e calouros
├── enviar_mensagens.py    # Script principal de envio
```

---

## 📄 Arquivos de Texto (`masc.txt` e `fem.txt`)

Esses arquivos contêm o corpo da mensagem que será enviada para os veteranos, com placeholders para personalização.  

### Variáveis disponíveis:
- `{nome_veterano}` – Primeiro nome do veterano
- `{nome_calouro}` – Nome completo do calouro
- `{grr_calouro}` – GRR do calouro

> Exemplo:
> ```
> 🎉 Fala, {nome_veterano}!
> Seu calouro é {nome_calouro} (GRR: {grr_calouro})
> ```

---

## 📄 Arquivo `sorteio_apadrinhamento.csv`

Esse CSV deve conter as seguintes colunas:

| GRR | Calouro | GeneroC | Veterano | TelefoneV | GeneroV |
|-----|---------|----------|----------|------------|----------|

- `TelefoneV` deve estar no formato internacional (ex: `5541999999999`)
- O script garante a personalização de acordo com o gênero do veterano (`GeneroV`) para escolher o texto correto.

---

## ▶️ Como usar

1. Instale os pacotes:
```bash
pip install selenium pandas
```

2. Execute o script:
```bash
python enviar_mensagens.py
```

3. Siga as instruções no terminal para escanear o QR code do WhatsApp Web.

---

## ⚠️ Avisos

- O WhatsApp Web precisa estar logado no navegador do Chrome.
- O script aguarda confirmação de envio antes de passar para a próxima mensagem.
- As mensagens são formatadas com quebras de linha e emojis 🎉.

---

## 📬 Autor
Criado por Arthur do CAAD 🐻
