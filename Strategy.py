from abc import ABC,abstractmethod
import datetime
from queue import Queue
import numpy as np
import pandas as pd
from EventType import SignalEvent

class Strategy(ABC):
    """
    Strategy is an abstract base class for the subsequent subclass
    that generate SignalEvent which will be send to Portfolio object

    DataHandler generate Bars(MarketEvent),Strategy recieve Bars then generate signals(SignalEvent)
    """
    @abstractmethod
    def calculate_signal(self):
        """
        calculate the list of signals
        :return:
        """
        raise NotImplementedError("not implemented")

