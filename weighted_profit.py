import numpy as np
import pandas as pd
from .hffactors import HFFactors

class weighted_profit(HFFactors):
    def __init__(self, start, end, period_list):
        super().__init__()
        self.start_date = start
        self.end_date = end
        self.period_list = period_list

    def cal(self):
        open = self.get_Kindle1M('Open')
        close = self.get_Kindle1M('Close')
        volume = self.get_Kindle1M('Volume')
        ret = close/open -1

        benchmark = np.nanmean (ret, axis = 2, keepdims=True)
        bias = ret - benchmark
        whether_profit = np.where(bias > 0.0001, 1, 0)
        volume_prop = volume / np.nansum(volume, axis = 1, keepdims=True)
        weighted_profit = whether_profit * volume_prop
        j= np.arange(whether_profit.shape[1])
        weights = (1/2) ** (240 - j/30)
        scale_weighted_profit = weighted_profit * weights[:, np.newaxis] * (10**70)
        sum_whether_profit = np.nansum(whether_profit, axis = 1) + 1e-8
        result = np.where(sum_whether_profit > 1e-8,
                        np.nansum(scale_weighted_profit, axis = 1) / sum_whether_profit, 0) ###??
        
        df = pd.DataFrame(result, index=self.gen_dates_list(), columns=self.gen_codes_list())
        for p in self.period_list:
            tmp1 = df.ewm(span = p).mean()
            tmp1.reset_index(inplace = True)
            tmp1.to_feather(self.rootpath + f'weighted_profit_mean_{p}.feather')
            tmp2 = df.ewm(span = p).std()
            tmp2.reset_index(inplace = True)
            tmp2.to_feather(self.rootpath + f'weighted_profit_std_{p}.feather')
        df.reset_index(inplace = True)
        df.to_feather(self.rootpath + 'weighted_profit.feather')

def update(start, end):
    period = [5, 10, 20, 50]
    f = weighted_profit(start, end, period)
    f.cal()

if __name__ == "__main__":
    period = [5,10,20,50]
    f = weighted_profit(20180101, 20240101, period)
    f.cal()