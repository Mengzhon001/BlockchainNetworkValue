import requests
import pandas as pd
import io
import pandas as pd
import numpy as np
import statsmodels.api as sm

from statsmodels.tsa.seasonal import STL



def Dune_dataGet(QueryNo):
    url = "https://api.dune.com/api/v1/query/"+str(QueryNo)+"/results/csv"
    headers = {"X-DUNE-API-KEY": "mOZPvoZqvudprBcgosT8KdyUVWHtd0TW"}
    response = requests.request("GET", url, headers=headers)
    r = response.content
    return pd.read_csv(io.StringIO(r.decode('utf-8')))

def Data_get_combine(QueryNo,MktCap,token_id):
    # get the dune data
    Dune_data = Dune_dataGet(QueryNo)
    Dune_data['day'] = Dune_data['day'].astype(str)
    Dune_data['day'] = Dune_data['day'].str.split(pat=' ', expand=True)[0]
    # Dune_data.set_index('day', inplace=True)

    combined_data=pd.merge(Dune_data,MktCap[['day','Market_cap']],how='left',on='day')
    combined_data.set_index('day', inplace=True)
    combined_data=combined_data.dropna()
    combined_data.to_csv('/Users/andyma/Desktop/Python /BlockchainNetwork_Value/Data_raw_Dune_price/'+token_id+'_rawData_allTierUser.csv')
    print('Data loading finished!')
    return combined_data

def smooth_regression(data):

    # for ALL
    Data_all=data
    Data_all.dropna(inplace=True)
    Data_all.index=pd.to_datetime(Data_all.index)

    Data_all = Data_all[~(Data_all == 0).any(axis=1)]
    ########## average using STL
    var_list = list(Data_all.columns.values)
    var_list.remove('blockchain')
    var_list.remove('project')
    var_list.remove('Market_cap')
    for var in var_list:
        stl = STL(Data_all[var], period=15)
        res = stl.fit()
        Data_all[var+'_trend'] = res.trend
        pass
    return Data_all



## for ethereum
# if __name__ == '__main__':
#     QueryNo=3524562
#     token_id='ethereum'
#     users_var='dau_nonce_100'
#     users_previous='dau_nonce_10'
#     MktCap=pd.read_csv('/Users/andyma/Desktop/Python /BlockchainNetwork_Value/Data_raw_Dune_price/'+token_id+'_'+users_previous+'_rawData.csv')
#     MktCap=MktCap[['day','Market_cap']]
#     Dune_MktCap_raw=Data_get_combine(QueryNo,MktCap,users_var)
#     Dune_MktCap_trend=smooth_regression(Dune_MktCap_raw)
#     Dune_MktCap_trend.to_csv('/Users/andyma/Desktop/Python /BlockchainNetwork_Value/Data_Dune_MktCap/'+token_id+'_all_trend.csv')

# ## for ARB
# if __name__ == '__main__':
#     QueryNo=3523740
#     token_id='arbitrum'
#     users_var='dau_nonce_100'
#     users_previous='dau_nonce_10'
#     MktCap=pd.read_csv('/Users/andyma/Desktop/Python /BlockchainNetwork_Value/Data_raw_Dune_price/'+token_id+'_'+users_previous+'_rawData.csv')
#     MktCap=MktCap[['day','Market_cap']]
#     Dune_MktCap_raw=Data_get_combine(QueryNo,MktCap,users_var)
#     Dune_MktCap_trend=smooth_regression(Dune_MktCap_raw)
#     Dune_MktCap_trend.to_csv('/Users/andyma/Desktop/Python /BlockchainNetwork_Value/Data_Dune_MktCap/'+token_id+'_all_trend.csv')

# ## for OP
# if __name__ == '__main__':
#     QueryNo = 3524566
#     token_id='optimism'
#     users_var='dau_nonce_100'
#     users_previous='dau_nonce_10'
#     MktCap=pd.read_csv('/Users/andyma/Desktop/Python /BlockchainNetwork_Value/Data_raw_Dune_price/'+token_id+'_'+users_previous+'_rawData.csv')
#     MktCap=MktCap[['day','Market_cap']]
#     Dune_MktCap_raw=Data_get_combine(QueryNo,MktCap,users_var)
#     Dune_MktCap_trend=smooth_regression(Dune_MktCap_raw)
#     Dune_MktCap_trend.to_csv('/Users/andyma/Desktop/Python /BlockchainNetwork_Value/Data_Dune_MktCap/'+token_id+'_all_trend.csv')

