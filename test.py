import unittest


## Unit & Integrations Tests File

# BASIC TESTS FOR THE UTITLITY SCRIPT
from utils import *


class TestUtility:
    def test_get_string(self):
        text = "你好世界"
        lang = "en"
        res = get_string(text, lang)
        assert text != res
        assert res.lower() == "hello world"
        assert res is not None

    def test_get_collection(self):
        accounts = db_client.get_collection("accounts")
        assert accounts != None

    def test_get_account(self):
        user, _ = db_client.get_account("123123")
        assert user != None

    def test_get_account_by_ref(self):
        user = db_client.get_account_by_ref("000000")
        assert user != None

    def test_save_account(self):
        pass

    def test_save_ref(self):
        pass
