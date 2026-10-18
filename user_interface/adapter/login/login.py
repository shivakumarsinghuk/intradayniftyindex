# -*- coding: utf-8 -*-
"""
login_types.py
"""
import sys
from user_interface.gsheet.login import *
sys.path.append('../interfaces')   # path to directory containing helper.py


class UserInterfaceAdapterLogin:

    def __init__(self, args):
        if "gsheet" == args.userinterface:
            self.ui_object = UserInterfaceLogin(args.key)

    def get_data(self):
        return self.ui_object.data


