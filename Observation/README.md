
```markdown
# Observation Phase Documentation

## Overview

This document provides instructions for running the `Observation` phase, corresponding to the first stage mentioned in the related paper. Follow the steps below to either view the disposition effect (DE) results or reproduce the `Observation` experiments.

## 1. Viewing Disposition Effect (DE) Results

To view the statistical results of the Disposition Effect (DE), simply run the `Oberservation_disposition_effect_calculation.ipynb` notebook. The output will be similar to the table below:

```plaintext
\begin{table}[h]
\centering
\caption{The observed results of agent behavior on disposition effect.}
\label{observation}
\resizebox{0.45\textwidth}{!}{%
\begin{tabular}{|c|c|c|c|c|c|c|c|}
\hline
Country & Years & Per. & C-DE & t-Sts & SE & p-Value & Return \\
\hline
USA  & 14-15 & 11.63\% & 0.324 & 8.428 & 0.038 & $<$0.001 & 0.03\% \\
USA  & 16-17 & 12.79\% & 0.445 & 12.549 & 0.035 & $<$0.001 & 0.44\% \\
USA  & 18-19 & 10.47\% & 0.465 & 5.434 & 0.086 & $<$0.001 & 0.18\% \\
USA  & 20-21 & 20.93\% & 0.431 & 9.071 & 0.048 & $<$0.001 & 2.00\% \\
USA  & 22-23 & 9.30\% & 0.493 & 6.717 & 0.073 & $<$0.001 & 0.16\% \\
% USA  & 22-23 & weekly & 35.35\% & 0.164 & 7.644 & 0.021 & $<$0.001 & 2.03\% \\
\hline
China  & 14-15 & 32.47\% & 0.344 & 10.082 & 0.034 & $<$0.001 & 10.19\% \\
China  & 16-17 & 33.77\% & 0.346 & 9.201 & 0.038 & $<$0.001 & 7.85\% \\
China  & 18-19 & 27.27\% & 0.270 & 9.133 & 0.030 & $<$0.001 & 9.66\% \\
China  & 20-21 & 49.35\% & 0.353 & 10.712 & 0.033 & $<$0.001 & 2.76\% \\
% \hline
China  & 22-23 & 37.66\% & 0.414 & 11.832 & 0.035 & $<$0.001 & 1.64\% \\
% China  & 22-23 & weekly & 51.55\% & 0.205 & 6.804 & 0.030 & $<$0.001 & 1.81\% \\
\hline
\end{tabular}
}
\end{table}
```

## 2. Reproducing the Observation Experiments

To reproduce the `Observation` experiments, follow the steps below:

### 2.1 Set the OpenAI API Key and Paths

Make sure to configure the following API key and paths:

```python
# coding=utf-8
import os

OPENAI_ORGANIZATION = "org-xxxxv"
API_KEY = "sk-xxxxx"
COMPLETION_MODEL = "gpt-3.5-turbo-16k"
# COMPLETION_MODEL = "gpt-4" 
# COMPLETION_MODEL = "gpt-4-1106-preview"
# COMPLETION_MODEL = "gpt-4-0613"
# COMPLETION_MODEL = "gpt-3.5-turbo"
# COMPLETION_MODEL = "gpt-3.5-turbo-1106"
# COMPLETION_MODEL = "gpt-3.5-turbo-0613"

# Root directory of Dataset
source_data_path = "/root/PNAS_Github/Dataset/sp_100_stocks"
Current_Input_data_path = "./sp100_Input_Dataset"

root_path = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir, os.pardir))
Results_path = os.path.abspath(os.path.join(root_path, 'Observation/Observation_Results', "sp100_gpt-3.5-baseline_monthly_2022-2023"))
# print("Results_path", Results_path)
```

### 2.2 Generate the Data

Run the following script to generate the necessary data:

```bash
python Pre_Data_convert.py
```

### 2.3 Execute the Main Script

Finally, run the main script to perform the experiments:

```bash
python Main.py
```

## Conclusion

Following these steps will allow you to either view the statistical results related to the disposition effect in the `Observation` phase. Make sure to set up the environment correctly and use the provided API keys and paths for a successful execution.
```
