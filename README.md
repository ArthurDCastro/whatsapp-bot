# WhatsApp Bot

## Overview

A Python script that uses Selenium to send personalized WhatsApp Web messages for a university peer mentorship program (*apadrinhamento*). Senior students act as mentors (*padrinhos* and *madrinhas*) to help incoming students settle into university life. The script notifies mentors of their assigned incoming student; it does not generate the assignments.

Created by Arthur from CAAD. The included Portuguese message templates reflect the original program context.

## Features

- Reads existing mentor–student assignments from a CSV file.
- Personalizes messages with the mentor’s first name, the incoming student’s full name, and their GRR (student registration identifier).
- Selects between two message templates based on the mentor’s gender field.
- Preserves line breaks and emojis through URL encoding.
- Saves the browser session locally and reports progress and error counts in the terminal.

## Technologies

- Python 3
- pandas for CSV processing
- Selenium WebDriver and Google Chrome for browser automation
- Python standard library: `time` and `urllib.parse`

## Requirements

- Python 3 with `pip` and Google Chrome installed.
- A working Selenium/Chrome WebDriver setup; no dependency versions are pinned in this repository.
- Internet access and a WhatsApp account that can sign in to WhatsApp Web.
- An authorized recipient list and reviewed message templates.

## Installation

From the repository directory, optionally create and activate a virtual environment:

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell (alternative)
# .venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
python -m pip install selenium pandas
```

## Usage

1. Populate `sorteio_apadrinhamento.csv` using the format below. The included file contains only headers.
2. Review `masc.txt` and `fem.txt` before sending. Replace the original sender attribution and event details, including relative dates such as “tomorrow.” Both files must remain UTF-8 encoded.
3. Run the script from the repository directory so it can find the CSV and templates:

   ```bash
   python bot.py
   ```

4. In the Chrome window, scan the WhatsApp Web QR code if required. Once logged in, press Enter in the terminal at the Portuguese prompt.
5. The script processes every CSV row and clicks Send automatically. Monitor the browser and terminal; there is no per-message approval. Chrome closes when processing finishes normally.

Both templates support the following placeholders:

| Placeholder | Value |
| --- | --- |
| `{nome_veterano}` | First word of `Veterano` |
| `{nome_calouro}` | Full `Calouro` value |
| `{grr_calouro}` | `GRR` value |

Example template (fictional context):

```text
Hello, {nome_veterano}!
Your assigned student is {nome_calouro} (student ID: {grr_calouro}).
Welcome to the fictional Example University mentorship program!
```

The script stores browser data in `./whatsapp_profile` to retain login state. Keep this directory private and out of version control, along with populated recipient files and terminal logs containing names and phone numbers. The repository currently has no `.gitignore`.

## CSV Format

Use a comma-separated file named `sorteio_apadrinhamento.csv` with these exact headers:

```csv
GRR,Calouro,GeneroC,Veterano,TelefoneV,GeneroV
GRR00000001,Alex Example,Masculino,Jordan Sample,12025550101,Masculino
```

All example values are fictional; the phone number is a fictional North American example, not a test recipient. Replace it only with an authorized recipient’s actual number before sending.

| Column | Meaning / behavior |
| --- | --- |
| `GRR` | Incoming student’s registration identifier, inserted into the message. |
| `Calouro` | Incoming student’s full name. |
| `GeneroC` | Incoming student’s gender; included in the supplied schema but unused by the script. |
| `Veterano` | Mentor’s name; only the first word is used in the greeting. |
| `TelefoneV` | Mentor’s phone number in international digits-only format, including country code, without `+`, spaces, or punctuation. |
| `GeneroV` | Exact value `Masculino` selects `masc.txt`; every other value selects `fem.txt`. |

The script reads values as strings and removes a trailing `.0` from phone numbers. It does not otherwise validate or normalize numbers. Keep required values populated and verify template wording: references to the incoming student’s gender are fixed in the templates and are not chosen using `GeneroC`.

## Limitations

- WhatsApp Web interface changes can break the XPath selector used to find the Send button. Fixed waits (10 seconds after login, 20 seconds per conversation, and 5 seconds after clicking Send) may be insufficient on slow connections.
- The script polls for up to 20 seconds for the Send button to disappear. This is only a UI heuristic, not proof of server acceptance, delivery, or reading. A timeout counts as an error and processing continues.
- There is no dry-run mode, retry mechanism, deduplication, or resume tracking. Running the script again can resend messages to all rows.
- Invalid or missing data, template placeholders, or setup failures can stop execution; only the send-button interaction has per-recipient exception handling.
- Names and phone numbers appear in terminal output. CSV files can contain student identifiers and contact details, and the saved browser profile may contain authenticated session data.
- This is unofficial browser automation, not an integration with the official WhatsApp Business Platform. Automated messaging can violate WhatsApp’s rules and lead to account restrictions or bans; fixed delays and recipient consent do not guarantee compliance. Review [WhatsApp’s responsible-use guidance](https://faq.whatsapp.com/361005896189245/) before considering use.

## Disclaimer

This repository documents a university mentorship automation project and is not affiliated with or endorsed by WhatsApp or Meta. Use only where permitted by the platform’s current rules, with recipients’ permission and authorization to share student information. Avoid unsolicited or bulk messaging, honor opt-outs, and do not bypass platform safeguards. Keep personal data and session files private, and consider official, authorized messaging tools for operational use.
