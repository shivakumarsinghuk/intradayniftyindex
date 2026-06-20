# -*- coding: utf-8 -*-
"""
login_types.py
"""
import sys
sys.path.append('../types')   # path to directory containing helper.py


class IUserInterface:

    def get_data(self):
        print("Parent IUserInterfaceLogin get function")

    def set_data(self):
        print("Parent IUserInterfaceLogin set function")



