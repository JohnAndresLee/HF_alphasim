import numpy as np 
import pandas as pd 
from .hffactors import HFFactors

class cgo(HFFactors):
    def _init_ (self, start, end, period_list):
        super ().__init_()
        self.start_date = start
        self.end_date = end
        self.period_list = period_list

    def cal(self):
        turnover = self.get_Kindle1M('Turnover') # axis = 1 -> minute
        volume = self.get_Kindle1M('Volume')
        expected_price = turnover / volume

        slice_ = expected_price[:, 30:-1, :]
        weights = (1/2)**np.arange(slice_.shape[1])[::-1]
        weights /= weights.sum()
        ref_price = np.nansum(slice_ * weights[:, np.newaxis], axis=1)
        close = self.get_Kindle1M('Close')
        pre_close = np.roll(close[:, -1, :], shift=1, axis=0)
        result = 1 - (ref_price - pre_close)/ref_price

        df = pd. DataFrame(result, index=self.gen_dates_list(), columns=self.gen_codes_list())
        for p in self.period_list:
            tmp1 = df.ewm(span = p).mean()
            tmp1.reset_index(inplace = True)
            tmp1.to_feather(self.rootpath + f'cgo_mean_{p}.feather')
            tmp2 = df.ewm(span=p).std()
            tmp2.reset_index(inplace = True)
            tmp2.to_feather(self.rootpath + f'cgo_std_{p}.feather')
        df.reset_index(inplace = True)
        df.to_feather(self.rootpath + 'cgo.feather')

def update(start, end) :
    period = [5, 10, 20, 50]
    f = cgo(start, end, period)
    f.cal()

if __name__ == "__main__":
    period = [5,10,20,50]
    f = cgo(20180101, 20230801, period)
    f.cal()