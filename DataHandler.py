from abc import ABC, abstractmethod
import datetime
import os, os.path
import numpy as np
import pandas as pd
from EventType import MarketEvent
from queue import Queue

class DataHandler(ABC):
    """
    ABC means that is can not be instantiate an instance directly
    only subclasses can be instantiated
    reason for this:
        all subsequent DataHandler subclasses must adhere to thereby
        ensuring the compatibility with other classes that comminicate with each other

    Derived class DataHandler object can generate set of bars(OHLCVI) for each symbol.
    """

    # abstractmethod will let the interpreter know this function
    # will be overridden in subclasses
    @abstractmethod
    def get_latest_bars(self, symbol, n=1):
        """
        :param n:
        :return:
        """
        raise NotImplementedError("not implemented")

    @abstractmethod
    def get_latest_bar_datetime(self, symbol):
        """

        :param symbol:
        :return:
        """
        raise NotImplementedError("not implemented")

    @abstractmethod
    def get_latest_bar_value(self, symbol, value_type=None):
        """
        :param n:
        :param value_type:
        :return:
        """
        raise NotImplementedError("not implemented")

    @abstractmethod
    def update_bars(self):
        """
        :return:
        """
        raise NotImplementedError("not implemented")


class HistoricCSVDataHandler(DataHandler):
    """
    read CSV files
    """

    def __init__(self, events:Queue, csv_dir:str, symbol_list:list):
        """
        :param events: The Event Queue
        :param csv_dir: Directory path to the CSV files.
        :param symbol_list: A list of symbol strings.
        """
        self.event = events
        self.csv_dir = csv_dir
        self.symbol_list = symbol_list

        self.symbol_data = {}
        self.latest_symbol_data = {}
        self.continue_backtest = True

        self._open_convert_csv_files()

    def _open_convert_csv_files(self):
        """
        open csv files and convert them into pandas dataframe
        :return:
        """
        comb_index = None
        for symbol in self.symbol_list:
            # read all csv files into a single one dict,this dict is a member variable
            # dict keys are string, values are dataframe
            self.symbol_data[symbol] = pd.read_csv(os.path.join(self.csv_dir, '%symbol.csv' % symbol),
                                                   header=0, index_col=0, parse_dates=True,
                                                   names=['datetime', 'open', 'high', 'low', 'close',
                                                          'volume', 'adj_close']).sort()
            if comb_index is None:
                comb_index = self.symbol_data[symbol].index
            else:
                comb_index.union(self.symbol_data[symbol].index)

            self.latest_symbol_data[symbol] = []
        # reindex the dataframe
        for symbol in self.symbol_list:
            self.symbol_data[symbol] = self.symbol_data[symbol].reindex(index=comb_index,
                                                                        method='pad').iterrows()

    def _get_new_bar(self, symbol):
        """
        a generator to provide a new bar
        :param symbol: instrument symbol
        :return: the latest bar from the data feed
        """
        for bar in self.symbol_data[symbol]:
            yield bar  # generator

    def get_latest_bars(self, symbol, n=1):
        """
        return the last n bars from the latest_symbol list
        :param symbol:
        :param n:
        :return:
        """
        bar_list = self.latest_symbol_data[symbol]
        return bar_list[-n:]

    def get_latest_bar_datetime(self, symbol):
        """

        :param symbol:
        :return:
        """
        bar_list = self.latest_symbol_data[symbol]
        return bar_list[-1][0]

    def get_latest_bar_value(self, symbol, value_type=None, n=1):
        """
        :param symbol:
        :param value_type:
        :return: open,high,low,close,volume,oi values from the pandas bar series object
        """
        bar_list = self.get_latest_bars(symbol, n)
        return [getattr(bar[1],value_type) for bar in bar_list]

    def update_bars(self):
        """

        :return:
        """
        for symbol in self.symbol_list:
            bar = next(self._get_new_bar(symbol))
            if bar is not None:
                self.latest_symbol_data[symbol].append(bar)

        self.event.put(MarketEvent())
