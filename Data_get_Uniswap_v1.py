import requests
import pandas as pd
import io
import json
import datetime


def Dune_dataGet(QueryNo):
    url = "https://api.dune.com/api/v1/query/"+str(QueryNo)+"/results/csv"
    headers = {"X-DUNE-API-KEY": "MUW8YOevxlDZtOW5KIIB3h6Dq7wUJ8PR"}
    response = requests.request("GET", url, headers=headers)
    r = response.content
    return pd.read_csv(io.StringIO(r.decode('utf-8')))

def TradingHistory(token_id):
    url_1='https://api.coingecko.com/api/v3/coins/'
    url_2='/market_chart/range?vs_currency=usd&from=1546300800&to=1683072000' # get the pricing data from 20190101 to 20230503
    url=url_1+str(token_id)+url_2
    headers = {
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    data = response.text
    data_dict = json.loads(data)
    return data_dict
pass

Data_UNI=TradingHistory('uniswap')
Data_UNI_MktCap=pd.DataFrame(Data_UNI['market_caps'],columns=['day','Market_cap'])
Data_UNI_MktCap['day']=pd.to_datetime(Data_UNI_MktCap['day'],unit='ms')
Data_UNI_MktCap['day']=Data_UNI_MktCap['day'].astype(str)
Data_UNI_MktCap['day']=Data_UNI_MktCap['day'].str.split(pat=' ', expand=True)[0]
Data_UNI_MktCap.set_index('day',inplace=True)

Uniswap_ETH_DAU = Dune_dataGet(3488164)
Uniswap_ETH_DAU.set_index('day',inplace=True)
Uniswap_ARB_DAU = Dune_dataGet(3488793)
Uniswap_ARB_DAU.set_index('day',inplace=True)
Uniswap_Polygon_DAU = Dune_dataGet(3488803)
Uniswap_Polygon_DAU.set_index('day',inplace=True)
Uniswap_OPT_DAU_MAU = Dune_dataGet(3500098)
Uniswap_OPT_DAU_MAU.set_index('day',inplace=True)# for both DAU and MAU
Uniswap_Base_DAU_MAU = Dune_dataGet(3500119)
Uniswap_Base_DAU_MAU.set_index('day',inplace=True) # for both DAU and MAU
Uniswap_AVAX_DAU_MAU = Dune_dataGet(3500160)
Uniswap_AVAX_DAU_MAU.set_index('day',inplace=True)# for both DAU and MAU
Uniswap_BSC_DAU_MAU = Dune_dataGet(3500201)
Uniswap_BSC_DAU_MAU.set_index('day',inplace=True)# for both DAU and MAU
Uniswap_Celo_DAU_MAU = Dune_dataGet(3500234)
Uniswap_Celo_DAU_MAU.set_index('day',inplace=True)# for both DAU and MAU
Uniswap_all_DAU = Dune_dataGet(3488820)
Uniswap_all_DAU.set_index('day',inplace=True)

Uniswap_chain_list=['ETH','ARB','Polygon','OPT','Base','AVAX','BSC','Celo','All']
Uniswap_DAU_table=pd.DataFrame(columns=Uniswap_chain_list,
                               index=Uniswap_all_DAU.index.tolist())
Uniswap_DAU_table['ETH']= Uniswap_ETH_DAU['daily active users']
Uniswap_DAU_table['ARB']= Uniswap_ARB_DAU['daily active users']
Uniswap_DAU_table['Polygon']= Uniswap_Polygon_DAU['daily active users']
Uniswap_DAU_table['OPT']= Uniswap_OPT_DAU_MAU['daily_active_users']
Uniswap_DAU_table['Base']= Uniswap_Base_DAU_MAU['daily_active_users']
Uniswap_DAU_table['AVAX']= Uniswap_AVAX_DAU_MAU['daily_active_users']
Uniswap_DAU_table['BSC']= Uniswap_BSC_DAU_MAU['daily_active_users']
Uniswap_DAU_table['Celo']= Uniswap_Celo_DAU_MAU['daily_active_users']
Uniswap_DAU_table['All']= Uniswap_all_DAU['daily active users']

Uniswap_DAU_table['day']=Uniswap_DAU_table.index
Uniswap_DAU_table['day']=Uniswap_DAU_table['day'].astype(str)
Uniswap_DAU_table['day']=Uniswap_DAU_table['day'].str.split(pat=' ', expand=True)[0]
Uniswap_DAU_table.set_index('day',inplace=True)

Uniswap_DAU_table['Market_cap']=Data_UNI_MktCap['Market_cap']

Uniswap_DAU_table.to_csv('Uniswap_DAU.csv')




