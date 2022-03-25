from backtesting import Strategy, Backtest
from backtesting.lib import Strategy, crossover
import talib


class SmaCross(Strategy):
    n1 = 20
    n2 = 45
    n3 = 4

    takeProfit=3
    stopLoss=1



    def init(self):
        super().init()

        self.sma1 = self.I(talib.SMA, self.data.Close, self.n1)
        self.sma2 = self.I(talib.SMA, self.data.Close, self.n2)
        self.rsi = self.I(talib.RSI, self.data.Close, self.n3)
        #self.set_trailing_sl(2)

    def next(self):
        super().next()
        price = self.data.Close[-1]
        if crossover(self.sma1, self.sma2) and self.rsi < 25:
            self.position.close()
            self.buy(sl=price-price*self.stopLoss/100, tp = price+price*self.takeProfit/100)
        elif crossover(self.sma2, self.sma1) and self.rsi > 75:
            self.position.close()
            self.sell(sl=price+price*self.stopLoss/100, tp = price - price*self.takeProfit/100)


