import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt


from statsmodels.tsa.seasonal import STL

def smooth_regression(token_id,users_var,MktCap_var):

    data=pd.read_csv('/Users/andyma/Desktop/Python /BlockchainNetwork_Value/Data_raw_Dune_price/'+token_id+'_'+users_var+'_rawData.csv',index_col='day')


    # for ALL
    Data_all=data[[users_var,MktCap_var]]
    Data_all.dropna(inplace=True)
    Data_all.index=pd.to_datetime(Data_all.index)

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

    Data_all.to_csv('/Users/andyma/Desktop/Python /BlockchainNetwork_Value/Data_for_plotting/'+token_id+'_'+users_var+'_forPlotting.csv')

# # for ethereum
# if __name__ == '__main__':
#     token_id='ethereum'
#     users_var='dau_nonce_10'
#     MktCap_var='Market_cap'
#     smooth_regression(token_id,users_var,MktCap_var)

# for ethereum
if __name__ == '__main__':
    token_id='ethereum'
    users_var='dau'
    MktCap_var='Market_cap'
    smooth_regression(token_id,users_var,MktCap_var)

# # for arbitrum
# if __name__ == '__main__':
#     token_id='arbitrum'
#     users_var='dau_nonce_10'
#     MktCap_var='Market_cap'
#     smooth_regression(token_id,users_var,MktCap_var)

# # for optimism
# if __name__ == '__main__':
#     token_id='optimism'
#     users_var='dau_nonce_10'
#     MktCap_var='Market_cap'
#     smooth_regression(token_id,users_var,MktCap_var)

# # for optimism
# if __name__ == '__main__':
#     token_id='optimism'
#     users_var='dau_nonce_10'
#     MktCap_var='Market_cap'
#     smooth_regression(token_id,users_var,MktCap_var)

# # for bsc
# if __name__ == '__main__':
#     token_id='binancecoin'
#     users_var='dau_nonce_10'
#     MktCap_var='Market_cap'
#     smooth_regression(token_id,users_var,MktCap_var)

# # for polygon
# if __name__ == '__main__':
#     token_id='matic-network'
#     users_var='dau_nonce_10'
#     MktCap_var='Market_cap'
#     smooth_regression(token_id,users_var,MktCap_var)

# # for AVAX
# if __name__ == '__main__':
#     token_id='avalanche-2'
#     users_var='dau_nonce_10'
#     MktCap_var='Market_cap'
#     smooth_regression(token_id,users_var,MktCap_var)

# # for uniswap
# if __name__ == '__main__':
#     token_id='uniswap'
#     users_var='dau_usd_10'
#     MktCap_var='Market_cap'
#     smooth_regression(token_id,users_var,MktCap_var)

# # for sushi
# if __name__ == '__main__':
#     token_id='sushi'
#     users_var='dau_usd_10'
#     MktCap_var='Market_cap'
#     smooth_regression(token_id,users_var,MktCap_var)