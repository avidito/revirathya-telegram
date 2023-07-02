from telegram.ext import (
  CallbackQueryHandler,
  CommandHandler,
  ConversationHandler,
  MessageHandler,
  filters
)

from conversation.transaction import handler, constant


conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("transaction", handler.transaction_command)],
    states={
      constant.STATES["transaction_branch_command"]: [
        CallbackQueryHandler(handler.transaction_add_category, pattern="command=Add")
      ],
      constant.STATES["transaction_add_branch_category"]: [
        CallbackQueryHandler(handler.transaction_add_amount, pattern="category=")
      ],
      constant.STATES["transaction_add_loop_amount"]: [
        CallbackQueryHandler(handler.transaction_add_amount_loop, pattern="amount="),
        CallbackQueryHandler(handler.transaction_add_description, pattern="ok")
      ],
      constant.STATES["transaction_add_branch_description"]: [
        MessageHandler(filters.TEXT & ~filters.COMMAND, handler.transaction_add_confirmation)
      ],
      constant.STATES["transaction_add_branch_confirmation"]: [
        CallbackQueryHandler(handler.transaction_add_closing, pattern="confirmation=")
      ]
    },
    fallbacks=[CommandHandler("transaction", handler.transaction_command)]
  )