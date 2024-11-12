import numpy as np
import pandas as pd
from .hffactors import HFFactors

class chase_prior(HFFactors):
    def __init__(self, start, end, period_list):
        super().__init__()
        self.start_date = start
        self.end_date = end
        self.period_list = period_list

    def cal(self):
        volume = self.get_Kindle1M('Volume')
        volume_rank = volume.argsort(axis = 1).argsort(axis = 1)
        volume_desc_rank = volume.shape[1] -1 - volume_rank
        volume_desc_rank = np.where(volume_desc_rank < 10, 1, 0)

        prior = np.where(volume_desc_rank == 1, volume, 0)
        chase = np.zeros_like(prior)
        window_size = 5
        for i in range(chase.shape[1] - window_size + 1):
            chase[:, i, :] = np.sum(volume[:, i+1:i + window_size+1, :], axis = 1)
    
        ratios = np.where(prior > 0, chase/prior, 0)
        avg_ratios = np.mean(ratios, axis = 1)

        df = pd.DataFrame(avg_ratios, index=self.gen_dates_list(), columns=self.gen_codes_list())
        for p in self.period_list:
            tmp1 = df.ewm(span = p).mean()
            tmp1.reset_index(inplace = True)
            tmp1.to_feather(self.rootpath + f'chase_prior_mean_{p}.feather')
            tmp2 = df.ewm(span=p).std()
            tmp2.reset_index(inplace = True)
            tmp2.to_feather(self.rootpath + f'chase_prior_std_{p}.feather')
        df.reset_index(inplace = True)
        df.to_feather(self.rootpath + 'chase_prior.feather')

def update(start, end):
    period = [5, 10, 20, 50]
    f = chase_prior(start, end, period)
    f.cal()

if __name__ == '__main__':
    period = [5,10,20,50]
    f = chase_prior(20180101, 20230928, period)
    f.cal()