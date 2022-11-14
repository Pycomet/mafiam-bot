from config import *
from utils import *


def validation_menu():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    a = types.InlineKeyboardButton(
        text=get_string("Join Channel", LANGUAGE), callback_data="join"
    )
    keyboard.add(a)
    return keyboard


@bot.message_handler(regexp="Login")
def login_user(msg):
    "Logs In A User To Gain Access"

    bot.send_chat_action(msg.from_user.id, "typing")
    user, _ = db_client.get_account(msg.from_user.id)

    if hasattr(msg, "message_id"):
        chat, m_id = get_received_msg(msg)
        bot.delete_message(chat.id, m_id)

    if user == None:
        bot.send_photo(
            msg.from_user.id,
            photo="https://ibb.co/nm9NTpZ",
            caption=get_string(
                "<b>🤵 Your account is registered, please seek an invitation from an existing user.</b> \n\nPlease try again.",
                LANGUAGE,
            ),
            parse_mode="html"
        )
    else:

        question = bot.send_photo(
            msg.from_user.id,
            photo="https://iili.io/yf6cNV.md.jpg",
            caption=get_string(
                "Please answer the question below to gain access; \n\n<b>{user.secret_question} ?</b>"
            ),
            parse_mode="html"
        )

        bot.register_next_step_handler(question, validate_answer)


def validate_answer(msg):
    answer = msg.text
    chat, m_id = get_received_msg(msg)
    user, _ = db_client.get_account(msg.from_user.id)

    # Delete prev question
    bot.delete_message(chat.id, m_id - 1)
    bot.send_chat_action(msg.from_user.id, "typing")

    # Validate the answer given
    if user.secret_answer == answer:
        bot.delete_message(chat.id, m_id)

        # Set User State To True
        db_client.update_account(
            msg.from_user.id, {"active": True}
        )

        bot.send_photo(
            msg.from_user.id,
            photo="https://ibb.co/nm9NTpZ",
            caption=get_string(
                "<b>🍷 Welcome back {user.nickname} </b> \n\n Your login session ends in 30 minutes. \n\nClick 'Join' to get access to the store channel."
            ),
            reply_marku=validation_menu(),
            parse_mode="html"
        )

    else:
        bot.delete_message(chat.id, m_id)
        bot.send_chat_action(msg.from_user.id, "typing")

        bot.send_photo(
            msg.from_user.id,
            photo="https://ibb.co/nm9NTpZ",
            caption=get_string(
                "<b>🤵 Wrong Answer!</b> \n\n Try to log in again, Click /start ",
                LANGUAGE,
            ),
            parse_mode="html"
        )

# Get anwer to secret question -

# Set active status to true -

# Generate invite link (10 seconds)

# Set scheduler to remove user in 30 minutes

# Send user session timeout message


@bot.message_handler(regexp="Logout")
def logout_user(msg):
    "Logs Out A User's Access"

    pass
