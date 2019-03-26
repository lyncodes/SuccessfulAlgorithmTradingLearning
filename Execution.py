"""
execution handlers take orders and send info to brokers
generate FillEvent to update the trading system
"""
from abc import ABC, abstractmethod
import datetime
from queue import Queue
from EventType import FillEvent, OrderEvent


class ExecutionHandler(ABC):
    @abstractmethod
    def execute_order(self, order: OrderEvent):
        """

        :param order:
        :return:
        """
        raise NotImplementedError("NOT IMPLEMENTED")


class SimulatedExecutionHandlers(ExecutionHandler):
    def __init__(self, events:Queue):
        self.events = events

    # SHFE上期所
    def execute_order(self, order: OrderEvent):
        if order.type == 'ORDER':
            fill_event = FillEvent(datetime.datetime.utcnow(),
                                   order.symbol,
                                   'SHFE',
                                   order.quantity,
                                   order.direction,
                                   None)
            self.events.put(fill_event)
