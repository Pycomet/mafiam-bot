from config import *
from models import *


def get_string(text: str, lang: str) -> str:
    "Return The Test In LangugaE String"
    try:
        if lang == "ja":
            result = translator.translate(text)
            return result
        else:
            return text
    except:
        return text


def get_received_msg(msg):
    "Delete This Message"
    message_id = msg.message_id
    chat = msg.chat
    return chat, message_id


class DbClient:
    def get_collection(self, name: str):
        "Returns The Collections Document (Query by - name)"
        res = client["mafiambot_db"][name]
        return res

    def get_account(self, user_id: str):
        "Get Account Object"
        collection = self.get_collection("accounts")
        result = collection.find_one({"userId": int(user_id)})  # Checker
        if result == None:
            return None, None

        # Get Obj
        res = Account.from_dict(result)
        return res, result["_id"]

    def get_account_by_ref(self, code: str) -> Referral or None:
        "This fetched the user by referral code"
        collection = self.get_collection("accounts")
        result = collection.find_one({"code": code})  # Checker
        if result == None:
            return None

        # Get Obj
        res = Account.from_dict(result)
        return res

    def save_account(self, account: Account) -> bool:
        "Saves Account Object To MongoDb"

        collection = self.get_collection("accounts")

        # Write To Collection
        result = collection.find_one({"userId": account.user_id})  # Checker

        if result == None:
            data = account.to_dict()
            collection.insert_one(data)
            return True

        return False

    def save_ref(self, referral: Referral) -> bool:
        "This Registers A New Referral"
        try:
            collection = self.get_collection("referrals")
            data = referral.to_dict()
            collection.insert_one(data)
            return True

        except Exception:
            return False

    def update_account(self, user_id: int, data: object) -> bool:
        "Update A Certain Account"

        user, _ = self.get_account(user_id)

        if user == None:
            return False

        collection = self.get_collection("accounts")
        collection.update_one({"userId": user_id}, {"$set": data})
        return True


db_client = DbClient()
