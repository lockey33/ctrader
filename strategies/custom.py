from backtesting import Strategy, Backtest
from backtesting.lib import Strategy, crossover
import talib
import numpy as np

class CustomStrat(Strategy):
    n1 = 3.7 #volatilityPercent
    n2 = 8 #atr ratio
    n3 = -0.05 # stop loss
    #n2 = 200
    #n3 = 50
    #n4 = 20
    waitForCloseToEma200 = False


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

        if(self.position.pl_pct < self.n3):
            self.position.close()
            self.waitForCloseToEma200 = True

        for trade in self.trades:
            """
            if(trade.entry_time==5003):
                print(trade)
                print(self.position.pl_pct)
                print(trade.pl_pct)
            """
            if trade.is_long:
                trade.sl = max(trade.sl or -np.inf, self.data.Close[-1] - self.data.ATR[-1] * self.n2)
            else:
                trade.sl = min(trade.sl or np.inf, self.data.Close[-1] + self.data.ATR[-1] * self.n2)
        if self.waitForCloseToEma200 == False or (self.waitForCloseToEma200 == True and self.data.closeToEma200[-1] == 1):
            self.waitForCloseToEma200 = False
            if self.data.TotSignal==2 and self.sma3 > self.sma2 and self.volatilityPercent >= self.n1 and len(self.trades)==0:
                self.position.close()
                self.buy()

            elif self.data.TotSignal==1 and self.sma3 < self.sma2 and self.volatilityPercent >= self.n1  and len(self.trades)==0:
                self.position.close()
                self.sell()
        #"""
