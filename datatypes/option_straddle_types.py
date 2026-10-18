# -*- coding: utf-8 -*-
"""
login_types.py
"""
from dataclasses import dataclass, field


DEFINE_NOT_TRADED = "Not Traded"
DEFINE_ORDER_PLACED = "Order Placed"
DEFINE_EXITED_WITH_PROFIT = "Exited with Profit"
DEFINE_EXITED_WITH_LOSS = "Exited with Profit"
DEFINE_TRADE_TYPE_BUY = "Buy"
DEFINE_TRADE_TYPE_Sell = "Sell"

@dataclass
class OptionStraddleUserInput:
    index: str = ""
    buy_total_price: float = 0.0
    sell_total_price: float = 0.0
    target_percentage: float = 0.0
    stop_loss_percentage: float = 0.0
    quantity: int = 0
    expiry_buy: str = ""
    expiry_sell: str = ""
    start_time: str = ""
    stop_time: str = ""

    def __init__(self, index:str, buy_total_price:float, sell_total_price:float, target_percentage:float, \
                 stop_loss_percentage:float, quantity:int, expiry_buy:str, expiry_sell:str, start_time:str, stop_time:str):
        self.index = index
        self.buy_total_price = buy_total_price
        self.sell_total_price = sell_total_price
        self.target_percentage = target_percentage
        self.stop_loss_percentage = stop_loss_percentage
        self.quantity = quantity
        self.expiry_buy = expiry_buy
        self.expiry_sell = expiry_sell
        self.start_time = start_time
        self.stop_time = stop_time

@dataclass
class trade_status:
    status: str = ""
    profit: float = 0.0


@dataclass
class TradeStatusInfo:
    buy_ce: trade_status = field(default_factory=trade_status)
    sell_ce: trade_status = field(default_factory=trade_status)
    buy_pe: trade_status = field(default_factory=trade_status)
    sell_pe: trade_status = field(default_factory=trade_status)

@dataclass
class ResultData:
    trade_date: str = ""
    index_type: str = ""
    is_weekly_expiry: str = ""
    is_monthly_expiry: str = ""
    atm: int = 0
    trade_type: str = ""
    target_total_price: float = 0.0
    exit_total_price: float = 0.0
    expiry_date: float = 0.0
    profit_loss_value: float = 0.0