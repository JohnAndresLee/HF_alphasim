import os
import time
import glob
import pandas as pd
from multiprocessing import Pool 
import warnings
warnings. filterwarnings('ignore')

def update_file(pq_path, l, endday):

    c = os.path.join(pq_path, l)

    if os.path.isfile(c) and c.endswith('.py') and c.find("update_all") == -1 and c.find("hffactors") == -1 \
            and c.find("function_tools") == -1 and c.find("__init__") == -1 :
        
        feather_files = glob.glob(os.path.join('/mnt/disk2/common/onlinev3/factors/HFFactors_alphasim', f"{l[:-3]}*.feather"))
        for feather_file_path in feather_files:
            try:
                df = pd.read_feather(feather_file_path)
            except Exception as e:
                continue

            latest_date = df['index'].max()
            if latest_date < endday:
                print(f'{l[:-3]} is insufficient')
                print(f"updating {c[:-3]}")
                exec (f"from {c[:-3].replace('/', '.')} import update as {l[:-3]}_update") 
                exec (f" {l[:-3]}_update({20180101}, {endday})")
                print(f"{l[:-3]} has updated")
                break
            # else:
            #     return
            # print(f"updating {c[:-3]}")
            # exec (f"from {c[:-3].replace('/', '.')} import update as {l[:-3]}_update") 
            # exec (f" {l[:-3]}_update({20180101}, {endday})")

def update_HF_alphasim(hf_path, endday):
    # hf_path = 'Factors/HF_alphasim'
    lst = os.listdir(hf_path)

    time1 = time.time()
    # with Pool(processes=5) as p:
    #     p.map(update_file, [(hf_path, l, endday) for l in lst])
    for l in lst:
        update_file(hf_path, l, endday)
    print('total runtime', time.time()-time1)

if __name__ == "__main__":
    update_HF_alphasim()
        