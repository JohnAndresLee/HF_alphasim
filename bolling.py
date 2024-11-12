import numpy as np 
import pandas as pd 
from .hffactors import HFFactors

class bolling(HFFactors):
    def _init_(self, start, end, period_list):
        super ()._init_()
        self.start_date = start
        set. period_list = period_list

    def cal(self): 
        close = self.get_Kindle1M('Close')

        deviation = -(np.nanmean(close[:, -30:, :], axis = 1) - np.nanmean(close, axis = 1)) / np.nanstd(close, axis = 1)

        buy_amount = self.get_IntradayAlpha('task1_buy_amount').transpose(0, 2, 1)
        sell_amount = self.get_IntradayAlpha('task1_sell_amount').transpose(0, 2, 1)
        buy_ratio = buy_amount / (buy_amount + sell_amount)
        sell_ratio = sell_amount / (buy_amount + sell_amount)

        sig = np.where(deviation > 0, np.nanmean(buy_ratio, axis = 1), np.nanmean(sell_ratio,axis = 1))
        result = deviation * sig

        df = pd.DataFrame(result, index=self.gen_dates_list(), columns=self.gen_codes_list())
        for p in self.period_list:
            tmp1 = df.ewm(span = p) .mean()
            tmp1.reset_index(inplace = True)
            tmp1. to_feather(self.rootpath + f'bolling_mean_{p}.feather')
            tmp2 = df.ewm(span=p).std()
            tmp2.reset_index(inplace = True)
            tmp2.to_feather(self.rootpath + f'bolling_std_{p}.feather')
        df.reset_index(inplace = True)
        df.to_feather(self.rootpath + 'bolling.feather')

def update(start, end):
    period = [5, 10, 20, 50]
    f = bolling(start, end, period)
    f.cal()

if __name__ == '__main__':
    period = [5,10,20,50]
    f = bolling(20180101, 20230818, period)
    f.cal()