from strategies.rsi import RsiStrat
from strategies.custom import CustomStrat
from strategies.sma import SmaCross
from strategies.smaOpti import SmaOpti
from strategies.smaLong import SmaLong
from binance.client import Client
from backtesting import Backtest
from datetime import datetime
import pytz
import pandas as pd
import pandas_ta as ta
import sys
import numpy as np
from dateutil import parser
from indicators.custom import PPSR

df = pd.read_csv("EURUSD_M15_2022-01-02_2022-03-31.csv")

#Check if NA values are in data
df=df[df['volume']!=0]
df.reset_index(drop=True, inplace=True)
df.isna().sum()
df.tail()
df['Close'] = pd.to_numeric(df['close'])
df['High'] = pd.to_numeric(df['high'])
df['Low'] = pd.to_numeric(df['low'])
df['Open'] = pd.to_numeric(df['open'])

length = len(df)
n1=2
n2=2
backCandles=30
signal = [0] * length

df["EMA200"] = ta.ema(df.Close, length=200)
df["EMA100"] = ta.ema(df.Close, length=100)
df["EMA20"] = ta.ema(df.Close, length=20)
df["RSI"] = ta.rsi(df.Close, length=3)
df['ATR']= df.ta.atr()

def get_diff(current, previous):
    if current == previous:
        return 100.0
    try:
        return (abs(current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return 0

trend = [0]*len(df)
closeToEma200 = [0]*len(df)
closeToEma100 = [0]*len(df)
closeToEma20 = [0]*len(df)
percentDiff = [0]*len(df)
backcandles = 8
volatilityPercent = [0]*len(df)
maxDiff=0.01


for row in range(backcandles-1, len(df)):
    upt = 1
    dnt = 1

    for i in range(row-backcandles, row+1):
        percentDiff[row] = get_diff(df.Close[row], df.EMA200[row])
        if percentDiff[row] <= maxDiff:
            closeToEma200[row]=1
        else:
            closeToEma200[row]=0

        percentDiff[row] = get_diff(df.Close[row], df.EMA100[row])
        if percentDiff[row] <= maxDiff:
            closeToEma100[row]=1
        else:
            closeToEma100[row]=0

        percentDiff[row] = get_diff(df.Close[row], df.EMA20[row])
        if percentDiff[row] <= maxDiff:
            closeToEma20[row]=1
        else:
            closeToEma20[row]=0

        volatilityPercent[row] = get_diff(df.EMA100[row], df.EMA20[row])

        if df.Close[row]>=df.EMA200[row]:
            dnt=0
        if df.Close[row]<=df.EMA200[row]:
            upt=0

    if upt==1 and dnt==1:
        #print("!!!!! check trend loop !!!!")
        trend[row]=0
    elif upt==1:
        trend[row]=2
    elif dnt==1:
        trend[row]=1

df['trend'] = trend
df['percentDiff'] = percentDiff
df['closeToEma200']= closeToEma200
df['closeToEma100']= closeToEma100
df['closeToEma20']= closeToEma20
df['volatilityPercent']= volatilityPercent

TotSignal = [0] * len(df)
for row in range(0, len(df)):
    TotSignal[row] = 0
    if df.trend[row]==1:
        TotSignal[row]=1
    if df.trend[row]==2:
        TotSignal[row]=2
df['TotSignal']=TotSignal
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)
#print(df.tail())
months = 24*4*30
startid = 0
dfpl = df[startid:startid+30*months]

bt = Backtest(dfpl, SmaLong, margin=1/3, cash=100000, commission=0.001, exclusive_orders=True)
stats = bt.run()
"""
stats = bt.optimize(n1=np.linspace(1, 10, 20).tolist(),
                    n2=np.linspace(1, 30, 20).tolist(),
                    n3=range(1, 30, 20),
                    maximize=lambda stats: -stats['Max. Drawdown [%]'],
                    constraint=lambda param: param.n2 > param.n1
)
"""
print(stats)
bt.plot()
#print(stats._strategy)
#print(stats['_trades'])
