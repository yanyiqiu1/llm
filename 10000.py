import pandas as pd
import os

folder_path = r"C:\您的数据文件夹"
fixed_number = 88888888  # 一个足够大的固定数字

for filename in os.listdir(folder_path):
    if filename.endswith(".xlsx"):
        file_path = os.path.join(folder_path, filename)

        df = pd.read_excel(file_path)

        # 确保Delivery是数字类型 (如果有脏数据需要先清洗)
        # errors='coerce' 会将无法转为数字的变成NaN，请确保数据干净
        df["Delivery"] = pd.to_numeric(df["Delivery"], errors="coerce")

        # 数学加法：原有顺序绝对保留，且相同号码结果必定相同
        df["Delivery"] = df["Delivery"] + fixed_number

        df.to_excel(file_path, index=False)
print("数字加盐脱敏完成")
