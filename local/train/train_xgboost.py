#coding:utf-8

import numpy as np
import scipy.sparse
import xgboost as xgb
import sys

# define the preprocessing function
# used to return the preprocessed training, test data, and parameter
# we can use this to do weight rescale, etc.
# as a example, we try to set scale_pos_weight
def fpreproc(dtrain, dtest, param):
    #label = dtrain.get_label()
    #ratio = float(np.sum(label == 0)) / np.sum(label==1)
    #param['scale_pos_weight'] = ratio
    return (dtrain, dtest, param)

### simple example
# load file from text file, also binary buffer generated by xgboost
dtrain = xgb.DMatrix(sys.argv[1])
dtest = xgb.DMatrix(sys.argv[2])
pred_file = sys.argv[3]
depth = int(sys.argv[4])
num_round = int(sys.argv[5])
run_mode = sys.argv[6]

# specify parameters via map, definition are same as c++ version
label = dtrain.get_label()
ratio = float(np.sum(label == 0)) / np.sum(label==1)
#ratio = 1400.0/13458.0
param = {
		 'max_depth':depth,
		 'eta':0.2, 
		 'silent':1,
		 'objective':'binary:logistic',
		 'gamma':0.1,
		 'min_child_weight':3,
		 'eval_metric':'auc',
		 'early_stopping_rounds':5,
		 'lambda':550,
		 'scale_pos_weight':ratio,
		 'subsample':0.7,
		 'colsample_bytree':1,
		 'seed':2016
		 }
if run_mode == 'online':
	watchlist  = [(dtrain,'train')]
	bst = xgb.train(param, dtrain, num_round, watchlist)
	bst.save_model('train.model')
	# predict
	preds = bst.predict(dtest) #, ntree_limit=bst.best_ntree_limit
	with open(pred_file, 'w') as f:
	    for pred in preds:
	    	if pred > 1.0:
	    		pred = 1.0
	        f.write(str(pred)+'\n')
else:
# cross validation
	xgb.cv(param, dtrain, num_round, nfold = 5, metrics={'auc'},seed = 2016, fpreproc = fpreproc)
