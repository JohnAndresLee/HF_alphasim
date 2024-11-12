import numpy as np
import pandas as pd
from .hffactors import HFFactors

class frightened_degree(HFFactors):
    def __init__(self, start, end, period_list):
        super().__init__()
        self.start_date = start
        self.end_date = end
        self.period_list = period_list

    def cal(self):
        open = self.get_Kindle1M('Open')
        close = self.get_Kindle1M('Close')
        ret = close/open -1

        benchmark = np.nanmean(ret,axis = 2, keepdims=True)
        bias = np.abs(ret - benchmark)
        frightened = bias / (np.abs(ret) + np.abs(benchmark) + 0.01)
        score = frightened * ret
        z_score = self.z_score(np.nanmean(score,axis = 1, keepdims=True), axis = 2) \
                    + self.z_score(np.nanstd(score,axis = 1, keepdims=True), axis = 2)
        
        df = pd.DataFrame(z_score.squeeze(axis = 1), index=self.gen_dates_list(), columns=self.gen_codes_list())
        for p in self.period_list:
            tmp1 = df.ewm(span = p).mean()
            tmp1.reset_index(inplace = True)
            tmp1.to_feather(self.rootpath + f'frightened_degree_mean_{p}.feather')
            tmp2 = df.ewm(span=p).std()
            tmp2.reset_index(inplace = True)
            tmp2.to_feather(self.rootpath + f'frightened_degree_std_{p}.feather')
        df. reset_index(inplace = True)
        df. to_feather(self.rootpath + 'frightened_degree.feather')

def update(start, end):
    period = [5, 10, 20, 50]
    f = frightened_degree(start, end, period)
    f.cal()

if __name__ == "__main__":
    period = [5,10,20,50]
    f = frightened_degree(20180101, 20230801, period)
    f.cal()