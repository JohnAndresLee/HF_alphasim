import numpy as np
import pandas as pd
from .hffactors import HFFactors

class motonic_increase_ratio(HFFactors):
    def __init__(self, start, end, period_list):
        super().__init__()
        self.start_date = start
        self.end_date = end
        self.period_list = period_list

    def cal(self):
        price= self.get_Kindle1M('Open') #axis = 1 is price
        slopes = np.diff(price, axis = 1)
        increasing = slopes > 0
        num_increasing = np.nansum(increasing, axis = 1)
        ratio = num_increasing / (price.shape[1] -1)

        df = pd. DataFrame(ratio, index=self.gen_dates_list(), columns=self.gen_codes_list())
        for p in self.period_list:
            tmp1 = df.ewm(span=p).mean()
            tmp1.reset_index(inplace=True)
            tmp1.to_feather(self.rootpath + f'motonic_increase_ratio_mean_{p}.feather')
            tmp2 = df.ewm(span=p).std()
            tmp2.reset_index(inplace=True)
            tmp2.to_feather(self.rootpath + f'motonic_increase_ratio_std_{p}.feather')
        df.reset_index(inplace=True)
        df.to_feather(self.rootpath + 'motonic_increase_ratio.feather')

def update(start, end):
    period = [5, 10, 20, 50]
    f = motonic_increase_ratio(start, end, period)
    f.cal()

if __name__=="__main__":
    period = [5, 10, 20, 50]
    m = motonic_increase_ratio(20180101, 20231009, period)
    m.cal()