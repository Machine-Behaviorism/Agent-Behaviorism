# coding=utf-8
import os

OPENAI_ORGANIZATION = "org-xxx"
API_KEY = "sk-xxxx"
COMPLETION_MODEL =  "gpt-3.5-turbo-16k"
# COMPLETION_MODEL = "gpt-4" 
# COMPLETION_MODEL ="gpt-4-1106-preview"
# COMPLETION_MODEL ="gpt-4-0613"
# COMPLETION_MODEL ="gpt-3.5-turbo"
# COMPLETION_MODEL ="gpt-3.5-turbo-1106"
# COMPLETION_MODEL = "gpt-3.5-turbo-0613"

# Root directory of Dataset
source_data_path ="/root/PNAS_Github/Dataset/csi_100_stocks"
Current_Input_data_path = "./csi100_Input_Dataset"

root_path = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir,os.pardir,os.pardir))
Results_path = os.path.abspath(os.path.join(root_path, 'Observation/Observation_Results', "xxx"))
# print("Results_path", Results_path)

