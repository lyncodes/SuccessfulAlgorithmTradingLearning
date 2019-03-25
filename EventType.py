class Event(object):
    """
    Event is base class,which will be inherited in the latter specified deritive
    Event
    """
    pass


class MarketEvent(Event):
    """
    triggered by the datahandler which recieve data feed from vendor
    trigger the strategy to generating trading strategy
    """

    def __init__(self):
        """
        Initialises the MarketEvent.
        """
        self.type = 'MARKET'


class SignalEvent(Event):
    """
    handle event and generate signal to portfolio object
    """

    def __init__(self, strategy_id, symbol, datetime, signal_type, strength):
        """
        :param strategy_id:the unique identifier for the strategy
        :param symbol: the ticker symbol e.g. 'GOOG' 'rb1905'
        :param datetime: the timestamp which the signal was generated
        :param signal_type: 'LONG' or 'SHORT'
        :param strength: scale the quantity at the portfolio level
        """
        self.type = 'SIGNAL'
        self.strategy_id = strategy_id
        self.symbol = symbol
        self.datetime = datetime
        self.signal_type = signal_type
        self.strength = strength


class OrderEvent(Event):
    '''
    handle the order
    '''

    def __init__(self, symbol, order_type, quantity, direction):
        """
        :param symbol:e.g.(GOOG,RB1906) instrument to trade
        :param order_type: market or limit, MKT or LMT
        :param quantity: how much we trade, non-negative integer
        :param direction: LONG or SHORT
        """
        self.type = 'ORDER'
        self.symbol = symbol
        self.order_type = order_type
        self.quantity = quantity
        self.direction = direction

    def print_order(self):
        print("Order: Symbol=%s, Type=%s, Quantity=%s, Direction=%s" %
              (self.symbol, self.order_type, self.quantity, self.direction)
              )


class FillEvent(Event):
    """
    store the information returns from the broker
    quantity of an instrument actually filled and what price
    the commission and other cost
    """

    def __init__(self, timeindex, symbol, exchange, quantity, direction, fill_cost, commission=None):
        """

        :param timeindex: bar-resolution when the order was filled
        :param symbol: instrument symbol
        :param exchange: which exchange
        :param quantity: how much been traded
        :param direction: LONG or SHORT
        :param fill_cost: holding value
        :param commission: optional commission sent from the broker
        """
        self.timeindex = timeindex
        self.symbol = symbol
        self.exchange = exchange
        self.quantity = quantity
        self.direction = direction
        self.fill_cost = fill_cost

        if commission:
            self.commission = commission
        else:
            self.commission = self.calculate_commission()

    def calculate_commission(self):
        """
        calculate the commission according
        specific rules
        :return: commission

        example purpose only
        """
        commission = 1.3
        if self.quantity <= 500:
            commission = max(1.3, 0.013 * self.quantity)
        else:
            commission = max(1.3, 0.008 * self.quantity)
        return commission
