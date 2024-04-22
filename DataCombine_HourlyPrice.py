import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.seasonal import STL

Price_hourly=pd.read_csv('/Users/andyma/Desktop/Python /BlockchainNetwork_Value/Price_hourly_data/ARBUSDT.csv')
Dune_raw=pd.read_csv('/Users/andyma/Desktop/Python /BlockchainNetwork_Value/Data_raw_Dune_price/arbitrum_dau_nonce_10_rawData.csv')

'''
Circulating supply of ARB:
2023-03-23 to 2024-03-15  1.28 B (1.28*10^9)
2024-03-16 to -   2.39 B (2.39*10^9)
'''

Price_hourly=Price_hourly[['openTime','open']]
Price_hourly['openTime']=Price_hourly['openTime']/1000
Price_hourly['openTime_dateHour'] = pd.to_datetime(Price_hourly['openTime'],unit='s')
Price_hourly['openTime_dateHour'] = Price_hourly['openTime_dateHour'].apply(lambda x: str(x))
Price_hourly['openTime_date']=Price_hourly['openTime_dateHour'].str.split(pat=' ', expand=True)[0]
Price_hourly['Cir_supply'] = float(1.28*10**9)
Price_hourly.loc[Price_hourly['openTime_date']>='2024-03-16','Cir_supply']=2.39*10**9
Price_hourly['Market_cap']=Price_hourly['Cir_supply']*Price_hourly['open']
Price_hourly.rename(columns={'openTime_date':'day'},inplace=True)

Dune_raw=Dune_raw[['day','dau_nonce_10']]
ARB_nonce10_MktCap1H=pd.merge(Price_hourly,Dune_raw,on='day',how='left')
ARB_nonce10_MktCap1H=ARB_nonce10_MktCap1H[['openTime_dateHour','dau_nonce_10','Market_cap']]
ARB_nonce10_MktCap1H.rename(columns={'openTime_dateHour':'day'},inplace=True)

def smooth_regression(data,users_var,MktCap_var):

    # for ALL
    Data_all=data[['day',users_var,MktCap_var]]
    Data_all.dropna(inplace=True)
    Data_all.index=pd.to_datetime(Data_all['day'])

    Data_all = Data_all[~(Data_all == 0).any(axis=1)]
    ########## average using STL
    stl = STL(Data_all[users_var],period=15)
    res = stl.fit()
    Data_all['Users_trend']=res.trend
    Data_all['Users_seasonal']=res.seasonal
    Data_all['Users_resid']=res.resid
    # fig.show()

    ########## regression
    y=np.log(Data_all[MktCap_var])
    x=np.log(Data_all[users_var]) # for the original users
    x = sm.add_constant(x)
    x_smooth=np.log(Data_all['Users_trend']) # for the smoothed series of users number
    x_smooth = sm.add_constant(x_smooth)
    model = sm.OLS(y, x, hasconst=1 )
    results = model.fit()
    print(results.summary())

    Data_all['Fitted_Market_cap']=np.exp(results.predict()) # fitted values with original users number
    Data_all.loc[:,'Fitted_Market_cap_trend']=np.exp(results.predict(x_smooth)) # fitted values with smoothed users number

    return Data_all

Data_proccessed=smooth_regression(ARB_nonce10_MktCap1H,'dau_nonce_10','Market_cap')
Data_proccessed.to_csv('/Users/andyma/Desktop/Python /BlockchainNetwork_Value/Data_for_plotting/ARB_nonce10_MktCap1H.csv')