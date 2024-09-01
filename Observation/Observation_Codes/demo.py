import os
import shutil

# 源文件夹
source_dir = "./csi100_gpt-3.5-baseline_monthly_2022-2023"

# 目标文件夹列表
target_dirs = [
    "csi100_gpt-3.5-baseline_monthly_2014-2015",
    "csi100_gpt-3.5-baseline_monthly_2016-2017",
    "csi100_gpt-3.5-baseline_monthly_2018-2019",
    "csi100_gpt-3.5-baseline_monthly_2020-2021",
    # "sp100_gpt-3.5-baseline_monthly_2014-2015",
    # "sp100_gpt-3.5-baseline_monthly_2016-2017",
    # "sp100_gpt-3.5-baseline_monthly_2018-2019",
    # "sp100_gpt-3.5-baseline_monthly_2020-2021"
    # "csi100_gpt-3.5-baseline_monthly_2022-2023"
]

# 遍历源文件夹中的所有文件
for file_name in os.listdir(source_dir):
    full_file_name = os.path.join(source_dir, file_name)
    if os.path.isfile(full_file_name):
        # 将文件复制到每个目标文件夹
        for target_dir in target_dirs:
            shutil.copy(full_file_name, target_dir)

print("代码文件已成功复制到所有目标文件夹中。")
