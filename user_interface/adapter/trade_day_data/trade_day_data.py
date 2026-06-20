# -*- coding: utf-8 -*-
"""
login_types.py
"""
import sys
from user_interface.gsheet.trade_day_data import *


class UserInterfaceAdapterTradeDayData:

    def __init__(self, args):
        if "gsheet" == args.userinterface:
            self.ui_object = UserInterfaceTradeDayData(args.key)

    def get_data(self):
        return self.ui_object.data

    def clear_data(self):
        self.ui_object.clear_data()

    def update_trade_date(self, p_date):
        self.ui_object.update_trade_date(p_date)

    def update_ohlc(self, row, open_price, high_price, low_price, close_price):
        self.ui_object.update_ohlc(row, open_price, high_price, low_price, close_price)

    def update_volume(self, row, volume):
        self.ui_object.update_volume(row, volume)

    def update_vix(self, row, vix):
        self.ui_object.update_vix(row, vix)

    def update_option_chain(self, row, p_option_chain_data:option_chain_data):
        self.ui_object.update_option_chain(row, p_option_chain_data)