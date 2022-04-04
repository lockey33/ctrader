from backtesting import Strategy, Backtest
from backtesting.lib import Strategy, crossover
import talib
import numpy as np

class SmaCrossCustom(Strategy):

    n1 = 3.7 #volatilityPercent
    n2 = 8 #atr ratio
    n3 = 35 # volIndex

    def init(self):
        super().init()

        self.sma1 = self.I(talib.SMA, self.data.Close, 200)
        self.sma2 = self.I(talib.SMA, self.data.Close, 100)
        self.sma3 = self.I(talib.SMA, self.data.Close, 20)
        self.rsi = self.I(talib.RSI, self.data.Close, 14)
        self.adx = self.I(talib.ADX, self.data.High, self.data.Low, self.data.Close, 14)
        #self.set_trailing_sl(2)

    def next(self):
        super().next()
        if(-0.02 > self.position.pl_pct):
            self.position.close()

        for trade in self.trades:
            if trade.is_long:
                trade.sl = max(trade.sl or -np.inf, self.data.Close[-1] - self.data.ATR[-1] * self.n2)
            else:
                trade.sl = min(trade.sl or np.inf, self.data.Close[-1] + self.data.ATR[-1] * self.n2)

        if (crossover(self.sma3, self.sma1) and self.adx >= self.n3) or (self.sma3 > self.sma1 and self.adx >= self.n3 and self.data.closeToEma200[-1] == 1) or (self.sma3 > self.sma1 and self.adx >= self.n3 and self.data.closeToEma20[-1] == 1):
            self.position.close()
            print(self.data.EMA200[-1], self.data.Close[-1], self.data.closeToEma200[-1], self.adx[-1])
            self.buy(sl=self.data.Close[-1] - self.data.ATR[-1] * self.n2)
        elif (crossover(self.sma1, self.sma3) and self.adx >= self.n3) or (self.sma1 > self.sma3 and self.adx >= self.n3 and self.data.closeToEma200[-1] == 1) or (self.sma1 > self.sma3 and self.adx >= self.n3 and self.data.closeToEma20[-1] == 1):
            self.position.close()
            print(self.data.EMA200[-1], self.data.Close[-1])
            self.sell(sl=self.data.Close[-1] + self.data.ATR[-1] * self.n2)


