from backtesting import Strategy, Backtest
from backtesting.lib import Strategy, crossover
import talib
import numpy as np
import sys
class SmaCross(Strategy):

    n1 = 4 #atr ratio
    n2 = 25 # atr profit ratio
    n3 = 5 #candleToWait


    def init(self):
        super().init()

        self.sma1 = self.I(talib.SMA, self.data.Close, 200)
        self.sma2 = self.I(talib.SMA, self.data.Close, 100)
        self.sma3 = self.I(talib.SMA, self.data.Close, 50)
        self.sma4 = self.I(talib.SMA, self.data.Close, 20)
        #self.rsi = self.I(talib.RSI, self.data.Close, 6)
        #self.adx = self.I(talib.ADX, self.data.High, self.data.Low, self.data.Close, 14)
        self.macd = self.I(talib.MACD, self.data.Close)
        #self.set_trailing_sl(2)



    def next(self):
        super().next()
        def trade(self):
            for trade in self.trades:
                if trade.is_long:
                    if crossover(self.sma3, self.sma4):
                        self.position.close()
                else:
                    if crossover(self.sma3, self.sma4):
                        self.position.close()

            if (crossover(self.sma4, self.sma1)):
                self.position.close()
                self.buy(sl=self.data.Close[-1] - self.data.ATR[-1] * self.n1, tp=self.data.Close[-1] + self.data.ATR[-1] * (self.n2))
                if len(self.closed_trades) >= 1:
                    lastTrade = self.closed_trades[-1]
                    print(lastTrade.exit_bar, self.data.index.stop)
            elif (crossover(self.sma1, self.sma4)):
                self.position.close()
                self.sell(sl=self.data.Close[-1] + self.data.ATR[-1] * self.n1, tp=self.data.Close[-1] - self.data.ATR[-1] * (self.n2))
                if len(self.closed_trades) >= 1:
                    lastTrade = self.closed_trades[-1]
                    print(lastTrade.exit_bar, self.data.index.stop)
        """
        if(self.position.pl_pct < -0.05):
            self.position.close()
        """
        if len(self.closed_trades) >= 1:
            lastTrade = self.closed_trades[-1]
            if self.data.index.stop + self.n3 > lastTrade.exit_bar : #on attend entre chaque position cloturées
                trade(self)

        elif len(self.closed_trades) == 0 :
            print("here")
            trade(self)




