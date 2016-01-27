#coding:utf-8
# usage: python sample.py 3500

import sys
import random
import numpy as np
import pandas as pd

uid2y = pd.read_csv('../data/train_y.csv')
uidOfyZero = uid2y[uid2y['y'] == 0]
uidOfyNZero = uid2y[uid2y['y'] == 1]

negSample_count = len(uidOfyZero.index)
posSample_count = len(uidOfyNZero.index)

#print uidOfyZero.reindex(range(negSample_count))

print 'The number of negative sample is: ' + str(negSample_count)
print 'The number of positive sample is: ' + str(posSample_count)

# specify positive sample number
sample_range = random.sample(uidOfyNZero.index, int(sys.argv[1]))
samp_uidOfNZero = uidOfyNZero.ix[sample_range]
#print uidOfyNZero.ix[sample_range]

train_sample = [uidOfyZero, samp_uidOfNZero]
train_sample = pd.concat(train_sample)
#print train_sample
print 'The number of sample after balance is: ' + str(len(train_sample.index))

train_sample.to_csv('./data/train_y.csv', encoding='utf-8', index = False)