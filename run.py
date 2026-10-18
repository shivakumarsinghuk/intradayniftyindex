"""
run.py
"""

import argparse
from user_interface.adapter import *
from pal.utility_manager import *
from datatypes.option_straddle_types import *
from utility.quotes_utility import *
from business_logic.orb_nifty_index import *
from utility.utility import *

def validate_arguments(args=None):
    parser = argparse.ArgumentParser(description="Demo script with named args")

    parser.add_argument("--userinterface", type=str, required=True, help="User Interface Supported [gsheet]")
    parser.add_argument("--key", type=str, help="Provide the json file")
    args = parser.parse_args()
    print(args.userinterface, args.key)
    return args

if __name__ == "__main__":

    args = validate_arguments()
    #construct nse utility
    obj_nse_utility = nse_utitlity()

    #create gsheet user login  object
    obj_adapter_login = UserInterfaceAdapterLogin(args)
    obj_adapter_config = UserInterfaceAdapterConfig(args)
    print(obj_adapter_login.get_data()[0])


    obj_utility_manager = utility_manager(ui_adapter=obj_adapter_login, nse_utility=obj_nse_utility)
    obj_broker_utility = obj_utility_manager.get_utility_object(obj_adapter_login.get_data()[0])
    obj_option_chain_broker_utility = obj_utility_manager.get_utility_object(obj_adapter_login.get_data()[1])
    obj_adapter_trade_day_data = UserInterfaceAdapterTradeDayData(args)
    obj_adapter_trade_day_data.clear_data()
    obj_adapter_cockpit_data = UserInterfaceAdapterCockpitData(args)

    #create quote utility
    obj_quote_utility = QuoteUtility(p_trade_utility=obj_broker_utility)

    #create business logic object

    obj_bl_orb_nifty_index = LogicORBNiftyIndex(order_utility=obj_broker_utility, \
                                                 trade_utility=obj_broker_utility, \
                                                 option_chain_utility=obj_option_chain_broker_utility, \
                                                 quotes_utility=obj_quote_utility, \
                                                 nse_utility=obj_nse_utility,\
                                                 ui_adapter_config=obj_adapter_config, \
                                                 ui_adapter_trade_day_data=obj_adapter_trade_day_data, \
                                                 ui_adapter_cockpit=obj_adapter_cockpit_data)

    obj_bl_orb_nifty_index.get_thread_info().join()

    # stop the quote utility
    obj_quote_utility.stop()
    obj_quote_utility.get_thread_info().join()

    print("Main Terminated")