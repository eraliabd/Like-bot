from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ConversationHandler
from telegram import (
    InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, ChatAction
)

CHANNEL_ID = -1001736766540
TOKEN = "5358957794:AAGjOAwGD1cAsFTD470LsbypxhsqjMv4DSM"
GLOBAL_LIKES = 0
GLOBAL_DISLIKES = 0

def start_handler(update, context):
    context.bot.send_message(
        chat_id=CHANNEL_ID,
        text="😁 Like or 😠 Dislike",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="👍", callback_data="like"),
                    InlineKeyboardButton(text="👎🏿", callback_data="dislike")
                ]
            ]
        )
    )
    update.message.reply_text(
        text="Xabar jo'natildi!",
    )

def message_handler(update, context):
    pass

def inline_handler(update, context):
    query = update.callback_query

    global GLOBAL_LIKES, GLOBAL_DISLIKES

    if query.data == "like":
        if context.user_data.get('choice') == "dislike":
            GLOBAL_DISLIKES -= 1

        if context.user_data.get('choice') != "like":
            GLOBAL_LIKES += 1


        context.user_data["choice"] = "like"

    elif query.data == "dislike":

        if context.user_data.get('choice') == "like":
            GLOBAL_LIKES -= 1

        if context.user_data.get('choice') != "dislike":
            GLOBAL_DISLIKES += 1

        context.user_data["choice"] = "dislike"

    try:
        context.bot.edit_message_reply_markup(
            chat_id=CHANNEL_ID,
            message_id=query.message.message_id,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=f"{GLOBAL_LIKES} 👍", callback_data=f"like"),
                        InlineKeyboardButton(text=f"👎🏿 {GLOBAL_DISLIKES}", callback_data=f"dislike")
                    ]
                ]
            )
        )
    except Exception as e:
        print(e)


def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_handler))
    dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
    dispatcher.add_handler(CallbackQueryHandler(inline_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
