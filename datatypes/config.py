# -*- coding: utf-8 -*-
"""
login_types.py
"""
from dataclasses import dataclass

@dataclass
class ConfigData:
    candle_interval: int = 0
    start_time: str = ""
    end_time: str = ""
    test_mode_status: bool = False
    test_mode_delta_days: int = 0

    def __init__(self, candle_interval=0, start_time="", end_time="",
                 test_mode_status=False, test_mode_delta_days=0):
        self.candle_interval = candle_interval
        self.start_time = start_time
        self.end_time = end_time
        self.test_mode_status = test_mode_status
        self.test_mode_delta_days = test_mode_delta_days

