import numpy as np
import pandas as pd
from .hffactors import HFFactors

class foc(HFFactors):
    def __init__(self, start, end, period_list):
        super().__init__()
        self.start_date = start
        self.end_date = end
        self.period_list = period_list

    def cal(self):
        open = self.get_Kindle1M('Open')
        close = self.get_Kindle1M('Close')
        ret = close / open -1
        ret = ret[:, 10:230, :]

        volume = self.get_Kindle1M('Volume')
        volume = volume / np.nanmean(volume, axis = 1, keepdims=True)
        volume = volume[:, 10:230, :]

        ret_mean = np.nanmean(ret, axis = 1, keepdims=True)
        vol_mean = np.nanmean(volume, axis = 1, keepdims=True)
        ret_diff = ret - ret_mean
        vol_diff = volume - vol_mean
        cov = np.nansum(ret_diff*vol_diff, axis=1)
        ret_var = np.nansum(ret_diff ** 2, axis=1)
        vol_var = np.nansum(vol_diff ** 2, axis=1)
        corr = cov / np.sqrt(ret_var * vol_var)
        df = pd.DataFrame(corr, index=self.gen_dates_list(), columns=self.gen_codes_list())
        for p in self.period_list:
            tmp1 = df.ewm(span = p).mean()
            tmp1.reset_index(inplace = True)
            tmp1.to_feather(self.rootpath + f'foc_mean_{p}.feather')
            tmp2 = df.ewm(span=p).std()
            tmp2.reset_index(inplace = True)
            tmp2.to_feather(self.rootpath + f'foc_std_{p}.feather')
        df.reset_index(inplace = True)
        df.to_feather(self.rootpath + 'foc.feather')

def update(start, end):
    period = [5, 10, 20, 50]
    f = foc(start, end, period)
    f. cal()

if __name__ == '__main__':
    period = [5,10,20,50]
    f = foc(20180101, 20230801, period)
    f.cal()