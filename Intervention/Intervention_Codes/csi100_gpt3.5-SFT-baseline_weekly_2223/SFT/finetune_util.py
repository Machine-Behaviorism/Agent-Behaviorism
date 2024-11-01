from openai import OpenAI
import os

API_KEY = "sk-XXX"
OPENAI_ORGANIZATION = "org-xxx"

client = OpenAI(api_key=API_KEY,organization=OPENAI_ORGANIZATION)

def file_upload(filepath):
    file = client.files.create(
        file=open(filepath, "rb"),
        purpose="fine-tune"
    )

    file_id = file.id

    print(f"success, the file_id is {file_id}")

    return file_id

def fine_tuning_create(file_id,model_name,epochs):
    job = client.fine_tuning.jobs.create(
      training_file= file_id,
      model = model_name,
        hyperparameters={
            "n_epochs":epochs
        }
    )

    job_id = job.id

    print(f"success, the job_id is {file_id}")

    return job_id

def job_retrieve(job_id):
    print(client.fine_tuning.jobs.retrieve())


import pdb
pdb.set_trace()



