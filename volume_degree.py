import numpy as np
import pandas as pd
from .hffactors import HFFactors

class volume_degree(HFFactors):
    def __init__(self, start, end, period_list):
        super().__init__()
        self.start_date = start
        self.end_date = end
        self.period_list = period_list

    def cal(self):
        volume = self.get_Kindle1M('Volume')

        benchmark = np. nanmean(volume, axis = 2, keepdims=True)
        percentage = volume / benchmark

        z_score = self.z_score(np.nanmean(percentage,axis = 1, keepdims=True), axis = 2) \
                + self.z_score(np.nanstd(percentage, axis = 1, keepdims=True), axis = 2)
        
        df = pd.DataFrame(z_score.squeeze(axis = 1), index=self.gen_dates_list(), columns=self.gen_codes_list())
        for p in self.period_list:
            tmp1 = df.ewm(span=p).mean()
            tmp1.reset_index(inplace=True)
            tmp1.to_feather(self.rootpath + f'volume_degree_mean_{p}.feather')
            tmp2 = df.ewm(span=p).std()
            tmp2.reset_index(inplace=True)
            tmp2.to_feather(self.rootpath + f'volume_degree_std_{p}.feather')
        df.reset_index(inplace=True)
        df.to_feather(self.rootpath + 'volume_degree.feather')

def update(start, end):
    period = [5, 10, 20, 50]
    f = volume_degree(start, end, period)
    f.cal()

if __name__ == "__main__":
    period = [5, 10, 20, 50]
    v = volume_degree(20180101, 20240101, period)
    v.cal()