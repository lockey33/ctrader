import time
import pandas as pd
from binance.client import Client
import ta
import mplfinance as mpf
import warnings
warnings.filterwarnings("ignore")
from logger import *
import numpy as np
from trading import *



def doBackTest(df, plot=False):
    dt = None
    dt = pd.DataFrame(columns = ['date','position', 'price', 'frais' ,'fiat', 'coins', 'wallet', 'drawBack'])

    params = {
        "usdt" : 1000,
        "initialWallet" : 1000,
        "coin" : 0,
        "wallet" : 1000,
        "lastAth" : 0,
        "lastIndex" : df.first_valid_index(),
        "fee" : 0.001,
        "leverage" : 10
    }

    up_markers = []
    down_markers = []

    for index, row in df.iterrows():
      trade=False
      isLong=False
      entryPrice=0
      #Buy
      if row['RSI'] < 20:# and  params['usdt'] > 0:
        #params['coin'] = params['usdt'] / row['close']
        #params['frais'] = params['fee'] * params['coin']
        #params['coin'] = params['coin'] - params['frais']
        #params['usdt'] = 0
        #params['wallet'] = params['coin'] * row['close']
        #if params['wallet'] > params['lastAth']:
        #  params['lastAth'] = params['wallet']
        # print("Buy COIN at",df['close'][index],'$ the', index)
        #myrow = {'date': index,'position': "Buy",'price': row['close'],'frais': params['frais'] * row['close'],'fiat': params['usdt'],'coins': params['coin'],'wallet': params['wallet'],'drawBack':(params['wallet']-params['lastAth'])/params['lastAth']}
        #dt = dt.append(myrow,ignore_index=True)
        up_markers.append(row['close'])
        down_markers.append(np.nan)
        trade=True
        isLong=True

      #Sell
      if row['RSI'] > 80:# and params['coin'] > 0:
        #params['usdt'] = params['coin'] * row['close']
        #params['frais'] = params['fee'] * params['usdt']
        #params['usdt'] = params['usdt'] - params['frais']
        #params['coin'] = 0
        #params['wallet'] = params['usdt']
        #if params['wallet'] > params['lastAth']:
        #  params['lastAth'] = params['wallet']
        # print("Sell COIN at",df['close'][index],'$ the', index)
        #myrow = {'date': index,'position': "Sell",'price': row['close'],'frais': params['frais'],'fiat': params['usdt'],'coins': params['coin'],'wallet': params['wallet'],'drawBack':(params['wallet']-params['lastAth'])/params['lastAth']}
        #dt = dt.append(myrow,ignore_index=True)
        down_markers.append(row['close'])
        up_markers.append(np.nan)
        trade=True
        isLong=False

      lastIndex = index
      if trade == False:
        up_markers.append(np.nan)
        down_markers.append(np.nan)


    up_plot = mpf.make_addplot(up_markers, type='scatter', marker='v', color='red', markersize=100, panel=0)
    down_plot = mpf.make_addplot(down_markers, type='scatter', marker='^', markersize=100, panel=0)

    plots = [up_plot, down_plot]

    #logResult(df, params, dt)
    #print(dt)
    mpf.plot(df, type='candle', volume=True, style='yahoo', addplot=plots, figratio=(20,12), title='BTCUSDT')


