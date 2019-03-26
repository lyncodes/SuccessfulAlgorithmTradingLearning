import pandas as pd
from EventType import FillEvent, OrderEvent, SignalEvent
from Performance import create_sharpe_ratio, create_drawdowns
from DataHandler import HistoricCSVDataHandler


class Portfolio:
    """
    Portfolio class handle the positions and market values
    of all instruments at a resolution of a '''bar'''
    secondly bar, minutely bar, 5-min bar ,30-min bar

    position DataFrame stores a time_index of the quantity of position

    holding DataFrame stores the '''cash and total market holdings values''' of
    each symbol for a particular time index

    """

    def __init__(self, bars: HistoricCSVDataHandler, events, start_date, initial_capital=1e5):
        """

        :param bars: DataHandler object
        :param events: Event Queue object
        :param start_date: Start date of the portfolio
        :param initial_capital: start capital
        """
        self.bars = bars
        self.events = events
        self.symbol_list = self.bars.symbol_list
        self.start_date = start_date
        self.initial_capital = initial_capital

        self.all_positions = self.construct_all_positions()
        self.current_positions = dict((k, v) for k, v in [(s, 0) for s in self.symbol_list])

        self.all_holdings = self.construct_all_holdings()
        self.current_holdings = self.construct_current_holdings()

        self.equity_curve: pd.DataFrame = None

    def construct_all_positions(self):
        d = dict((k, v) for k, v in [(s, 0) for s in self.symbol_list])
        d['datetime'] = self.start_date

        return [d]

    def construct_all_holdings(self):
        d = dict((k, v) for k, v in [(s, 0) for s in self.symbol_list])
        d['datetime'] = self.start_date
        d['cash'] = self.initial_capital
        d['commission'] = 0
        d['total'] = self.initial_capital

        return [d]

    def construct_current_holdings(self):
        d = dict((k, v) for k, v in [(s, 0) for s in self.symbol_list])
        d['cash'] = self.initial_capital
        d['commission'] = 0
        d['total'] = self.initial_capital
        # not wrap the dictionary into the list
        return d

    def update_timeindex(self):
        latest_datetime = self.bars.get_latest_bar_datetime(self.symbol_list[0])
        dp = dict((k, v) for k, v in [(s, 0) for s in self.symbol_list])
        dp['datetime'] = latest_datetime

        for symbol in self.symbol_list:
            dp[symbol] = self.current_positions[symbol]

        self.all_positions.append(dp)

        dh = dict((k, v) for k, v in [(s, 0) for s in self.symbol_list])
        dh['datetime'] = latest_datetime
        dh['cash'] = self.current_holdings['cash']
        dh['commission'] = self.current_holdings['commission']
        dh['total'] = self.current_holdings['cash']

        for symbol in self.symbol_list:
            market_value = self.current_positions[symbol] * self.bars.get_latest_bar_value(symbol, 'adj_close')
            dh[symbol] = market_value
            dh['total'] += market_value
        self.all_holdings.append(dh)

    def update_positions_from_fill(self, fill: FillEvent):
        fill_dir = 0
        if fill.direction == 'BUY':
            fill_dir = 1
        elif fill.direction == 'SELL':
            fill_dir = -1
        self.current_positions[fill.symbol] += fill_dir * fill.quantity

    def update_holdings_from_fill(self, fill: FillEvent):
        fill_dir = 0
        #         fill direction
        if fill.direction == 'BUY':
            fill_dir = 1
        elif fill.direction == 'SELL':
            fill_dir = -1
        fill_cost = self.bars.get_latest_bar_value(fill.symbol, 'adj_close')
        cost = fill_dir * fill_cost * fill.quantity
        self.current_holdings[fill.symbol] += cost
        self.current_holdings['commission'] += fill.commission
        self.current_holdings['cash'] -= (cost + fill.commission)
        self.current_holdings['total'] -= (cost + fill.commission)

    def update_fill(self, fill_event: FillEvent):
        if fill_event.type == 'FILL':
            self.update_positions_from_fill(fill_event)
            self.update_holdings_from_fill(fill_event)

    def generate_naive_order(self, signal: SignalEvent):
        order = None
        symbol = signal.symbol
        direction = signal.signal_type
        # strength = signal.strength

        mkt_quantity = 100
        cur_quantity = self.current_positions[symbol]
        order_type = 'MKT'

        if direction == 'LONG' and cur_quantity == 0:
            order = OrderEvent(symbol, order_type, mkt_quantity, 'BUY')
        elif direction == 'SHORT' and cur_quantity == 0:
            order = OrderEvent(symbol, order_type, mkt_quantity, 'SELL')
        elif direction == 'EXIT' and cur_quantity > 0:
            order = OrderEvent(symbol, order_type, abs(cur_quantity), 'SELL')
        elif direction == 'EXIT' and cur_quantity < 0:
            order = OrderEvent(symbol, order_type, abs(cur_quantity), 'BUY')

        return order

    def update_signal(self, signalevent: SignalEvent):
        if signalevent.type == 'SIGNAL':
            order_event = self.generate_naive_order(signalevent)
            self.events.put(order_event)

    def create_equity_curve_dataframe(self):
        curve = pd.DataFrame(self.all_holdings)
        curve.set_index('datetime', inplace=True)
        curve['returns'] = curve['total'].pct_change()
        curve['equity_curve'] = (1 + curve['returns']).cumprod()
        self.equity_curve = curve

    def output_summary_stats(self):
        total_return = self.equity_curve['equity_curve'][-1]
        returns = self.equity_curve['returns']
        pnl = self.equity_curve['equity_curve']

        sharp_ratio = create_sharpe_ratio(returns, periods=252 * 60 * 6.5)
        drawdown, max_dd, dd_duration = create_drawdowns(pnl)
        self.equity_curve['drawdown'] = drawdown

        stats = {"total return": ((total_return - 1) * 100),
                 "sharpe ratio": sharp_ratio,
                 "max draw down": (max_dd * 100),
                 "duration": dd_duration}
        self.equity_curve.to_csv('equity.csv')

        return stats
