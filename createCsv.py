import oandapyV20
import oandapyV20.endpoints.instruments as instruments
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
client =  oandapyV20.API(access_token="bbaaf27390b9331a572bbcc6aab53330-462bdb18312ec94066fd0d5ff37d1912")
step=21600*12*15 # equals to 6h in UNIX_time.Depends on granulariy.
# for 5s 6 hours is maximum granularity time.
# for 1m 21600*12 for 5m 21600*12*5.
granularity="M15"
begin_unix=int(parser.parse("2022-01-01 00:00:00 EDT").strftime('%s'))
end_unix=int(parser.parse("2022-04-01 00:000:00 EDT").strftime('%s'))

i=begin_unix+step
dataset=pd.DataFrame()
params={"from": str(i-step),
        "to": str(i),
        "granularity":granularity,
        "price":'A' } # 'A' stands for ask price;
                      # if you want to get Bid use 'B' instead or 'AB' for both.
while i<=end_unix:
    params['from']=str(i-step)
    params['to']=str(i)
    r=instruments.InstrumentsCandles(instrument="EUR_USD",params=params)
    data = client.request(r)
    results= [{"time":x['time'],"open":float(x['ask']['o']),"high":float(x['ask']['h']),
              "low":float(x['ask']['l']),"close":float(x['ask']['c']),"volume":float(x['volume'])} for x in data['candles']]
    df = pd.DataFrame(results)
    if dataset.empty: dataset=df.copy()
    else: dataset=dataset.append(df, ignore_index=True)
    if(i+step)>=end_unix:
        params['from']=str(i)
        params['to']=str(end_unix)
        r=instruments.InstrumentsCandles(instrument="EUR_USD",params=params)
        data = client.request(r)
        results= [{"time":x['time'],"open":float(x['ask']['o']),"high":float(x['ask']['h']),
                  "low":float(x['ask']['l']),"close":float(x['ask']['c'])} for x in data['candles']]
        df = pd.DataFrame(results)
        i+=step
        dataset=dataset.append(df, ignore_index=True)
    if len(dataset)>2000000:
        dataset.to_csv("EURUSD"+"_"+granularity+"_"+dataset['time'][0].split('T')[0]+"_"+dataset['time'][len(dataset)-1].split('T')[0]+'.csv',index=False)
        dataset=pd.DataFrame()
    i+=step
dataset.to_csv("EURUSD"+"_"+granularity+"_"+dataset['time'][0].split('T')[0]+"_"+dataset['time'][len(dataset)-1].split('T')[0]+'.csv',index=False)