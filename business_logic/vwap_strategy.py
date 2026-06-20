
"""
vwap_strategy.py

Multi-stock VWAP strategy framework with:
- State Pattern
- Long / Short independent flows
- 10-minute candle setup logic
- 5-second tick monitoring
- Target exit
- Time exit (15 min)
- Stop-loss (entry candle high/low)
- Market close square-off (14:25)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta, time
from utility.quotes_utility import *
from utility.utility import *
from user_interface.adapter.config import *
from user_interface.adapter.trade_day_data import *
from user_interface.adapter.cockpit import *
import datetime      # ✅ module import, use datetime.datetime.today()
from datetime import datetime, timedelta, time  # ✅ direct import, use datetime.today()
from datatypes.option_straddle_types import *
import time as time_module



START_TIME = datetime.time(9, 45)
ENTRY_CUTOFF = datetime.time(14, 10)
END_TIME = datetime.time(14, 25)


@dataclass
class Trade:
    symbol: str
    side: str
    entry_time: datetime
    entry_price: float
    exit_time: datetime = None
    exit_price: float = None
    pnl: float = None
    exit_reason: str = None


class State(ABC):
    @abstractmethod
    def handle(self, strategy, candle):
        pass

    def on_tick(self, strategy, tick):
        return None


class NeutralState(State):
    def handle(self, strategy, candle):
        if candle["close"] > candle["vwap"]:
            strategy.candle_1_high = candle["high"]
            strategy.candle_1_low = candle["low"]
            strategy.candle_1_close = candle["close"]
            strategy.change_state(LongWait10MinState())
        elif candle["close"] < candle["vwap"]:
            strategy.candle_1_high = candle["high"]
            strategy.candle_1_low = candle["low"]
            strategy.candle_1_close = candle["close"]
            strategy.change_state(ShortWait10MinState())
        return None


class LongWait10MinState(State):
    def __init__(self):
        self.waited = 0

    def handle(self, strategy, candle):
        self.waited += 1
        if self.waited >= 1:
            strategy.change_state(LongPullbackState())
        return None


class LongPullbackState(State):
    def handle(self, strategy, candle):
        if candle["close"] < strategy.candle_1_close:
            strategy.change_state(LongBreakoutState())
        return None


class LongBreakoutState(State):
    def handle(self, strategy, candle):
        if candle["high"] > strategy.candle_1_high:
            strategy.entry_price = strategy.candle_1_high
            strategy.entry_time = candle["timestamp"]
            strategy.target_price = strategy.entry_price + strategy.TARGET_POINTS
            strategy.stop_loss = candle["low"]

            strategy.current_trade = Trade(
                symbol=strategy.symbol,
                side="LONG",
                entry_time=strategy.entry_time,
                entry_price=strategy.entry_price,
            )

            strategy.change_state(LongPositionState())

            return {
                "symbol": strategy.symbol,
                "action": "BUY",
                "entry_price": strategy.entry_price,
            }
        return None


class LongPositionState(State):
    def handle(self, strategy, candle):
        return None

    def on_tick(self, strategy, tick):
        if tick["ltp"] >= strategy.target_price:
            return strategy.close_trade(strategy.target_price, tick["timestamp"], "TARGET")

        if tick["ltp"] <= strategy.stop_loss:
            return strategy.close_trade(strategy.stop_loss, tick["timestamp"], "STOP_LOSS")

        if tick["timestamp"] - strategy.entry_time >= timedelta(minutes=15):
            return strategy.close_trade(tick["ltp"], tick["timestamp"], "TIME_EXIT")

        return None


class ShortWait10MinState(State):
    def __init__(self):
        self.waited = 0

    def handle(self, strategy, candle):
        self.waited += 1
        if self.waited >= 1:
            strategy.change_state(ShortPullbackState())
        return None


class ShortPullbackState(State):
    def handle(self, strategy, candle):
        if candle["close"] > strategy.candle_1_close:
            strategy.change_state(ShortBreakdownState())
        return None


class ShortBreakdownState(State):
    def handle(self, strategy, candle):
        if candle["low"] < strategy.candle_1_low:
            strategy.entry_price = strategy.candle_1_low
            strategy.entry_time = candle["timestamp"]
            strategy.target_price = strategy.entry_price - strategy.TARGET_POINTS
            strategy.stop_loss = candle["high"]

            strategy.current_trade = Trade(
                symbol=strategy.symbol,
                side="SHORT",
                entry_time=strategy.entry_time,
                entry_price=strategy.entry_price,
            )

            strategy.change_state(ShortPositionState())

            return {
                "symbol": strategy.symbol,
                "action": "SELL",
                "entry_price": strategy.entry_price,
            }
        return None


class ShortPositionState(State):
    def handle(self, strategy, candle):
        return None

    def on_tick(self, strategy, tick):
        if tick["ltp"] <= strategy.target_price:
            return strategy.close_trade(strategy.target_price, tick["timestamp"], "TARGET")

        if tick["ltp"] >= strategy.stop_loss:
            return strategy.close_trade(strategy.stop_loss, tick["timestamp"], "STOP_LOSS")

        if tick["timestamp"] - strategy.entry_time >= timedelta(minutes=15):
            return strategy.close_trade(tick["ltp"], tick["timestamp"], "TIME_EXIT")

        return None


class VWAPStrategy:
    TARGET_POINTS = 30

    def __init__(self, symbol, trade_book):
        self.symbol = symbol
        self.trade_book = trade_book
        self.current_trade = None
        self.reset()

    def reset(self):
        self.state = NeutralState()
        self.candle_1_high = None
        self.candle_1_low = None
        self.candle_1_close = None
        self.entry_price = None
        self.entry_time = None
        self.target_price = None
        self.stop_loss = None

    def change_state(self, state):
        self.state = state

    def on_candle_close(self, candle):
        return self.state.handle(self, candle)

    def on_tick(self, tick):
        if self.current_trade is None:
            return None
        return self.state.on_tick(self, tick)

    def close_trade(self, exit_price, exit_time, reason):
        trade = self.current_trade
        trade.exit_price = exit_price
        trade.exit_time = exit_time
        trade.exit_reason = reason

        if trade.side == "LONG":
            trade.pnl = exit_price - trade.entry_price
        else:
            trade.pnl = trade.entry_price - exit_price

        self.trade_book.append(trade)

        result = {
            "symbol": trade.symbol,
            "side": trade.side,
            "entry_price": trade.entry_price,
            "exit_price": trade.exit_price,
            "pnl": trade.pnl,
            "reason": reason,
        }

        self.current_trade = None
        self.reset()
        return result

    def square_off(self, timestamp, ltp):
        if self.current_trade is None:
            return None
        return self.close_trade(ltp, timestamp, "MARKET_CLOSE")


class StrategyManager:
    def __init__(self):
        self.trade_book = []
        self.strategies = {}

    def get_strategy(self, symbol):
        if symbol not in self.strategies:
            self.strategies[symbol] = VWAPStrategy(symbol, self.trade_book)
        return self.strategies[symbol]

    def on_candle(self, symbol, candle):
        t = candle["timestamp"].time()

        if t < START_TIME or t > ENTRY_CUTOFF:
            return None

        return self.get_strategy(symbol).on_candle_close(candle)

    def on_tick(self, symbol, ltp, timestamp):
        strategy = self.get_strategy(symbol)

        if timestamp.time() >= END_TIME:
            return strategy.square_off(timestamp, ltp)

        return strategy.on_tick({
            "ltp": ltp,
            "timestamp": timestamp
        })


class LogicVwapClose:
    def __init__(self, order_utility, \
                 trade_utility, option_chain_utility, quotes_utility, nse_utility, \
                 ui_adapter_config, ui_adapter_trade_day_data, ui_adapter_cockpit):
        # initialization from arguments
        self.logic_name = "LogicORBNiftyIndex"
        self.order_utility = order_utility
        self.trade_utility = trade_utility
        self.option_chain_utility = option_chain_utility
        self.nse_utility = nse_utility
        self.quotes_utility: QuoteUtility = quotes_utility
        self.nifty_future: str = ""

        # config data
        self.ui_adapter_config: UserInterfaceAdapterConfig = ui_adapter_config
        self.config_data = self.ui_adapter_config.get_data()

        self.ui_adapter_trade_day_data: UserInterfaceAdapterTradeDayData = ui_adapter_trade_day_data
        self.test_mode = self.config_data.test_mode_status

        # start the thread
        self.pre_requisite_thread = threading.Thread(target=self.pre_requisite_thread_handler)
        self.execute_thread = threading.Thread(target=self.execute)
        self.exit_thread = threading.Thread(target=self.exit_execution_thread)
        #pre requisite complete eent
        self.pre_requisite_complete_event = threading.Event()

        # start the prerequisite thread
        self.pre_requisite_thread.start()
        # start the thread
        self.execute_thread.start()
        # start the close order thread

        # start exit thread
        self.exit_thread.start()


    def pre_requisite_thread_handler(self):
        print("Prerequsite Thread", self.pre_requisite_start_time, type(self.pre_requisite_start_time))
        self.pre_requisite_complete_event.set()

    def execute(self):
        self.pre_requisite_complete_event.wait()
        self.__prerequisite()
        print("self.config_data.start_time", self.config_data.start_time)
        time_obj = datetime.strptime(self.config_data.start_time, "%H:%M:%S").time()
        start_time = datetime.combine(datetime.today(), time_obj)
        i_sleep_time = (start_time - datetime.now()).seconds
        print("i_sleep_time: ", i_sleep_time)
        time.sleep(i_sleep_time)
        print("Execute Thread - Prerequisite End")
        while True:
            end_time = datetime.strptime(self.config_data.end_time, '%H:%M:%S')
            is_trade_time_expired = is_trade_start_time_expired(end_time)
            if not is_trade_time_expired:
                print("Executing vwap strategy")
                if not self.config_data.test_mode_status:
                    time.sleep(15)
                else:
                    time.sleep(0.25)
            else:
                break

    def exit_execution_thread(self):
        print("Start of Exiting Thread")
        end_time = datetime.strptime(self.config_data.end_time, '%H:%M:%S')
        i_sleep_time = (end_time - datetime.now()).seconds
        time.sleep(i_sleep_time)
        print("End of Exiting Thread")

    def get_thread_info(self):
        return self.exit_thread

    # private functions
    def __get_candle_data(self, ticker):
        str_date = datetime.today() - timedelta(days=self.day_preset)
        str_from_date, str_to_date = self.trade_utility.get_broker_utility().getTimeFrame(str_start_time="09:15:00",
                                                                     str_stop_time="15:30:00", date=str_date)

        candle_data = self.trade_utility.get_broker_utility().fetchOHLC(ticker=ticker,\
                                                    str_from_date=str_from_date,\
                                                    str_to_date=str_to_date,\
                                                    interval="1minute",\
                                                    all_data=False,\
                                                    exchange="NSE",\
                                                    market_type="NFO")
        if len(candle_data) > 0:
            if "09:14:00" in candle_data[DATE_TIME][0]:
                candle_data = candle_data.drop(candle_data.index[0]).reset_index(drop=True)
        return candle_data

    def __get_prev_day_candle_data(self, ticker):
        prev_trade_day = nse_utitlity.get_prev_day_trade_date(self.day_preset)
        str_date = datetime.strptime(prev_trade_day, "%Y-%m-%d")
        print("str_date: ", str_date, type(str_date))
        str_from_date, str_to_date = self.option_chain_utility.get_broker_utility().getTimeFrame(str_start_time="09:15:00",
                                                                     str_stop_time="15:30:00", start_date=str_date, stop_date=str_date)

        candle_data = self.option_chain_utility.get_broker_utility().fetchOHLC(ticker=ticker,\
                                                    str_from_date=str_from_date,\
                                                    str_to_date=str_to_date,\
                                                    interval="1Day",\
                                                    all_data=False,\
                                                    exchange="NSE",\
                                                    market_type="")
        return candle_data

    def __get_prev_week_candle_data(self, ticker):
        #pass 1 for tuesday
        prev_prev_week_day, prev_week_day = get_previous_expirty_day(1, self.day_preset)
        str_date = datetime.strptime(prev_prev_week_day, "%Y-%m-%d")
        end_date = datetime.strptime(prev_week_day, "%Y-%m-%d")
        print("str_date: ", str_date, type(str_date))
        str_from_date, str_to_date = self.option_chain_utility.get_broker_utility().getTimeFrame(
            str_start_time="09:15:00",
            str_stop_time="15:30:00", start_date=str_date, stop_date=end_date)

        candle_data = self.option_chain_utility.get_broker_utility().fetchOHLC(ticker=ticker,\
                                                    str_from_date=str_from_date,\
                                                    str_to_date=str_to_date,\
                                                    interval="1Day",\
                                                    all_data=False,\
                                                    exchange="NSE",\
                                                    market_type="")
        return candle_data


    def __get_option_chain(self, ticker):
        return self.option_chain_utility.get_broker_utility().getOptionChain(ticker)