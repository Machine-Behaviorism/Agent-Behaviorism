# -*- coding: utf-8 -*-

def equity_curve(df, pos_div=0.2, initial_money=1000000, slippage=0.01, SEC=0.21/10000, Finra=0.119/1000):

    df.at[10, 'hold_num'] = 0  
    df.at[10, 'stock_value'] = 0 
    df.at[10, 'actual_pos'] = 0 
    df.at[10, 'cash'] = initial_money 
    df.at[10, 'equity'] = initial_money 

    for i in range(11, df.shape[0]):

        hold_num = df.at[i - 1, 'hold_num']

        if abs((df.at[i, 'close'] / df.at[i - 1, 'close'] - 1) - df.at[i, 'change']) > 0.001:
            stock_value = df.at[i - 1, 'stock_value']
            last_price = df.at[i, 'close'] / (df.at[i, 'change'] + 1)
            hold_num = stock_value / last_price
            hold_num = int(hold_num)

        if df.at[i-1, 'decision'] == "buy":

            # Quantify the cash portion for purchasing
            buy_part = df.at[i-1, 'cash'] * pos_div

            theory_num = buy_part / (df.at[i, 'open'] + slippage)
            theory_num = int(theory_num) 
            buy_cash = theory_num * (df.at[i, 'open'] + slippage)

            df.at[i, 'commission'] = 0 
            df.at[i, 'hold_num'] = hold_num + theory_num
            df.at[i, 'cash'] = df.at[i - 1, 'cash'] - buy_cash

        elif df.at[i-1, 'decision'] == "sell":

            # Quantify the portion of shares to be sold
            sell_num = int(hold_num * pos_div)
            sell_cash = sell_num * (df.at[i, 'open'] - slippage)

            commission = sell_num * Finra + sell_cash * SEC
            df.at[i, 'commission'] = commission

            df.at[i, 'hold_num'] = hold_num - sell_num
            df.at[i, 'cash'] = df.at[i - 1, 'cash'] + sell_cash - commission

        else:

            df.at[i, 'hold_num'] = hold_num
            df.at[i, 'cash'] = df.at[i - 1, 'cash']

        df.at[i, 'stock_value'] = df.at[i, 'hold_num'] * df.at[i, 'close']
        df.at[i, 'equity'] = df.at[i, 'cash'] + df.at[i, 'stock_value']
        df.at[i, 'actual_pos'] = df.at[i, 'stock_value'] / df.at[i, 'equity']

    return df
