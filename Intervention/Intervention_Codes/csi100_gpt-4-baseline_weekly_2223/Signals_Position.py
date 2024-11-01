# -*- coding: utf-8 -*-

import openai
from openai import OpenAI
import os
import pandas as pd
import numpy as np
import timeout_decorator
import time
from Timing_Functions import equity_curve
import os
import Configs
import random
random.seed(990101)


def ChatBot(message_our, Configs, n=1, max_tokens=1000):
    
    client = OpenAI(api_key=Configs.API_KEY, organization=Configs.OPENAI_ORGANIZATION)

    completion = client.chat.completions.create(
        model=Configs.COMPLETION_MODEL,
        max_tokens=max_tokens,
        n=n,
        temperature=0,
        messages=message_our
    )

    return completion.choices[0].message



system_prompt = """

As an ordinary shareholder, you start with an initial equity of $1,000,000. Your task is to make trading decisions based on the provided historical dataset to maximize your equity. \

The dataset includes the following columns: ["date", "code", "open", "high", "low", "close", "change", "decision", "hold_num", "cash", "equity"]. \
The "date" column records the stock trading date. The "code" column represents the code of the current stock. \
The K-line of the stock consists of "open" (open price), "high" (highest price), "low" (lowest price) and \
"close" (close price). The "change" column records the change in stock's close price. \
The "decision" column articulates the actions you undertake, thoughtfully considering both the K-line data of the current period and the comprehensive historical data from past periods. \
The "hold_num" column records the number of shares you hold, and the "cash" column records your cash on hand in this period.\
The "equity" column is calculated by summing your stock value and cash on hand, which is also your maximizing target. \
Besides, the stock value is calculated by multiplying the "hold_num" column and the "close" column.\

You have to select your decision between ['buy', 'sell', 'keep'].\
If you choose 'buy', you will use 20% of your cash to buy the stock. \
If you choose 'sell', on the contrary, you will sell 20% of the shares you hold and receive the corresponding cash. \
If you choose 'keep', you conduct neither buying nor selling, not making any new trades.

Please note that you cannot perform any operations during the first 10 periods. These 10 periods are used to show you the current \
trend of the stock.

Please be aware that purchasing stocks incurs a 0.025% commission fee, and when selling stocks, a 0.025% commission fee and an additional 0.1% tax apply.\
Additionally, stocks are only purchasable in multiples of 100 shares.\
Ensure that the response is presented exclusively in JSON format, adhering strictly to the following structure: {'decision': 'buy'/'sell'/'keep'}. Any deviation from this format is not acceptable.

"""


# GPT Timing Trading strategy
def signal_and_position(input_data, pos_div=0.2):

    # Add a new column "hold_num"
    input_data['hold_num'] = None
    input_data.at[10, 'hold_num'] = 0  # Number of shares held
    
    # Add a new column "cash"
    input_data['cash'] = None
    input_data.at[10, 'cash'] = 1000000  # Cash held

    # Add a new column "equity"
    input_data['equity'] = None
    input_data.at[10, 'equity'] = 1000000

    # Iterate over subsequent data rows
    for i in range(11, len(input_data)):
    
        row = input_data.iloc[0:i, :].copy()
        buy_price = -1
        counter = equity_curve(row, pos_div)

        for k in range(11, i):
            # Update purchase price
            if counter.at[k-1, 'decision'] == "buy":
                # Prevent division by zero, i.e., even if the strategy is buy, but unable to afford
                if counter.at[k, 'hold_num'] != 0:
                    buy_price = (buy_price * counter.at[k-1, 'hold_num'] + counter.at[k, 'open'] * (counter.at[k, 'hold_num'] - counter.at[k-1, 'hold_num'])) / counter.at[k, 'hold_num']
        
        message_our = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Here you handle each row of data, for example, print or perform other operations
        user_prompt = f"{row}"
        user_prompt_dic = {"role": "user", "content": user_prompt}
        message_our.append(user_prompt_dic)

        # Retry up to 5 times
        attempts = 0
        success = False
        while attempts < 5 and not success:
            try:
                output = ChatBot(message_our, Configs).content
                print("Origin output", output)
                success = True
            except:
                print('No response from GPT')
                time.sleep(5)
                attempts += 1
                if attempts == 3:
                    break

        try:
            output_decision = eval(output)['decision']
            input_data.at[i-1, 'decision'] = output_decision
        except:
            def extract_decision(text):
                # Attempt to find a decision in the format 'decision': 'xxxx'
                match = re.search(r"'decision': '(\w+)'", text)
                if match:
                    return match.group(1)
                # If not found, try directly matching 'buy', 'sell', or 'keep'
                match = re.search(r"\b(buy|sell|keep)\b", text)
                if match:
                    return match.group(1)
                # If still not found, return 'keep'
                return 'keep'
            output_decision = extract_decision(output)
            input_data.at[i-1, 'decision'] = output_decision

        # Get position, then get hold number and equity
        tem = input_data.iloc[:i+1].copy()
        current_curve = equity_curve(tem, pos_div)

        input_data.at[i, 'equity'] = current_curve.at[i, 'equity']
        input_data.at[i, 'hold_num'] = current_curve.at[i, 'hold_num']
        input_data.at[i, 'cash'] = current_curve.at[i, 'cash']

    return input_data
