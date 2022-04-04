from backtesting import Strategy, Backtest
from backtesting.lib import Strategy, crossover
import talib
import numpy as np

class SmaLong(Strategy):

    n1 = 1 #atr ratio
    n2 = 2 # profit atr ratio
    def init(self):
        super().init()

        self.sma1 = self.I(talib.EMA, self.data.Close, 7)
        self.sma2 = self.I(talib.SMA, self.data.Close, 21)
        self.rsi = self.I(talib.RSI, self.data.Close, 14)
        self.stoch = self.I(talib.STOCHRSI, self.data.Close, 14, 5, 3, 0)
        #self.set_trailing_sl(2)

    def next(self):
        super().next()

        for trade in self.trades:
            if trade.is_long:
                if trade.pl_pct < -0.02 or trade.pl_pct > 0.05:
                    self.position.close()
            else:
                if trade.pl_pct < -0.02 or trade.pl_pct > 0.05:
                    self.position.close()

        if (crossover(self.sma1, self.sma2)):
            self.position.close()
            self.buy()
        elif (crossover(self.sma2, self.sma1)):
            self.position.close()
            self.sell()


