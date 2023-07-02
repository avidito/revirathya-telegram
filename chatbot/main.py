import os
import logging

from telegram import Update
from telegram.ext import Application

from conversation import transaction

from warnings import filterwarnings
from telegram.warnings import PTBUserWarning
filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)

# Secret
BOT_TOKEN = os.environ.get("BOT_TOKEN")


# Main
def main():
  app = Application.builder().token(BOT_TOKEN).build()

  # Handler
  app.add_handler(transaction.conversation_handler)
  
  # Polling
  app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
  logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
  )
  
  main()