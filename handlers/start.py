from config import *
from utils import *


def start_menu(status: bool):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    a = types.InlineKeyboardButton(
        text=get_string("Open Website", LANGUAGE), url="www.google.com"
    )

    b = types.InlineKeyboardButton(
        text=get_string("Login Account", LANGUAGE), callback_data="login"
    )

    if status == False:
        keyboard.add(a)
    else:
        keyboard.add(a, b)
    return keyboard


def start_menu2(status: bool):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    a = types.InlineKeyboardButton(
        text=get_string("Register Account", LANGUAGE), callback_data="register"
    )
    b = types.InlineKeyboardButton(
        text=get_string("Share Invitation", LANGUAGE), callback_data="invite"
    )
    c = types.InlineKeyboardButton(
        text=get_string("Contact Agent", LANGUAGE), callback_data="contact"
    )
    d = types.InlineKeyboardButton(
        text=get_string("Main Menu", LANGUAGE), callback_data="back"
    )
    e = types.InlineKeyboardButton(
        text=get_string("Activate Your Invitation", LANGUAGE), callback_data="invite"
    )
    if status:
        keyboard.add(a, b, c, d)
    else:
        keyboard.add(e)

    return keyboard


@bot.message_handler(regexp="Start")
@bot.message_handler(commands=["start"])
def startbot(msg):
    "Ignites the bot application to take action"

    bot.send_chat_action(msg.from_user.id, "typing")
    # check user in the database to see if they registered
    user, _ = db_client.get_account(msg.from_user.id)

    if hasattr(msg, "message_id"):
        chat, m_id = get_received_msg(msg)
        bot.delete_message(chat.id, m_id)

    if user == None:
        bot.send_photo(
            msg.from_user.id,
            photo="https://ibb.co/nm9NTpZ",
            caption=get_string(
                f"🤡 Welcome {msg.from_user.first_name}, \n\nIf you are invited, follow these instructions; \n\n- Click /invitecode or  button below \n- Enter your invitation code \n\nFor access to all the bot's services and commands.",
                LANGUAGE,
            ),
            reply_markup=start_menu2(False),
            parse_mode="html",
        )

        bot.send_photo(
            msg.from_user.id,
            photo="https://ibb.co/J3Q7Q8k",
            allow_sending_without_reply=True,
        )

    else:

        bot.send_photo(
            msg.from_user.id,
            photo="https://ibb.co/nm9NTpZ",
            caption=get_string(
                f"Welcome Back <b>{user.nickname} ({user.account_type})</b>,\n\n\
                    \nClick /start to display default menu\n\nGet Yourself familiar by joining the invite room for more info and news update.",
                LANGUAGE,
            ),
            reply_markup=start_menu(True),
            parse_mode="html",
        )

        bot.send_photo(
            msg.from_user.id,
            photo="https://ibb.co/mXBzyt8",
            allow_sending_without_reply=True,
        )

        bot.send_chat_action(msg.from_user.id, "typing")
        bot.send_video(
            msg.from_user.id,
            video=open("assets/vid2.mp4", "rb"),
            supports_streaming=True,
            allow_sending_without_reply=True,
            reply_markup=start_menu2(True),
        )

        bot.send_photo(
            msg.from_user.id,
            photo="https://ibb.co/J3Q7Q8k",
            allow_sending_without_reply=True,
        )


@bot.message_handler(regexp="^Back")
def startbotn(msg):
    startbot(msg)


# photo='https://ibb.co/nm9NTpZ', - INLINE TOP

# https://ibb.co/mXBzyt8 - INLINE MIDDLE
# https://ibb.co/J3Q7Q8k - INLINE BOTOM


# https://ibb.co/C6vztBZ - INVITATION


# https://ibb.co/pfHDP4v - BIG LAMP
