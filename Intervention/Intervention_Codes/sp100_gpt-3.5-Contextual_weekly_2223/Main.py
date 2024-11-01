# -*- coding: utf-8 -*-
"""
Main function of the timing strategy framework
"""
import pandas as pd
import Signals_Position  
import Timing_Functions
import os
import warnings
warnings.filterwarnings("ignore")
import Configs
import re


if not os.path.exists(Configs.Results_path):
    os.makedirs(Configs.Results_path)

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
code_list = get_stock_code_list_in_one_dir(Configs.Current_Input_data_path)


def extract_number(file_name):
    match = re.search(r'xxx(\d+)_convert\.csv', file_name)
    if match:
        return int(match.group(1))
    return 0

code_list = sorted(code_list, key=extract_number)
# Print the sorted file list
print(code_list)


# Resume from the breakpoint
existed_stocks = set()  # Create an empty set
for existed_stock in os.listdir(Configs.Results_path):
    existed_stock = existed_stock.replace("_decision", "").replace("_summary", "")
    existed_stock = existed_stock.split(".")[0]
    existed_stocks.add(existed_stock)


# Number of layers in the position strategy
position_div = 0.2


for stock_code in code_list[:4]:  # Select how many stocks to trade
    stock_code = stock_code.split("/")[-1].split(".")[0]
    print("stock_code", stock_code)

    # Resume from the breakpoint
    if stock_code in existed_stocks:
        continue

    # Import data
    df = pd.read_csv(Configs.Current_Input_data_path + "/" + stock_code + '.csv', encoding='gbk')

    df = df[['date', 'code', 'open', 'high', 'low', 'close', 'change', 'decision']]
    df.sort_values(by=['date'], inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    df['code'] = stock_code
    df.reset_index(inplace=True, drop=True)

    # === Generate trading signals based on GPT strategy
    df = Signals_Position.signal_and_position(df)
    print('***************************************************')

    # ===== Calculate the equity curve based on trading signals
    df = Timing_Functions.equity_curve(df, position_div, initial_money=1000000, slippage=0.01, SEC=0.21/10000, Finra=0.119/1000)
    df = df.round(4)  # Keep four significant digits

    df.to_csv(f"{Configs.Results_path}/" + stock_code + "_summary.csv", index=False)
