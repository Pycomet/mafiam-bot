from config import *
from utils import *
from models import Account


def gender_menu():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    a = types.InlineKeyboardButton(text="🚹  Male", callback_data="male")
    b = types.InlineKeyboardButton(text="🚺 Female", callback_data="female")
    keyboard.add(a, b)
    return keyboard


type_options = ["個人のお客様", "メーカー様", "卸業者様",
                "不定期小売店", "特殊案件", "個人メーカー", "経営者", "紹介業者"]


def type_menu():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=get_string(
        each, LANGUAGE), callback_data=each) for each in type_options]
    [keyboard.add(button) for button in buttons]
    return keyboard


def register_menu():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    a = types.InlineKeyboardButton(
        text="同意して次へ (Agree and Continue)", callback_data="continue")
    b = types.InlineKeyboardButton(text="辞める (Quit)", callback_data="quit")
    keyboard.add(a, b)
    return keyboard


@bot.message_handler(commands=["register"])
def register_user(msg):
    "Register Msg Handler"

    if hasattr(msg, "message_id"):
        chat, m_id = get_received_msg(msg)
        bot.delete_message(chat.id, m_id)

    bot.send_chat_action(msg.from_user.id, "typing")

    bot.send_photo(
        msg.from_user.id,
        photo="https://ibb.co/nm9NTpZ",
        caption=get_string(
            "🤡<b><u>Agreement/Confirmation</u></b>",
            LANGUAGE,
        ),
        parse_mode="html"
    )

    bot.send_chat_action(msg.from_user.id, "typing")
    bot.send_photo(
        msg.from_user.id,
        photo="https://ibb.co/mXBzyt8",
        allow_sending_without_reply=True,
    )

    bot.send_message(
        msg.from_user.id,
        get_string("\n\n・We are a <b>secret jewelery store</b> that <u>mainly operates within the 23 wards of Tokyo</u> and allows local delivery. \
            \n\n・This shop is a <u>invitation (introduction) only</u>, and <b>a membership service for good customers</b>. \
            \n\n・With <b>military-level security</b>, <u>information sent from customers</u> will be It is <b>100% privacy guaranteed</b> as it is sent to a server in a legal country and all content is \
            \n<b>securely</b> erased after the transaction is completed. All information that could lead to identification is not stored securely. \
            \n\n・All customers are <u>selected by our own screening</u> and then invited to <b>excellent credit customers</b> and only <u>their referrals. </u> will be used. \
            \n\n・In consideration of the safety of information leakage, customers who have been detained by arrest for various reasons, or who have not made transactions for a certain period of time, may be subject to temporary withdrawal by data separation. (It will be restored by contacting the customer.) \
            \n\n・Due to the nature of the membership service, it is strictly prohibited to disclose the details of the service to anyone other than the introducer/member of our shop. \
            \n\n・New customers <b>introduced by current members</b> cannot use <u>direct transactions</u>. \
            \n\nCurrently, we are not <u> direct dealings with customers other than those who are <b>directly invited by our shop</b>. </u> Please acknowledge it beforehand. \
            \n\n・A society that has cultivated order based on common sense knowledge will take time to accept the truth. \
            \n\n・Don't be impatient with changes in social values, please enjoy yourself smartly and modestly. \
            \n\n・ As a member privilege, you will be able to receive special preferential treatment at <b>permanently cheap prices</b> when you open a physical store in the future <u>domestic law revision</u> or overseas. \
            \n\n・If you agree to <b>all of the above</b>, please proceed to <u>next</u>.",
                   LANGUAGE,
                   ),
        parse_mode="html",
        reply_markup=register_menu()
    )

    bot.send_photo(
        msg.from_user.id,
        photo="https://ibb.co/J3Q7Q8k",
        allow_sending_without_reply=True,
    )


def get_name(msg):
    "Ask the gender of the user"

    name = msg.text
    chat, m_id = get_received_msg(msg)

    # Delete prev question
    bot.delete_message(chat.id, m_id - 1)

    if name == "":
        name = msg.from_user.first_name

    account = Account(name, int(msg.from_user.id))

    isNew = db_client.save_account(account)

    bot.delete_message(chat.id, m_id)

    bot.send_chat_action(msg.from_user.id, "typing")

    if isNew:
        bot.send_photo(
            msg.from_user.id,
            photo="https://ibb.co/mXBzyt8",
            caption=get_string(
                "Pick your gender from the options below 👇", LANGUAGE),
            reply_markup=gender_menu(),
        )

    else:
        bot.send_message(
            msg.from_user.id,
            get_string(
                "You are already a registered member! Move along", LANGUAGE),
        )


