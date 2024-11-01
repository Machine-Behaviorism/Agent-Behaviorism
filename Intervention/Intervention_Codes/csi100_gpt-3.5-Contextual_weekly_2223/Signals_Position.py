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
import pandas as pd


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



system_prompt_dic = {"role": "system", "content": system_prompt}


# Injecting some RAG-retrieved industry knowledge into System (RAG's static part, obtained by GPT and manually selected)
# system_query = """
# Here is some general external information for the task. Please continue to adhere to the previous instructions without allowing this information to influence the format of your decision-making output. The following information serves as background knowledge relevant to this task. It has been obtained through extensive searches, manual selection, and summarization using search tools. When making decisions, it is important to carefully consider and study this information. It can serve as a solid foundation for your basic knowledge. The knowledge provided includes:\

# The stock market operates on the basic premise that stocks represent partial ownership in companies. Stock prices are primarily determined by the interplay of supply and demand, influenced by the activities of buyers and sellers. Key factors driving price movements include company performance, growth outlook, and broader economic indicators. Additionally, market sentiment, reflecting investors' attitudes towards stocks or the market, plays a crucial role, along with external factors such as central bank policies, economic updates, and geopolitical events.\

# Analyzing stock performance involves utilizing essential dataset columns like 'open,' 'high,' 'low,' 'close,' and 'change.' These columns provide insights into daily and intraday volatility, price range within a trading period, and momentum. Such data is instrumental for technical analysis, aiding investors in identifying trends and predicting future movements through various charting techniques.\

# Effective trading decisions require a holistic approach, considering various factors such as investment objectives, risk tolerance, market evaluation, portfolio composition, emotional management, financial planning, long-term outlook, budgeting and timing, and tax considerations. Each of these aspects contributes to a well-rounded trading strategy aimed at achieving investment goals while managing risk and maximizing returns.\

# Transaction costs, including both explicit fees like broker commissions and taxes and implicit costs such as bid-ask spreads and market impact, have a direct impact on investment returns. While technological advancements and competitive brokerage offerings have reduced these costs, they remain a significant consideration for investors, particularly for active traders and smaller accounts. Strategies to mitigate transaction costs include utilizing efficient order types and carefully planning trade execution.\

# Also, ensure that the response is presented exclusively in JSON format, adhering strictly to the following structure: {'decision': 'buy'/'sell'/'keep'}. Any deviation from this format is not acceptable.

# """


system_query = """
Here is some general external information for the task. Please continue to adhere to the previous instructions without allowing this information to influence the format of your decision-making output. The following information serves as background knowledge relevant to this task. It has been obtained through extensive searches, manual selection, and summarization using search tools. When making decisions, it is important to carefully consider and study this information. It can serve as a solid foundation for your basic knowledge. The knowledge provided includes:\

The stock market operates on the principle of stocks representing partial ownership in companies, with prices driven by supply, demand, and various factors like company performance and economic indicators. Analyzing stock performance involves key dataset columns like 'open,' 'high,' 'low,' 'close,' and 'change,' aiding in trend identification and future predictions. Effective trading decisions consider investment goals, risk tolerance, portfolio composition, and financial planning. Transaction costs, including explicit fees and implicit costs, impact returns and should be managed through efficient order types and trade planning.\

Also, ensure that the response is presented exclusively in JSON format, adhering strictly to the following structure: {'decision': 'buy'/'sell'/'keep'}. Any deviation from this format is not acceptable.

"""

system_query_dic = {"role": "system", "content": system_query}


# GPT strategy
def signal_and_position(input_data, pos_div=0.2):

    # Add a new column "hold_num"
    input_data['hold_num'] = None
    input_data.at[10, 'hold_num'] = 0  # Number of shares held
    
    # Add a new column "cash"
    input_data['cash'] = None
    input_data.at[10, 'cash'] = 1000000  # Cash balance

    # Add a new column "equity"
    input_data['equity'] = None
    input_data.at[10, 'equity'] = 1000000

    # Extract subsequent data row by row
    for i in range(11, len(input_data)):
    
        row = input_data.iloc[0:i,:].copy()
    
        buy_price = -1
        counter = equity_curve(row, pos_div)
    
        for k in range(11,i):
            # Update purchase price
            if counter.at[k-1,'decision'] == "buy":
                # Prevent division by zero, i.e., even if the strategy is "buy," ensure affordability
                if counter.at[k,'hold_num'] != 0:
                    buy_price = (buy_price * counter.at[k-1,'hold_num'] + counter.at[k,'open'] * (counter.at[k,'hold_num'] - counter.at[k-1,'hold_num'])) / counter.at[k,'hold_num']


        message_our = []

        message_our.append(system_prompt_dic)
        message_our.append(system_query_dic)


        # Dynamic analysis of current historical information (dynamic part of RAG)
        if i >= 20:
            history = row[['date', 'code', 'open', 'high', 'low', 'close', 'change']][-10:]
            history = f"{history}"
            # history = row[-10:]
            # print("Last 10 history", history)


            user_query = """

            Based on the historical trading data provided, please summarize the stock's recent characteristics and give your potential recommendations in one sentence, no more than 50 words.
            """

            message_user_query = [

                {"role": "system", "content": user_query}
            ]

            user_query_dic = {"role": "user", "content": history}
            message_user_query.append(user_query_dic)
            # print("message_user_query",message_user_query)


            # Retry up to 5 times
            attempts = 0
            success = False
            while attempts < 5 and not success:
                try:
                    
                    user_query_output = ChatBot(message_user_query, Configs).content
                    success = True
                    # print("user_query_output", user_query_output)
                except:
                    user_query_output = None
                    print('no response from user_query_output of gpt')
                    attempts += 1
                    if attempts == 3:
                        break
                    
            if user_query_output :
                user_query_output_prompt = f""""
                Here is some external analysis specific to the latest 10 historical trading records for this task. This analysis provides insights into the current dynamics of the stock. The analysis is as follows: "{user_query_output}"
                """
                user_query_output_prompt_dic = {"role": "user", "content": user_query_output_prompt}
            else:
                user_query_output_prompt_dic  = None

        else:
            user_query_output_prompt_dic = None

        # print(user_prompt)
        user_prompt = f"{row}"
        user_prompt_dic = {"role": "user", "content": user_prompt}
        message_our.append(user_prompt_dic)
        if user_query_output_prompt_dic:
            print(user_query_output)
            message_our.append(user_query_output_prompt_dic)


        # Retry up to 5 times
        attempts = 0
        success = False
        while attempts < 5 and not success:
            try:
                output = ChatBot(message_our, Configs).content
                print("Origin output", output)
                success = True

            except:
                print('no response from gpt')
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
