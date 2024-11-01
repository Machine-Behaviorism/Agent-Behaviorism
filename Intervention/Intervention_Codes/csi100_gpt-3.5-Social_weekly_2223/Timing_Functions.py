# -*- coding: utf-8 -*-

def equity_curve(df, pos_div=0.2, initial_money=1000000, slippage=0.01, c_rate=2.5/10000, t_rate=1.0/1000):

    df.at[10, 'hold_num'] = 0 
    df.at[10, 'stock_value'] = 0 
    df.at[10, 'actual_pos'] = 0 
    df.at[10, 'cash'] = initial_money 
    df.at[10, 'equity'] = initial_money 

    for i in range(11, df.shape[0]):

        hold_num = df.at[i - 1, 'hold_num']

        # Calculate adjusted price
        if abs((df.at[i, 'close'] / df.at[i - 1, 'close'] - 1) - df.at[i, 'change']) > 0.001:
            stock_value = df.at[i - 1, 'stock_value']
            last_price = df.at[i, 'close'] / (df.at[i, 'change'] + 1)
            hold_num = stock_value / last_price
            hold_num = int(hold_num)

        if df.at[i-1, 'decision'] == "buy":
            
            # Quantify the cash portion for purchase
            buy_part = df.at[i-1,'cash'] * pos_div

            theory_num = buy_part / ((df.at[i, 'open'] + slippage) * (1 + c_rate))
            theory_num = int(theory_num)  

            buy_num = theory_num 
            buy_num = int(buy_num / 100) * 100
            buy_cash = buy_num * (df.at[i, 'open'] + slippage)

            commission = round(buy_cash*c_rate, 2)
            if commission < 5 and commission != 0:
                commission = 5

            df.at[i, 'commission'] = commission
            df.at[i, 'hold_num'] = hold_num + buy_num
            df.at[i, 'cash'] = df.at[i - 1, 'cash'] - buy_cash - commission

        elif df.at[i-1, 'decision'] == "sell":

            # Quantify the portion of shares for sale
            sell_num = int(hold_num * pos_div)
            sell_cash = sell_num * (df.at[i, 'open'] - slippage)
            
            commission = 0
            tax = 0
            if sell_cash != 0:
                commission = round(max(sell_cash * c_rate, 5), 2)
                df.at[i, 'commission'] = commission

                tax = round(sell_cash * t_rate, 2)
                df.at[i, 'tax'] = tax

            df.at[i, 'hold_num'] = hold_num - sell_num
            df.at[i, 'cash'] = df.at[i - 1, 'cash'] + sell_cash - commission - tax 

        else:
            
            df.at[i, 'hold_num'] = hold_num  
            df.at[i, 'cash'] = df.at[i - 1, 'cash'] 
        
 
        # print(hold_num, df.at[i, 'hold_num'])
        df.at[i, 'stock_value'] = df.at[i, 'hold_num'] * df.at[i, 'close']      
        df.at[i, 'equity'] = df.at[i, 'cash'] + df.at[i, 'stock_value']      
        df.at[i, 'actual_pos'] = df.at[i, 'stock_value'] / df.at[i, 'equity']  

    return df
