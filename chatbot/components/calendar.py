from datetime import date
from telegram import (
  InlineKeyboardButton,
  InlineKeyboardMarkup
)

def date_payload(dt: date) -> str:
    return dt.strftime("%Y-%m-%d")


def create_calendar(dt: date) -> InlineKeyboardMarkup:
    month_label = dt.strftime("%b %Y")
    calendar = InlineKeyboardMarkup([
        [InlineKeyboardButton(month_label, callback_data=f"date={date_payload(dt)}")],
        
    ])