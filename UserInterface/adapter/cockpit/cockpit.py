# -*- coding: utf-8 -*-
"""
login_types.py
"""
import sys
from user_interface.gsheet.cockpit import *


class UserInterfaceAdapterCockpitData:

    def __init__(self, args):
        if "gsheet" == args.userinterface:
            self.ui_object = UserInterfaceCockpitData(args.key)

    def update_prev_day_ohlc(self, high_price, low_price, close_price):
        self.ui_object.update_prev_day_ohlc(high_price, low_price, close_price)

    def update_prev_week_data(self, p_high_price, p_low_price):
        self.ui_object.update_prev_week_data(p_high_price, p_low_price)