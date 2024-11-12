import numpy as np
import pandas as pd
from .hffactors import HFFactors

class competition_trend(HFFactors):
    def __init__(self, start, end, period_list):
        super().__init__()
        self.start_date = start
        self.end_date = end
        self.period_list = period_list

    def cal(self) :
        open = self.get_Kindle1M('Open')
        close = self.get_Kindle1M('Close')
        ret = close / open -1

        high = self.get_Kindle1M('High')
        low = self.get_Kindle1M('Low')
        spread = high - low

        dg= np.where(np.abs(ret) < 0.004, 1, 0)
        tail = (spread - np.abs(close - open))/spread

        volume = self.get_Kindle1M('Volume')
        volume = volume / np. nanmean(volume, axis = 1, keepdims=True)

        competition = tail * volume * dg
        z_score = self.z_score(np.nanmean(competition, axis=1, keepdims=True), axis=2) \
                    + self.z_score(np.nanstd(competition, axis=1, keepdims=True), axis=2)
        
        df = pd.DataFrame(z_score.squeeze(axis = 1), index=self.gen_dates_list, columns=self.gen_codes_list)
        for p in self.period_list:
            tmp1 = df.ewm(span = p).mean()
            tmp1.reset_index(inplace = True)
            tmp1.to_feather(self.rootpath + f'competition_trend_mean_{p}.feather')
            tmp2 = df.ewm(span=p).std()
            tmp2.reset_index(inplace = True)
            tmp2.to_feather(self.rootpath + f'competition_trend_std_{p}.feather')
        df.reset_index(inplace = True)
        df. to_feather(self.rootpath + 'competition_trend.feather')

def update(start, end):
    period = [5, 10, 20, 50]
    f = competition_trend(start, end, period)
    f.cal()

if __name__ == '__main__':
    period = [5,10,20,50]
    f = competition_trend(20180101, 20230928, period)
    f.cal()