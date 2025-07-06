
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
from bs4 import BeautifulSoup
import os

TOKEN = os.getenv("BOT_TOKEN")

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Ассалому алайкум! ИНН юборинг, лицензия PDF топиб бераман.")

def get_license_pdf(inn):
    search_url = f"https://license.gov.uz/search?inn={inn}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    pdf_link = soup.find("a", href=lambda href: href and href.endswith(".pdf"))
    if pdf_link:
        return pdf_link['href']
    return None

def handle_message(update: Update, context: CallbackContext):
    inn = update.message.text.strip()
    update.message.reply_text(f"{inn} учун маълумот изланмоқда...")
    pdf_url = get_license_pdf(inn)
    if pdf_url:
        update.message.reply_document(pdf_url)
    else:
        update.message.reply_text("Лицензия PDF топилмади.")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
