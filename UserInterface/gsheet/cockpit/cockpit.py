# -*- coding: utf-8 -*-
"""
login_types.py
"""
import sys
import numpy as np
sys.path.append('../interfaces')   # path to directory containing helper.py

from interfaces.Iuser_Interface import *
from Utility.gsheet_utility import *
#from broker_platform.datatypes.trade_data import *
from Utility.utility import *

INDEX_DATA_INDEX = 0
BUY_TOTAL_PRICE_INDEX = 1
SELL_TOTAL_PRICE_INDEX = 2
TARGET_PERCENTAGE_INDEX = 3
STOP_LOSS_PERCENTAGE_INDEX = 4
QUANTITY_INDEX = 5
EXPIRY_BUY_INDEX = 7
EXPIRY_SELL_INDEX = 8
START_TIME_INDEX = 11
STOP_TIME_INDEX = 12

class UserInterfaceCockpitData(IUserInterface):

    def __init__(self, key):
        self.data = None
        self.googlesheet_utility = gsheet_utility(account_file=key,
                                                  spread_sheet_name="ORB_Nifty_Index")
        self.gworksheet_cockpit = self.googlesheet_utility.get_work_sheet("Cockpit")
        #reset the values
        self.update_prev_day_ohlc(0, 0, 0)
        self.update_prev_week_data(0, 0)

    def update_prev_day_ohlc(self, high_price, low_price, close_price):
        lst_data = [
            [high_price],
            [low_price],
            [close_price]
        ]

        l_ranges = 'B4:B6'

        self.gworksheet_cockpit.update_values(
            l_ranges,
            lst_data,
            majordim='ROWS'
        )

    def update_prev_week_data(self, p_high_price, p_low_price):
        lst_data = [
            [p_high_price],
            [p_low_price]
        ]

        l_ranges = 'B7:B8'

        self.gworksheet_cockpit.update_values(
            l_ranges,
            lst_data,
            majordim='ROWS'
        )