# ## for Base
# if __name__ == '__main__':
#     QueryNo = 3524568
#     token_id='base'
#     users_var='dau_nonce_100'
#     users_previous='dau_nonce_10'
#     MktCap=pd.read_csv('/Users/andyma/Desktop/Python /BlockchainNetwork_Value/Data_raw_Dune_price/'+token_id+'_'+users_previous+'_rawData.csv')
#     MktCap=MktCap[['day','Market_cap']]
#     Dune_MktCap_raw=Data_get_combine(QueryNo,MktCap,users_var)
#     Dune_MktCap_trend=smooth_regression(Dune_MktCap_raw)
#     Dune_MktCap_trend.to_csv('/Users/andyma/Desktop/Python /BlockchainNetwork_Value/Data_Dune_MktCap/'+token_id+'_all_trend.csv')

# ## for OP
# if __name__ == '__main__':
#     QueryNo = 3524572
#     token_id='binancecoin'
#     users_var='dau_nonce_100'
#     users_previous='dau_nonce_10'
#     MktCap=pd.read_csv('/Users/andyma/Desktop/Python /BlockchainNetwork_Value/Data_raw_Dune_price/'+token_id+'_'+users_previous+'_rawData.csv')
#     MktCap=MktCap[['day','Market_cap']]
#     Dune_MktCap_raw=Data_get_combine(QueryNo,MktCap,users_var)
#     Dune_MktCap_trend=smooth_regression(Dune_MktCap_raw)
#     Dune_MktCap_trend.to_csv('/Users/andyma/Desktop/Python /BlockchainNetwork_Value/Data_Dune_MktCap/'+token_id+'_all_trend.csv')

# ## for Polygon
# if __name__ == '__main__':
#     QueryNo = 3524574
#     token_id='matic-network'
#     users_var='dau_nonce_100'
#     users_previous='dau_nonce_10'
#     MktCap=pd.read_csv('/Users/andyma/Desktop/Python /BlockchainNetwork_Value/Data_raw_Dune_price/'+token_id+'_'+users_previous+'_rawData.csv')
#     MktCap=MktCap[['day','Market_cap']]
#     Dune_MktCap_raw=Data_get_combine(QueryNo,MktCap,users_var)
#     Dune_MktCap_trend=smooth_regression(Dune_MktCap_raw)
#     Dune_MktCap_trend.to_csv('/Users/andyma/Desktop/Python /BlockchainNetwork_Value/Data_Dune_MktCap/'+token_id+'_all_trend.csv')

# ## for AVAX
# if __name__ == '__main__':
#     QueryNo = 3524582
#     token_id='avalanche-2'
#     users_var='dau_nonce_100'
#     users_previous='dau_nonce_10'
#     MktCap=pd.read_csv('/Users/andyma/Desktop/Python /BlockchainNetwork_Value/Data_raw_Dune_price/'+token_id+'_'+users_previous+'_rawData.csv')
#     MktCap=MktCap[['day','Market_cap']]
#     Dune_MktCap_raw=Data_get_combine(QueryNo,MktCap,users_var)
#     Dune_MktCap_trend=smooth_regression(Dune_MktCap_raw)
#     Dune_MktCap_trend.to_csv('/Users/andyma/Desktop/Python /BlockchainNetwork_Value/Data_Dune_MktCap/'+token_id+'_all_trend.csv')

# ## for uniswap
# if __name__ == '__main__':
#     QueryNo = 3488820
#     token_id='uniswap'
#     users_var='dau_usd_100'
#     users_previous='dau_usd_10'
#     MktCap=pd.read_csv('/Users/andyma/Desktop/Python /BlockchainNetwork_Value/Data_raw_Dune_price/'+token_id+'_'+users_previous+'_rawData.csv')
#     MktCap=MktCap[['day','Market_cap']]
#     Dune_MktCap_raw=Data_get_combine(QueryNo,MktCap,users_var)
#     Dune_MktCap_trend=smooth_regression(Dune_MktCap_raw)
#     Dune_MktCap_trend.to_csv('/Users/andyma/Desktop/Python /BlockchainNetwork_Value/Data_Dune_MktCap/'+token_id+'_all_trend.csv')

## for shushiswap
if __name__ == '__main__':
    QueryNo = 3488783
    token_id='sushi'
    users_var='dau_usd_100'
    users_previous='dau_usd_10'
    MktCap=pd.read_csv('/Users/andyma/Desktop/Python /BlockchainNetwork_Value/Data_raw_Dune_price/'+token_id+'_'+users_previous+'_rawData.csv')
    MktCap=MktCap[['day','Market_cap']]
    Dune_MktCap_raw=Data_get_combine(QueryNo,MktCap,users_var)
    Dune_MktCap_trend=smooth_regression(Dune_MktCap_raw)
    Dune_MktCap_trend.to_csv('/Users/andyma/Desktop/Python /BlockchainNetwork_Value/Data_Dune_MktCap/'+token_id+'_all_trend.csv')