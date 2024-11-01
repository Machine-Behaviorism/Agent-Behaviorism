from openai import OpenAI
import os

API_KEY = "sk-xxxx"
OPENAI_ORGANIZATION = "org-TfIH2DbMdVVsDTC4wawLqvcv"

client = OpenAI(api_key=API_KEY,organization=OPENAI_ORGANIZATION)


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


def completion_create(model_id,sysrem_prompt,user_content):
  completion = client.chat.completions.create(
  model = model_id,
  messages=[
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_content

  print(completion.choices[0].message)

import pdb
pdb.set_trace()