import pandas as pd

def logResult(df, params, dt):
    #///////////////////////////////////////
    print("Period : [" + str(df.index[0]) + "] -> [" +str(df.index[len(df)-1]) + "]")
    dt = dt.set_index(dt['date'])
    dt.index = pd.to_datetime(dt.index)
    dt['resultat'] = dt['wallet'].diff()
    dt['resultat%'] = dt['wallet'].pct_change()*100
    dt.loc[dt['position']=='Buy','resultat'] = None
    dt.loc[dt['position']=='Buy','resultat%'] = None


    dt['tradeIs'] = ''
    dt.loc[dt['resultat']>0,'tradeIs'] = 'Good'
    dt.loc[dt['resultat']<=0,'tradeIs'] = 'Bad'

    iniClose = df.iloc[0]['close']
    lastClose = df.iloc[len(df)-1]['close']
    holdPorcentage = ((lastClose - iniClose)/iniClose) * 100
    algoPorcentage = ((params['wallet'] - params['initialWallet'])/params['initialWallet']) * 100
    vsHoldPorcentage = ((algoPorcentage - holdPorcentage)/holdPorcentage) * 100


    print("Starting balance : " + str(params['initialWallet']) + " $")
    print("Final balance :",round(params['wallet'],2),"$")
    print("Performance vs US Dollar :",round(algoPorcentage,2),"%")
    print("Buy and Hold Performence :",round(holdPorcentage,2),"%")
    print("Performance vs Buy and Hold :",round(vsHoldPorcentage,2),"%")
    print("Number of negative trades : ",dt.groupby('tradeIs')['date'].nunique()['Bad'])
    print("Number of positive trades : ",dt.groupby('tradeIs')['date'].nunique()['Good'])
    print("Average Positive Trades : ",round(dt.loc[dt['tradeIs'] == 'Good', 'resultat%'].sum()/dt.loc[dt['tradeIs'] == 'Good', 'resultat%'].count(),2),"%")
    print("Average Negative Trades : ",round(dt.loc[dt['tradeIs'] == 'Bad', 'resultat%'].sum()/dt.loc[dt['tradeIs'] == 'Bad', 'resultat%'].count(),2),"%")
    idbest = dt.loc[dt['tradeIs'] == 'Good', 'resultat%'].idxmax()
    idworst = dt.loc[dt['tradeIs'] == 'Bad', 'resultat%'].idxmin()
    print("Best trade +"+str(round(dt.loc[dt['tradeIs'] == 'Good', 'resultat%'].max(),2)),"%, the ",dt['date'][idbest])
    print("Worst trade",round(dt.loc[dt['tradeIs'] == 'Bad', 'resultat%'].min(),2),"%, the ",dt['date'][idworst])
    print("Worst drawBack", str(100*round(dt['drawBack'].min(),2)),"%")
    print("Total fee : ",round(dt['frais'].sum(),2),"$")

    dt[['wallet','price']].plot(subplots=True, figsize=(12,10))
