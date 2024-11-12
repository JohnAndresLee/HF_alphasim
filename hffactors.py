import numpy as np 
from numba import jit 
import pandas as pd 
import os 
import time 
import datetime
from .function_tools import compute_mean, compute_std, compute_skew, compute_kurt 
from .PythonAlpha import PyAlphaApi as api

dc = api.DataCache("/mnt/NFS95/Data/ProductionCache", "/mnt/NFS95/AlphaPoo1")

class HFFactors:
    def _init_(self, root = '/mnt/disk2/common/onlinev3/factors/HFFactors_alphasim/', start = 20180101, end=20230801):
        self.rootpath = root
        self.start_date = start
        self. end_date = end

    def get_IntradayAlpha(self, agg_name):
        # data: first axis-date; second axis-code; third axis-minute
        data = dc.GetIntradayAlpha("chenpeng", agg_name, start_date=self.start_date, end_date=self.end_date)
        # data = np.nan_to_num(data) # replace NaN with 0
        return data

    def get_Kindle1M(self, name):
        """
        field: InstrumentID,TradingDay,StartTime,EndTime,OpenPrice,ClosePrice,HighPrice, LowPrice,TotalVolume,LastVolume,
            OpenInterest, LastTurnover, KindlePeriod (60)
        """
        # only numpy is available for Cube, cannot convert to pandas
        # data: first axis-date; second axis-minute; third axis-code
        k_np = dc.GetNumData('Kindle1M', name, np.float64, start_date=self.start_date, end_date=self.end_date) # Cube, iH-FaE
        data = np.nan_to_num(k_np)
        return data

    def gen_dates_list(self):
        start_ind = np.searchsorted(dc.Dates, self.start_date, side='left')
        end_ind = np.searchsorted(dc.Dates, self.end_date, side='right' )
        dates_list = dc.Dates[start_ind: end_ind]
        return dates_list

    def gen_codes_list(self):
        return dc.Instruments

    def compute_mean(self, arr, axis, step):
        return compute_mean(arr, axis, step)
    
    def compute_std(self, arr, axis, step): 
        return compute_std(arr, axis, step)

    def compute_skew(self, arr, axis, step): 
        return compute_skew(arr, axis, step)
    
    def compute_kurt(self, arr, axis, step): 
        return compute_kurt(arr, axis, step)
    
    def z_score(self, arr, axis):
        mean = np.nanmean(arr, axis = axis, keepdims=True)
        std = np.nanstd(arr, axis = axis, keepdims=True)
        std[std == 0] = 1
        z = (arr-mean)/std
        return z
    
if __name__ == '__main__':
    test = HFFactors()
    data = test.get_Kindle1M('High')
    mean = test.compute_mean(data, axis=1, step=60)
    print (mean.shape)
    std = test.compute_std(data, axis=1, step=60)
    print(std.shape)
    skew = test.compute_skew(data, axis=1, step=60)
    print (skew.shape)
    kurt = test.compute_kurt(data, axis=1, step=60)
    print (kurt.shape)