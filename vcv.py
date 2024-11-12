import numpy as np
import pandas as pd
from hffactors import HFFactors

class vcv(HFFactors):
    def __init__(self, start, end, period_list):
        super().__init__()
        self.start_date = start
        self.end_date = end
        self.period_list = period_list

    def cal(self):
        buy_amount = self.get_IntradayAlpha('task1_buy_amount').transpose(0, 2, 1)
        sell_amount = self.get_IntradayAlpha('task1_sell_amount').transpose(0, 2, 1)
        v = 0.5 * ((buy_amount + sell_amount) + np.abs(buy_amount - sell_amount))
        signal = np.nanstd(v, axis=1) / np.nanmean(v, axis=1)
        df = pd.DataFrame(signal, index=self.gen_dates_list(), columns=self.gen_codes_list())
        for p in self.period_list:
            tmp1 = df.ewm(span = p).mean()
            tmp1.reset_index(inplace = True)
            tmp1.to_feather(self.rootpath + f'vcv_mean_{p}.feather')
            tmp2 = df.ewm(span=p).std()
            tmp2.reset_index(inplace = True)
            tmp2.to_feather(self.rootpath + f'vcv_trend_std_{p}.feather')
        df.reset_index(inplace = True)
        df.to_feather(self.rootpath + 'vcv.feather')
                   
def update(start, end):
    period = [5, 10, 20, 50]
    f = vcv(start, end, period)
    f.cal()

if __name__ == "__main__":
    period = [5,10,20,50]
    f = vcv(20180101, 20240101, period)
    f.cal()