def get_type(msg):
    "Adds Account Type And Request Secret Question"
    account_type = msg.text
    chat, m_id = get_received_msg(msg)

    # Delete prev question
    bot.delete_message(chat.id, m_id - 1)

    status = db_client.update_account(
        msg.from_user.id, {"accountType": account_type}
    )
    print(f"Account status - {True}")

    bot.delete_message(chat.id, m_id)

    bot.send_chat_action(msg.from_user.id, "typing")

    question = bot.send_photo(
        msg.from_user.id,
        photo="https://ibb.co/mXBzyt8",
        caption=get_string(
            f"Enter your own custom secret question here👇 \n<b>(📌 write in a safe place)</b>\n<b>(📌 This question remains exclusive to you alone)</b>",
            LANGUAGE,
        ),
        parse_mode="html",
    )

    bot.register_next_step_handler(question, get_secret_question)


def get_secret_question(msg):
    "Ask Secret Question"
    secret_question = msg.text
    chat, m_id = get_received_msg(msg)

    # Delete prev question
    bot.delete_message(chat.id, m_id - 1)

    status = db_client.update_account(
        msg.from_user.id, {"secretQuestion": secret_question}
    )

    bot.delete_message(chat.id, m_id)

    bot.send_chat_action(msg.from_user.id, "typing")

    if status == True:
        question = bot.send_photo(
            msg.from_user.id,
            photo="https://ibb.co/mXBzyt8",
            caption=get_string(
                f"Enter the answer to your secret question👇 ", LANGUAGE),
        )

        bot.register_next_step_handler(question, get_secret_answer)
    else:
        print("An error occured update the secret question")
        logging.error("An error occured update the secret question")


def get_secret_answer(msg):
    answer = msg.text
    chat, m_id = get_received_msg(msg)

    # Delete prev question
    bot.delete_message(chat.id, m_id - 1)

    bot.send_chat_action(msg.from_user.id, "typing")

    status = db_client.update_account(
        msg.from_user.id, {"secretAnswer": answer})

    bot.delete_message(chat.id, m_id)

    bot.send_chat_action(msg.from_user.id, "upload_document")

    if status == True:
        user, u_id = db_client.get_account(msg.from_user.id)

        ref_code = str(u_id)[:6]
        db_client.update_account(msg.from_user.id, {"code": ref_code})

        bot.send_photo(
            msg.from_user.id,
            photo="https://ibb.co/nm9NTpZ",
            caption=get_string(
                f"🎉<b>Welcome to MAFIAM CLUB {user.nickname},🎉 \n\nClick /start to get started exploring...</b>",
                LANGUAGE,
            ),
            parse_mode="html",
        )

        bot.send_photo(
            msg.from_user.id,
            photo="https://ibb.co/J3Q7Q8k",
            allow_sending_without_reply=True,
        )
    else:
        print("An error occured update the secret answer")
        logging.error("An error occured update the secret answer")


# Callback Handlers
@bot.callback_query_handler(func=lambda c: c.data in [
    "male", "female", "continue", "quit",
    "個人のお客様", "メーカー様", "卸業者様", "不定期小売店",
    "特殊案件", "個人メーカー", "経営者", "紹介業者"
])
def register_callback_answer(call):
    """
    Button Response
    """

    bot.send_chat_action(call.from_user.id, "typing")
    # ADDING THE GENDER
    if call.data == "male" or call.data == "female":
        # Delete prev question
        bot.delete_message(call.from_user.id, call.message.message_id)

        status = db_client.update_account(
            call.from_user.id, {"sex": call.data})

        if status == True:

            bot.send_photo(
                call.from_user.id,
                photo="https://iili.io/ycPN7n.md.png",
                caption=get_string(
                    f"🤡 Choose about your customers. \
                        \n\n-------------------------- \
                        \n\nWe will provide services tailored to each customer, such as <b>small lot special menus</b> for individual customers and <b>useful information</b> for vendors. \
                        \n\nOnce selected, you can <b>change it at any time</b>.",
                    LANGUAGE,
                ),
                reply_markup=type_menu(),
                parse_mode="html",
            )

    elif call.data in type_options:
        # Delete prev question
        bot.delete_message(call.from_user.id, call.message.message_id)

        status = db_client.update_account(
            call.from_user.id, {"accountType": call.data})

        question = bot.send_photo(
            call.from_user.id,
            photo="https://iili.io/yEYeiN.md.png",
            caption=get_string(
                f"Enter your own custom secret question here👇 \n<b>(📌 write in a safe place)</b>\n<b>(📌 This question remains exclusive to you alone)</b>",
                LANGUAGE,
            ),
            parse_mode="html",
        )

        bot.register_next_step_handler(question, get_secret_question)

    elif call.data == "continue":

        bot.delete_message(call.from_user.id, call.message.message_id)

        question = bot.send_photo(
            call.from_user.id,
            photo="https://iili.io/ycPOes.md.png",
            caption=get_string("🤡 Choose a nickname for your store. \
                \n\n *Can be changed later. \
                \n *Press back to return to the previous question.", LANGUAGE),
        )

        bot.register_next_step_handler(question, get_name)

    elif call.data == "quit":

        bot.delete_message(call.from_user.id, call.message.message_id)

    else:
        print(call.data)
        print("invalid callback passed")
        pass
