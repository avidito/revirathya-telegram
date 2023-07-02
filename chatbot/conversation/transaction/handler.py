from telegram import (
  InlineKeyboardButton,
  InlineKeyboardMarkup,
  Update
)
from telegram.ext import (
  ContextTypes,
  ConversationHandler
)
from telegram.constants import ParseMode

from components import numpad, confirmation
from conversation.transaction import constant


# Utils
def create_reply(data: dict, message: str):
  opening = "<b>Adding New Transaction</b>"
  payload = "\n".join([
    f"""{col.title()}: {data[col] if col != 'amount' else f"{data[col]:,}".replace(",", ".")}"""
    for col in [
      "date",
      "category",
      "amount",
      "description"
    ]
    if col in data.keys()
  ])

  reply_text_token = [opening, "", payload, "", message] if (payload) else [opening, "", message]
  reply_text = "\n".join(reply_text_token)
  return reply_text


# Handler
async def transaction_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  keyboard = InlineKeyboardMarkup([
    [
      InlineKeyboardButton("add", callback_data="command=Add"),
      InlineKeyboardButton("List", callback_data="command=List"),
    ],
    [
      InlineKeyboardButton("Edit", callback_data="command=Edit"),
      InlineKeyboardButton("Remove", callback_data="command=Remove"),
    ],
  ])

  await update.message.reply_html(
    "<b>What do you want to do with transaction</b>?",
    reply_markup=keyboard
  )

  return constant.STATES["transaction_branch_command"]


async def transaction_add_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  query = update.callback_query
  command = query.data.split("=")[-1]
  context.user_data["command"] = command
  context.user_data[command.lower()] = {}

  keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton(category, callback_data=f"category={category}")]
    for category in constant.CATEGORIES
  ])
  await query.answer()
  await query.edit_message_text(
    text=create_reply(context.user_data[command.lower()], "Input category of transaction:"),
    parse_mode=ParseMode.HTML,
    reply_markup=keyboard
  )

  return constant.STATES["transaction_add_branch_category"]


async def transaction_add_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  query = update.callback_query
  context.user_data["add"]["category"] = query.data.split("=")[-1]

  keyboard = numpad.create_numpad(amount=0)
  await query.answer()
  await query.edit_message_text(
    text=create_reply(context.user_data["add"], "Input amount of transaction:"),
    parse_mode=ParseMode.HTML,
    reply_markup=keyboard
  )

  return constant.STATES["transaction_add_loop_amount"]


async def transaction_add_amount_loop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  query = update.callback_query
  context.user_data["add"]["amount"] = int(query.data.split("=")[-1])

  keyboard = numpad.create_numpad(amount=context.user_data["add"]["amount"])
  await query.answer()
  await query.edit_message_text(
    text=create_reply(context.user_data["add"], "Input amount of transaction:"),
    parse_mode=ParseMode.HTML,
    reply_markup=keyboard
  )

  return constant.STATES["transaction_add_loop_amount"]


async def transaction_add_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  query = update.callback_query
  context.user_data["add"]["amount"] = int(query.data.split("=")[-1])
  context.user_data["message_id"] = update.callback_query.message.id

  await query.answer()
  await query.edit_message_text(
    text=create_reply(context.user_data["add"], "Input description of transaction:"),
    parse_mode=ParseMode.HTML
  )

  return constant.STATES["transaction_add_branch_description"]


async def transaction_add_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  context.user_data["add"]["description"] = update.message.text

  keyboard = confirmation.create_confirmation()
  await context.bot.edit_message_text(
    chat_id=update.message.chat_id,
    message_id=context.user_data["message_id"],
    text=create_reply(context.user_data["add"], "Are you sure to input this transaction?"),
    reply_markup=keyboard,
    parse_mode=ParseMode.HTML
  )

  del context.user_data["message_id"]
  return constant.STATES["transaction_add_branch_confirmation"]


async def transaction_add_closing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  query = update.callback_query
  confirm_text = query.data.split("=")[-1]
  confirm_message = "<b>Sucessfully add new transaction!</b>" if (confirm_text == "Yes") else "<b>Cancel adding new transaction!</b>"

  await query.answer()
  await query.edit_message_text(
    text=create_reply(context.user_data["add"], confirm_message),
    parse_mode=ParseMode.HTML
  )

  del context.user_data["command"]
  del context.user_data["add"]
  return ConversationHandler.END