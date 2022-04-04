from backtesting import Strategy, Backtest
from backtesting.lib import Strategy, crossover
import talib
import numpy as np

class SmaOpti(Strategy):

    n1 = 3.7 #volatilityPercent
    n2 = 8 #atr ratio
    n3 = 16 #atr profit ratio
    n4 = 200
    n5 = 100
    n6 = 20

    def init(self):
        super().init()

        self.sma1 = self.I(talib.SMA, self.data.Close, self.n4)
        self.sma2 = self.I(talib.SMA, self.data.Close, 100)
        self.sma3 = self.I(talib.SMA, self.data.Close, self.n5)
        self.sma4 = self.I(talib.SMA, self.data.Close, self.n6)
        self.rsi = self.I(talib.RSI, self.data.Close, 6)
        self.adx = self.I(talib.ADX, self.data.High, self.data.Low, self.data.Close, 14)
        #self.set_trailing_sl(2)

    def next(self):
        super().next()

        for trade in self.trades:
            if trade.is_long:
                if crossover(self.sma3, self.sma4):
                    self.position.close()
            else:
                if crossover(self.sma3, self.sma4):
                    self.position.close()

        if self.position == False:
            if (crossover(self.sma4, self.sma1)):
                self.position.close()
                self.buy(sl=self.data.Close[-1] - self.data.ATR[-1] * self.n2, tp=self.data.Close[-1] + self.data.ATR[-1] * self.n3)
            elif (crossover(self.sma1, self.sma4)):
                self.position.close()
                self.sell(sl=self.data.Close[-1] + self.data.ATR[-1] * self.n2, tp=self.data.Close[-1] - self.data.ATR[-1] * self.n3)


