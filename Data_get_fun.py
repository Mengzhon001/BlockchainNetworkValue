import requests
import pandas as pd
import io
import json



def Dune_dataGet(QueryNo):
    url = "https://api.dune.com/api/v1/query/"+str(QueryNo)+"/results/csv"
    headers = {"X-DUNE-API-KEY": "MUW8YOevxlDZtOW5KIIB3h6Dq7wUJ8PR"}
    response = requests.request("GET", url, headers=headers)
    r = response.content
    return pd.read_csv(io.StringIO(r.decode('utf-8')))

def TradingHistory(token_id):
    url_1='https://api.coingecko.com/api/v3/coins/'
    url_2='/market_chart/range?vs_currency=usd&from=1206080301&to=1711001933' # get the pricing data from 20190101 to 20230503
    url=url_1+str(token_id)+url_2
    headers = {
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    data = response.text
    data_dict = json.loads(data)
    return data_dict
pass


def Data_get_combine(QueryNo,token_id,users_var):
    # get and clean the market cap data
    Data_token = TradingHistory(token_id)
    Data_token_MktCap = pd.DataFrame(Data_token['market_caps'], columns=['day', 'Market_cap'])
    Data_token_MktCap['day'] = pd.to_datetime(Data_token_MktCap['day'], unit='ms')
    Data_token_MktCap['day'] = Data_token_MktCap['day'].astype(str)
    Data_token_MktCap['day'] = Data_token_MktCap['day'].str.split(pat=' ', expand=True)[0]
    # Data_token_MktCap.set_index('day', inplace=True)
    # get the dune data
    Dune_data = Dune_dataGet(QueryNo)
    Dune_data['day'] = Dune_data['day'].astype(str)
    Dune_data['day'] = Dune_data['day'].str.split(pat=' ', expand=True)[0]
    # Dune_data.set_index('day', inplace=True)
    # combine data
    combined_data=Dune_data[['day',users_var]]
    # combined_data['Market_cap']=None
    # combined_data['Market_cap']=Data_token_MktCap['Market_cap']
    combined_data=pd.merge(combined_data,Data_token_MktCap[['day','Market_cap']],how='left',on='day')
    combined_data.set_index('day', inplace=True)
    combined_data=combined_data.dropna()
    combined_data.to_csv('/Users/andyma/Desktop/Python /BlockchainNetwork_Value/Data_raw_Dune_price/'+token_id+'_'+users_var+'_rawData.csv')
    print('Data loading finished!')
    pass


## for ethereum
if __name__ == '__main__':
    QueryNo=3524562
    token_id='ethereum'
    users_var='dau_nonce_10'
    Data_get_combine(QueryNo,token_id,users_var)

# for ethereum
# if __name__ == '__main__':
#     QueryNo=3524562
#     token_id='ethereum'
#     users_var='dau'
#     Data_get_combine(QueryNo,token_id,users_var)

# # for arbitrum
# if __name__ == '__main__':
#     QueryNo=3523740
#     token_id='arbitrum'
#     users_var='dau_nonce_10'
#     Data_get_combine(QueryNo,token_id,users_var)


# # for optimism
# if __name__ == '__main__':
#     QueryNo=3524566
#     token_id='optimism'
#     users_var='dau_nonce_10'
#     Data_get_combine(QueryNo,token_id,users_var)

# # for base
# if __name__ == '__main__':
#     QueryNo=3524568
#     token_id='base'
#     users_var='dau_nonce_10'
#     Data_get_combine(QueryNo,token_id,users_var)

# # for bsc
# if __name__ == '__main__':
#     QueryNo=3524572
#     token_id='binancecoin'
#     users_var='dau_nonce_10'
#     Data_get_combine(QueryNo,token_id,users_var)


# # for polygon
# if __name__ == '__main__':
#     QueryNo=3524574
#     token_id='matic-network'
#     users_var='dau_nonce_10'
#     Data_get_combine(QueryNo,token_id,users_var)

# ## for AVAX
# if __name__ == '__main__':
#     QueryNo=3524582
#     token_id='avalanche-2'
#     users_var='dau_nonce_10'
#     Data_get_combine(QueryNo,token_id,users_var)

# ## for uniswap
# if __name__ == '__main__':
#     QueryNo=3488820
#     token_id='uniswap'
#     users_var='dau_usd_10'
#     Data_get_combine(QueryNo,token_id,users_var)

# ## for sushiswap
# if __name__ == '__main__':
#     QueryNo=3488783
#     token_id='sushi'
#     users_var='dau_usd_10'
#     Data_get_combine(QueryNo,token_id,users_var)

