from telegram import (
  InlineKeyboardButton,
  InlineKeyboardMarkup
)


def create_confirmation() -> InlineKeyboardMarkup:
  confirmation = InlineKeyboardMarkup([
    [
      InlineKeyboardButton("Yes", callback_data="confirmation=Yes"),
      InlineKeyboardButton("No", callback_data="confirmation=No")
    ]
  ])
  return confirmation