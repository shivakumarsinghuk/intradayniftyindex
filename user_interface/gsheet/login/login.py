# -*- coding: utf-8 -*-
"""
login_types.py
"""
import sys
sys.path.append('../interfaces')   # path to directory containing helper.py

from interfaces.Iuser_Interface import *
from datatypes.login_types import *
from utility.gsheet_utility import *

BROKER_DATA_INDEX = 0
USER_ID_INDEX = 1
PW_INDEX = 2
API_KEY_INDEX = 3
API_SECRET_KEY_INDEX = 4
PHONE_NO_INDEX = 5
TOTP_KEY_INDEX = 6

class UserInterfaceLogin(IUserInterface):

    def __init__(self, key):
        self.data = None
        #optionstraddle-521182d6265d.json
        self.googlesheet_utility = gsheet_utility(account_file=key,
                                                  spread_sheet_name="ORB_Nifty_Index")
        self.gworksheet_brokerdata = self.googlesheet_utility.get_work_sheet("BrokerData")
        self.__set_data()

    def get_data(self):
        return self.data


    def __set_data(self):
        data = self.gworksheet_brokerdata.get_all_values()  # All rows as a list of lists
        lst_data = []
        # Example: Read rows 2–4, columns 1–3
        subset = [row[0:3] for row in data[1:8]]
        for r in subset:
            lst_data.append(r[1])
        obj_trade_login_data = LogInData(lst_data[BROKER_DATA_INDEX], lst_data[USER_ID_INDEX], lst_data[PW_INDEX], \
                                   lst_data[API_KEY_INDEX], lst_data[API_SECRET_KEY_INDEX], lst_data[PHONE_NO_INDEX], \
                                   lst_data[TOTP_KEY_INDEX])

        # Rows 1–8 → data[0:8]
        # Column D → index 3
        subset = [row[3] for row in data[1:8]]
        lst_data.clear()
        for val in subset:
            lst_data.append(val)

        obj_option_chain_login_data = LogInData(lst_data[BROKER_DATA_INDEX], lst_data[USER_ID_INDEX], lst_data[PW_INDEX], \
                                   lst_data[API_KEY_INDEX], lst_data[API_SECRET_KEY_INDEX], lst_data[PHONE_NO_INDEX], \
                                   lst_data[TOTP_KEY_INDEX])

        self.data = obj_trade_login_data, obj_option_chain_login_data





