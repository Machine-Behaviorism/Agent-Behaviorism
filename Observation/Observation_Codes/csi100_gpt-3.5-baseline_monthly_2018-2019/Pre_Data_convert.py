# -*- coding: utf-8 -*-
import os
import Configs

# Import the stock codes of all files in a given directory
def get_stock_code_list_in_one_dir(path):
    stock_list = []

    # System function os.walk is used to traverse all files in a directory
    import os
    for root, dirs, files in os.walk(path):
        if files:  # When files is not empty
            for f in files:
                if f.endswith('.csv'):
                    stock_list.append(f.split(".csv")[0])

    return stock_list

def transfer_to_period_data(df, period_type='w'):
    # Set 'date' as the index
    df['LastDate'] = df['date']
    df.set_index('date', inplace=True)

    # Convert to period data
    period_df = df.resample(rule=period_type).last()  # Most columns use the last value during conversion

    period_df['open'] = df['open'].resample(period_type).first()
    period_df['high'] = df['high'].resample(period_type).max()
    period_df['low'] = df['low'].resample(period_type).min()
    period_df['change'] = df['change'].resample(period_type).apply(lambda x: (x + 1.0).prod() - 1.0)
    period_df['LastChange'] = df['change'].resample(period_type).last()

    # Remove periods with no trades
    period_df.dropna(subset=['code'], inplace=True)

    # Reset the index
    period_df.reset_index(inplace=True)
    period_df['date'] = period_df['LastDate']
    del period_df['LastDate']

    return period_df


# Import stock data
def import_stock_data(source_data_path, stock_code):
    df = pd.read_csv(source_data_path + "/" + stock_code + '.csv', encoding='gbk')
    df = df[['date', 'open', 'high', 'low', 'close']]
    df.sort_values(by=['date'], inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    stock_code_list = [stock_code] * len(df)
    df.insert(loc=2, column="code", value=stock_code_list)

    df['change'] = df['close'].pct_change() 
    df.reset_index(inplace=True, drop=True)
    return df


import pandas as pd
import os


print(os.listdir(Configs.source_data_path))
code_list = get_stock_code_list_in_one_dir(Configs.source_data_path)

print(len(code_list))

index = 1
for code in code_list:
    print(code)

    df = import_stock_data(Configs.source_data_path, code)

    # Check if the stock has been listed for at least a certain period, requiring at least two years of data
    # Trading days from 2022.01 to 2023.12 are approximately 490 days
    if df.shape[0] < 490:
        print(code[code.find("/")+1:code.find(".")])
        print('Stock has been listed for less than two years, strategy will not be run')
        continue

    # Select the time period
    df = df[df['date'] > pd.to_datetime('20180101')]
    df = df[df['date'] < pd.to_datetime('20200101')]

    # Convert daily data to "w" or "m" data
    df = transfer_to_period_data(df, period_type='m')  # Default resampling is by week

    # Add a new column "Decision"
    df['decision'] = None
    # === Practical method
    df = df[['date', 'code', 'open', 'high', 'low', 'close', 'change', 'decision']]
    df.reset_index(inplace=True, drop=True)

    # Obfuscate the stock name
    df['code'] = f"xxx{index}"
    code = f"xxx{index}"
    index = index + 1
    file_name = f'{code}' + '_convert.csv'
    df = df.round(4)  # Keep four significant digits
    
    
    if not os.path.exists(Configs.Current_Input_data_path):
        os.makedirs(Configs.Current_Input_data_path)

    df.to_csv(f"./{Configs.Current_Input_data_path}/{file_name}", index=False)
