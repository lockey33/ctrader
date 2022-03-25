from backtesting import Strategy, Backtest
from backtesting.lib import Strategy, crossover
import talib
import numpy as np

class CustomStrat(Strategy):
    n1 = 1 #volatilityPercent
    n2 = 3 #stopLossRatio
    n3 = 1.3 #atr ratio
    #n2 = 200
    #n3 = 50
    #n4 = 20


    def init(self):
        super().init()
        self.rsi = self.I(talib.RSI, self.data.Close, 14)
        self.sma1 = self.I(talib.SMA, self.data.Close, 200)
        self.sma2 = self.I(talib.SMA, self.data.Close, 100)
        self.sma3 = self.I(talib.SMA, self.data.Close, 20)
        #self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        #self.stoch = self.I(talib.STOCHRSI, self.data.Close, 14, 5, 3, 0)
        self.signal1 = self.I(lambda: self.data.TotSignal)
        #self.trend = self.I(lambda: self.data.trend)
        self.volatilityPercent = self.I(lambda: self.data.volatilityPercent)

    def next(self):
        super().next()
        price = self.data.Close[-1]
        slatr = self.n3*self.data.ATR[-1]

        #"""
        for trade in self.trades:
                 if trade.is_long:
                     trade.sl = max(trade.sl or -np.inf,
                                    self.data.Close[-1] - self.data.ATR[-1] * 6)
                 else:
                     trade.sl = min(trade.sl or np.inf,
                                    self.data.Close[-1] + self.data.ATR[-1] * 6)
        #"""

        if self.data.TotSignal==2 and self.sma3 > self.sma2 and self.volatilityPercent >= self.n1 and len(self.trades)==0:
            sl1 = price - slatr
            tp1 = price + slatr*self.n2
            self.position.close()
            self.buy()

        elif self.data.TotSignal==1 and self.sma3 < self.sma2 and self.volatilityPercent >= self.n1  and len(self.trades)==0:
            sl1 = price + slatr
            tp1 = price - slatr*self.n2
            self.position.close()
            self.sell()
