import datetime
from queue import Queue
import time


class Backtest:
    def __init__(self, csv_dir, symbol_list, initial_capital,
                 heartbeat, start_date, data_handler,
                 execution_handler, portfolio, strategy):
        """

        :param csv_dir:
        :param symbol_list:
        :param initial_capital:
        :param hearbeat:
        :param start_date:
        :param data_handler:
        :param execution_handler:
        :param portfolio:
        :param strategy:
        """
        self.csv_dir = csv_dir
        self.symbol_list = symbol_list
        self.initial_capital = initial_capital
        self.heartbeat = heartbeat
        self.start_date = start_date

        self.data_handler_cls = data_handler
        self.execution_handler_cls = execution_handler
        self.portfolio_cls = portfolio
        self.strategy_cls = strategy

        self.events = Queue()

        self.signals = 0
        self.orders = 0
        self.fills = 0
        self.num_strats = 1

        self._generate_trading_instance()

    def _generate_trading_instance(self):
        self.data_handler = self.data_handler_cls(self.events,
                                                  self.csv_dir,
                                                  self.symbol_list)
        self.strategy = self.strategy_cls(self.data_handler, self.events)
        self.portfolio = self.portfolio_cls(self.data_handler,
                                            self.events,
                                            self.start_date,
                                            self.initial_capital)
        self.execution_handler = self.execution_handler_cls(self.events)

    def _run_backtest(self):
        i = 0
        while True:
            i += 1
            print(i)
            if self.data_handler.continue_backtest == True:
                self.data_handler.update_bars()
            else:
                break

            while True:
                try:
                    event = self.events.get()
                except:
                    break

                if event is not None:
                    if event.type == 'MARKET':
                        self.strategy.calculate_signal(event)
                        self.portfolio.update_timeindex(event)
                    elif event.type == 'SIGNAL':
                        self.signals += 1
                        self.portfolio.update_signal(event)
                    elif event.type == 'ORDER':
                        self.orders += 1
                        self.execution_handler.execute_order(event)
                    elif event.type == 'FILL':
                        self.fills +=1
                        self.portfolio.update_fill(event)
            time.sleep(self.heartbeat)

    def _out_performace(self):
        self.portfolio.create_equity_curve_dataframe()
        stats = self.portfolio.output_summary_stats()
        print(stats)

    def simulate_trading(self):
        self._run_backtest()
        self._out_performace()

