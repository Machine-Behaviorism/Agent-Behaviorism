import pandas as pd
import json
import os

def generate_decision(stock_history):

    decisions  = []
    for i in range(1, len(stock_history)):
        change = stock_history.loc[i, 'change']
        # if change > 0.02:
        if change > 0.01:
            decisions.append('buy')
        elif change < -0.01:
            decisions.append('sell')
        else:
            decisions.append('keep')

    stock_history['decision'] = decisions + [' '] 


    return stock_history[:]


def data_sort_by_date(file_path, save_path, begin, end, limit = -1):
    i = 0
    for file in os.listdir(file_path):
        if i == limit : break
        else:
            df = pd.read_csv(file_path+"/"+file)

            df = df[pd.to_datetime(df['date']) > pd.to_datetime(begin)]
            df = df[pd.to_datetime(df['date']) < pd.to_datetime(end)]
            df = df.reset_index()
            df =  generate_decision(df)
            df.to_csv(save_path+"/"+file, index=False)
            i += 1

def message_generate(file_path, save_path, system_prompt, key_list, batch, num):
    count = 0
    for file in os.listdir(file_path):
        if count == num :break
        else: 
            print(count)
            count += 1

        df = pd.read_csv(file_path+"/"+file, encoding='gbk')

        df = df[key_list]

        df.sort_values(by=['date'], inplace=True)

        df['date'] = pd.to_datetime(df['date'])

        df.reset_index(inplace=True, drop=True)

        josnl_save_path = save_path +"/"+ file +".jsonl"

        dic = {'keep':0,'buy':0,'sell':0}

        print(f"jsonl file is saves as {josnl_save_path}")
        with open(josnl_save_path, 'w') as f:
            for i in range(batch,len(df)-batch):
                row = df.iloc[i-batch:i,:-1].copy()
                decision = df['decision'][i]
                dic[decision] =  dic[decision] +1
                if decision != 'keep' or  data_balance(dic):
                    message_user = {"role": "user", "content": f"{row}"}
                    message_assissant = {"role": "assistant", "content": f"decision:{decision}"}
                    message_sys = {"role": "system", "content": system_prompt}
                    j_message = {"messages" : [message_sys,message_user,message_assissant]}
                    json.dump(j_message, f)
                    f.write("\n")
                else:
                    dic ['keep'] = dic ['keep'] - 1

# merge all the jsonl in the datapath
def jsonl_files_merge(data_path, merge_path):
    with open (data_path+"/"+merge_path+".jsonl",'w',encoding='utf-8') as f2:
        for file in os.listdir(data_path):
            with open(data_path+"/"+file , 'r', encoding='utf-8') as f:
                f2.write(f.read())
                f.close()

def data_balance(dic):
    keep = dic['keep']
    sell = dic['sell']
    buy  = dic['buy']
    if (keep < min(buy,sell)/10 or keep < 150) and keep < 600:
        return True 
    else: return False

def data_ana(data_path):
    dic = {'keep':0,'buy':0,'sell':0}
    with open(data_path) as f:
        dataset=[(json.loads(line)) for line in f]
        for ex in dataset:
            content = ex["messages"][-1]['content'].replace("decision:","")
            dic[content] =  dic[content] +1
    return dic

