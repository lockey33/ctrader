from backtesting import Strategy, Backtest
from backtesting.lib import Strategy, crossover
import talib
import pandas_ta as ta


class RsiStrat(Strategy):
    n1 = 14
    n2 = 7
    n3 = 200

    n4 = 6

    takeProfit=5
    stopLoss=2



    def init(self):
        super().init()

        #self.trend1 = self.I(ta.supertrend, self.data.High, self.data.Low, self.data.Close, self.n1, self.n2)
        self.sma1 = self.I(talib.SMA, self.data.Close, self.n1)
        self.sma2 = self.I(talib.SMA, self.data.Close, self.n2)
        self.sma3 = self.I(talib.SMA, self.data.Close, self.n3)
        self.rsi = self.I(talib.RSI, self.data.Close, self.n3)
        #self.set_trailing_sl(2)

    def next(self):
        super().next()
        price = self.data.Close[-1]
        if crossover(self.sma1, self.sma2) and price > self.sma3:
            self.position.close()
            self.buy(sl=price-price*self.stopLoss/100, tp = price+price*self.takeProfit/100)
            #self.buy()
        elif crossover(self.sma2, self.sma1) and price < self.sma3:
            self.position.close()
            self.sell(sl=price+price*self.stopLoss/100, tp = price - price*self.takeProfit/100)
            #self.sell()


