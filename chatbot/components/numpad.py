from telegram import (
  InlineKeyboardButton,
  InlineKeyboardMarkup
)


def create_numpad(amount: int) -> InlineKeyboardMarkup:
  numpad = InlineKeyboardMarkup([
    [InlineKeyboardButton(f'Rp {amount:,}'.replace(",", "."), callback_data=f"amount={amount}")],
    [
      InlineKeyboardButton("1", callback_data=f"amount={str(amount) + '1'}"),
      InlineKeyboardButton("2", callback_data=f"amount={str(amount) + '2'}"),
      InlineKeyboardButton("3", callback_data=f"amount={str(amount) + '3'}")
    ],
    [
      InlineKeyboardButton("4", callback_data=f"amount={str(amount) + '4'}"),
      InlineKeyboardButton("5", callback_data=f"amount={str(amount) + '5'}"),
      InlineKeyboardButton("6", callback_data=f"amount={str(amount) + '6'}")
    ],
    [
      InlineKeyboardButton("7", callback_data=f"amount={str(amount) + '7'}"),
      InlineKeyboardButton("8", callback_data=f"amount={str(amount) + '8'}"),
      InlineKeyboardButton("9", callback_data=f"amount={str(amount) + '9'}")
    ],
    [
      InlineKeyboardButton("000", callback_data=f"amount={str(amount) + '000'}"),
      InlineKeyboardButton("0", callback_data=f"amount={str(amount) + '0'}"),
      InlineKeyboardButton("C", callback_data=f"amount={str(amount)[:-1] if len(str(amount)) > 1 else '0'}")
    ],
    [InlineKeyboardButton("Enter", callback_data=f"ok;amount={str(amount)}")]
  ])
  return numpad
