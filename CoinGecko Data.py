import pandas as pd
import requests
import json

url = 'https://api.coingecko.com/api/v3/coins/list'
response = requests.get(url)
if response.status_code != 200:
    print("Unable to Connect!")
else:
    crypto_list = pd.DataFrame(json.loads(response.text))
    data = pd.DataFrame()
    for i in range (len(crypto_list['symbol'])):
        coin_id = crypto_list['id'][i]
        coin_symbol = crypto_list['symbol'][i]
        # USDT, DAI, UST not included
        if coin_symbol not in ['usdt', 'dai', 'ust']:
            print(f'{i} id: {coin_id}, symbol: {coin_symbol}') 
            url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart/range?vs_currency=usd&from=1604170800&to=1636570800'
            response = requests.get(url)
            if response.status_code == 200:
                temp = pd.DataFrame(json.loads(response.text))
                temp.insert(0, 'Symbol', coin_symbol)
                data = data.append(temp)
            else:
                print(f'===============NO RESPONSE FOR: {coin_symbol}')
    
    data.index = [i for i in range(len(data))]
    data.insert(1, 'Date', 0)
    data.insert(2, 'Price', 0)
    data.insert(3, 'Market Capital', 0)
    data.insert(4, 'Total Volume', 0)
    
    for i in range(len(data)):
        data.loc[i, 'Date'] = pd.to_datetime(data.loc[i, 'prices'][0], 
                                         unit ='ms')
        data.loc[i, 'Price'] = data['prices'][i][1]
        data.loc[i, 'Market Capital'] = data.loc[i, 'market_caps'][1]
        data.loc[i, 'Total Volume'] = data.loc[i, 'total_volumes'][1]
    
    data['Date'] = pd.to_datetime(data['Date'], format = '%Y-%m-%d')
    data.index = data['Date']
    
    del data['Date']
    del data['prices']
    del data['market_caps']
    del data['total_volumes']
    
    data.to_csv("Crypto_data.csv", index = True)
