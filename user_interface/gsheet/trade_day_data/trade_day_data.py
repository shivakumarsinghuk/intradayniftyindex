# -*- coding: utf-8 -*-
"""
login_types.py
"""
import sys
import numpy as np
sys.path.append('../interfaces')   # path to directory containing helper.py

from interfaces.Iuser_Interface import *
from utility.gsheet_utility import *
from utility.utility import *
from broker_platform.datatypes.trade_data import *

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

class UserInterfaceTradeDayData(IUserInterface):

    def __init__(self, key):
        self.data = None
        self.googlesheet_utility = gsheet_utility(account_file=key,
                                                  spread_sheet_name="ORB_Nifty_Index")
        self.gworksheet_trade_day_data = self.googlesheet_utility.get_work_sheet("TradingDayData")
        #self.gworksheet_result = self.googlesheet_utility.get_work_sheet("Result")


    def get_data(self):
        return self.data

    def clear_data(self):
        self.gworksheet_trade_day_data.clear("B2:G376")
        self.gworksheet_trade_day_data.clear("J2:AB27")


    def update_trade_date(self, p_date):
        lst_data = [[p_date]]
        l_ranges = f'I2:I2'
        # Ensure we write by ROWS, not COLUMNS
        self.gworksheet_trade_day_data.update_values(
            l_ranges,
            lst_data,
            majordim='ROWS'
        )

    def update_ohlc(self, row, open_price, high_price, low_price, close_price):
        lst_data = [[open_price, high_price, low_price, close_price]]
        l_ranges = f'B{row}:E{row}'
        # Ensure we write by ROWS, not COLUMNS
        self.gworksheet_trade_day_data.update_values(
            l_ranges,
            lst_data,
            majordim='ROWS'
        )

    def update_volume(self, row, volume):
        lst_data = [[volume]]
        l_ranges = f'F{row}:F{row}'
        # Ensure we write by ROWS, not COLUMNS
        self.gworksheet_trade_day_data.update_values(
            l_ranges,
            lst_data,
            majordim='ROWS'
        )

    def update_vix(self, row, vix):
        lst_data = [[vix]]
        l_ranges = f'G{row}:G{row}'
        # Ensure we write by ROWS, not COLUMNS
        self.gworksheet_trade_day_data.update_values(
            l_ranges,
            lst_data,
            majordim='ROWS'
        )

    def update_option_chain(self, row, p_option_chain_data: option_chain_data):

        raw_data = [
            p_option_chain_data.date_time,
            p_option_chain_data.atm_strike,
            p_option_chain_data.atm_straddle_price,
            p_option_chain_data.call_greeks.iv,
            p_option_chain_data.put_greeks.iv,
            p_option_chain_data.pcr,
            p_option_chain_data.max_pain,
            p_option_chain_data.put_wall_data.strike_price,
            p_option_chain_data.put_wall_data.oi,
            p_option_chain_data.call_wall_data.strike_price,
            p_option_chain_data.call_wall_data.oi,
            p_option_chain_data.call_greeks.gamma,
            p_option_chain_data.call_greeks.vega,
            p_option_chain_data.call_greeks.theta,
            p_option_chain_data.call_greeks.delta,
            p_option_chain_data.put_greeks.gamma,
            p_option_chain_data.put_greeks.vega,
            p_option_chain_data.put_greeks.theta,
            p_option_chain_data.put_greeks.delta
        ]

        lst_data = [[to_python_type(v) for v in raw_data]]

        l_ranges = f'J{row}:AB{row}'

        self.gworksheet_trade_day_data.update_values(
            l_ranges,
            lst_data,
            majordim='ROWS'
        )
