import numpy as np
import pandas as pd
from .hffactors import HFFactors

class rsi_varup(HFFactors):
    def __init__(self, start, end, period_list):
        super().__init__()
        self.start_date = start
        self.end_date = end
        self.period_list = period_list

    def cal(self):
        close = self.get_Kindle1M('Close')
        open = self.get_Kindle1M('Open')
        ret = close/open -1
        up_ret = np.where(ret>0, ret, 0)
        down_ret = np.where(ret<0, ret, 0)
        RSI = np. nanmean(up_ret, axis = 1) / (np. nanmean(up_ret,axis = 1) - np.nanmean(down_ret, axis = 1)) * 100
        varup = np.nanvar(up_ret, axis = 1)
        vardown = np.nanvar(down_ret, axis = 1)
        result = np.where(RSI > 50, RSI*varup, RSI*vardown)

        df = pd.DataFrame(result, index=self.gen_dates_list(), columns=self.gen_codes_list())
        for p in self.period_list:
            tmp1 = df.ewm(span = p).mean()
            tmp1.reset_index(inplace = True)
            tmp1.to_feather(self.rootpath + f'rsi_varup_mean_{p}.feather')
            tmp2 = df.ewm(span=p).std()
            tmp2.reset_index(inplace = True)
            tmp2.to_feather(self.rootpath + f'rsi_varup_std_{p}.feather')
        df.reset_index(inplace = True)
        df.to_feather(self.rootpath + 'rsi_varup.feather')

def update(start, end):
    period = [5, 10, 20, 50]
    f = rsi_varup(start, end, period)
    f. cal()

if __name__ == "__main__":
    period = [5,10,20,50]
    f = rsi_varup(20180101, 20230801, period)
    f.cal()