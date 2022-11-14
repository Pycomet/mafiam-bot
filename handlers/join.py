from config import *
from utils import *


def join_chat(msg):
    "Logs In A User To Gain Access"

    bot.send_chat_action(msg.from_user.id, "typing")
    user, _ = db_client.get_account(msg.from_user.id)

    if hasattr(msg, "message_id"):
        chat, m_id = get_received_msg(msg)
        bot.delete_message(chat.id, m_id)

    if user.active == False:
        bot.send_photo(
            msg.from_user.id,
            photo="https://ibb.co/nm9NTpZ",
            caption=get_string(
                "<b>🤵 Invalid access rights! Login in again.</b>",
                LANGUAGE,
            ),
            parse_mode="html"
        )

    else:

        # Generate invite link (10 seconds)

        # Set scheduler to remove user in 30 minutes

        # Send user session timeout message

        pass
