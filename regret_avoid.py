import numpy as np
import pandas as pd
from .hffactors import HFFactors

class regret_avoid(HFFactors):
    def __init__(self, start, end, period_list):
        super().__init__()
        self.start_date = start
        self.end_date = end
        self.period_list = period_list

    def cal(self):
        ## 此处turnover是成交金额
        turnover = self.get_Kindle1M('Turnover') #axis = 1 -> minute
        volume = self.get_Kindle1M('Volume')
        buy_volume = self.get_IntradayAlpha("task1_buy_volume").transpose(0, 2, 1)# axis=2 ->minute
        sell_volume = self.get_IntradayAlpha("task1_sell_volume").transpose(0, 2, 1)

        expected_price = turnover / volume
        last_ep = expected_price[:, -1:, :]
        holding_gain = (last_ep - expected_price) / expected_price

        positive_gain = np.where(holding_gain > 0, 1, 0) 
        negative_gain = np.where(holding_gain < 0, 1, 0)

        sell_tmp = sell_volume * np.abs(buy_volume * negative_gain) / np.nanmean(sell_volume, axis = 1, keepdims=True)
        buy_tmp = buy_volume * np.abs(sell_volume * positive_gain) / np.nanmean (buy_volume, axis = 1, keepdims=True)

        HCVOL = np.nanmean(buy_tmp, axis = 1, keepdims=True) / np.nansum(volume, axis = 1, keepdims=True)
        LCVOL = np.nanmean(sell_tmp, axis = 1, keepdims=True) / np.nansum(volume, axis = 1, keepdims=True)

        score = 0.2 * self.z_score(HCVOL, axis = 2) + 0.8 * self.z_score(LCVOL, axis = 2)
        
        df = pd.DataFrame(score.squeeze(axis = 1), index=self.gen_dates_list(), columns=self.gen_codes_list())
        for p in self.period_list:
            tmp1 = df.ewm(span = p).mean()
            tmp1.reset_index(inplace = True)
            tmp1.to_feather(self.rootpath+f'regret_avoid_mean_{p}.feather')
            tmp2 = df.ewm(span=p).std()
            tmp2.reset_index(inplace = True)
            tmp2.to_feather(self.rootpath + f'regret_avoid_std_{p}.feather')
        df.reset_index(inplace = True)
        df.to_feather(self.rootpath + 'regret_avoid.feather')

def update(start, end):
    period = [5, 10, 20, 50]
    f = regret_avoid(start, end, period)
    f.cal()

if __name__ == "__main__":
    period = [5, 10, 20, 50]
    f = regret_avoid(20180101, 20231009, period)
    f.cal()