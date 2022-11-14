from config import *
from utils import *
from .register import register_user
from .invite import invite_user
from .start import startbot
from .auth import login_user, logout_user
from .join import join_chat
# Callback Handlers For Menu Button


@bot.callback_query_handler(
    func=lambda c: c.data in ["register", "invite",
                              "contact", "back", "login", "logout", "join"]
)
def button_callback_answer(call):
    """
    Button Response
    """

    bot.send_chat_action(call.from_user.id, "typing")
    # ADDING THE GENDER
    if call.data == "register":
        # Delete prev question
        bot.delete_message(call.from_user.id, call.message.message_id)

        register_user(call)

    elif call.data == "invite":
        # Delete prev question
        bot.delete_message(call.from_user.id, call.message.message_id)

        invite_user(call)

    elif call.data == "contact":
        # Delete prev question
        bot.delete_message(call.from_user.id, call.message.message_id)

        print("No contact yet")

    elif call.data == "back":
        # Delete prev question
        bot.delete_message(call.from_user.id, call.message.message_id)

        startbot(call)

    # LOGIN PORTAL
    elif call.data == "login":
        # Delete prev question
        bot.delete_message(call.from_user.id, call.message.message_id)

        login_user(call)

    # LOGOUT PORTAL
    elif call.data == "logout":
        # Delete prev question
        bot.delete_message(call.from_user.id, call.message.message_id)

        logout_user(call)

    elif call.data == "join":
        # Delete prev question
        bot.delete_message(call.from_user.id, call.message.message_id)

        join_chat(call)

    else:
        pass
