from config import *
from utils import *


def menu5():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    a = types.InlineKeyboardButton(text="English - EN", callback_data="en")
    b = types.InlineKeyboardButton(
        text=get_string("Japanese - JA", "ja"), callback_data="ja"
    )
    keyboard.add(a, b)
    return keyboard


@bot.message_handler(commands=["lang"])
def startRef(msg):
    bot.reply_to(
        msg,
        get_string("<b>Pick Your Preferred Language ?</b>", LANGUAGE),
        parse_mode="html",
        reply_markup=menu5(),
    )


# Callback Handlers
@bot.callback_query_handler(func=lambda c: c.data in ["en", "zh"])
def lang_callback_answer(call):
    """
    Button Response
    """

    bot.send_chat_action(call.from_user.id, "typing")

    if call.data == "en":
        user.language = "en"
        LANGUAGE = user.language

    elif call.data == "ja":
        user.language = "ja"
        LANGUAGE = user.language

    else:
        pass
