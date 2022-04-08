from backtesting import Strategy, Backtest
from backtesting.lib import Strategy, crossover
import talib
import numpy as np

class SmaLong(Strategy):

    n1 = 1 #atr ratio
    n2 = 6 # profit atr ratio
    n3 = 25 #candleToWait
    def init(self):
        super().init()

        self.sma1 = self.I(talib.EMA, self.data.Close, 21)
        self.sma2 = self.I(talib.SMA, self.data.Close, 7)
        self.rsi = self.I(talib.RSI, self.data.Close, 14)
        self.stoch = self.I(talib.STOCHRSI, self.data.Close, 14, 5, 3, 0)
        #self.set_trailing_sl(2)

    def next(self):
        super().next()
        def trade(self):

            #"""
            for trade in self.trades:
                if trade.is_long:
                    trade.sl = max(trade.sl or -np.inf, self.data.Close[-1] - self.data.ATR[-1] * self.n2)
                else:
                    trade.sl = min(trade.sl or np.inf, self.data.Close[-1] + self.data.ATR[-1] * self.n2)
            #"""


            if (crossover(self.sma2, self.sma1)):
                self.position.close()
                self.buy()
                if len(self.closed_trades) >= 1:
                    lastTrade = self.closed_trades[-1]
            elif (crossover(self.sma1, self.sma2)):
                self.position.close()
                self.sell()
                if len(self.closed_trades) >= 1:
                    lastTrade = self.closed_trades[-1]

        if len(self.closed_trades) >= 1:
            lastTrade = self.closed_trades[-1]
            if self.data.index.stop + self.n3 > lastTrade.exit_bar : #on attend entre chaque position cloturées
                trade(self)

        elif len(self.closed_trades) == 0 :
            trade(self)


