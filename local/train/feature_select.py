#coding:utf-8

import os
import numpy as np
import scipy.sparse
import xgboost as xgb
import sys
from time import sleep
from matplotlib import pylab as plt
import operator
import pandas as pd

bst = xgb.Booster({'nthread':4}) #init model
bst.load_model("train.model") # load data

importance = bst.get_fscore(fmap='')
importance = sorted(importance.items(), key=operator.itemgetter(1),reverse=True)

df = pd.DataFrame(importance, columns=['feature','fscore'])
df['fscore'] = df['fscore'] / df['fscore'].sum()

print len(df.index)
#print df
df.to_csv('../feature/feature_importance.csv')

#xgb.plot_importance(bst)
#sleep(10000)
#os.system("pause")