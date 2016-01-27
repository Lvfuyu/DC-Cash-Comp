#运行流程#
----------

* cd ./local
* sample.py 保留所有负样本，对正样本进行取样，取样后数据格式同原始数据，数据目录在/local/data
* sh feature_format.sh. 对./local/data里的数据特征处理，输出libsvm格式，输出目录在./local/feature，目前所有特征，category特征onehot coding处理
* cd ./local/train
* sh train_pred.sh 参数在shell脚本和train_xgboost.py里调

#线上目前最好参数#
----------
* 线上结果: 0.7116
* 样本: 所有样本，相当于全部取样
* depth: 8
* round: 430
* eta: 0.2
* gamma: 0.1
* min_child_weight: 3
* lambda: 550
* scale_pos_weight: neg_num/pos_num ~= 1400.0/13458.0
* subsample: 0.7
* colsample_bytree: 0.4
* seed:2016

#线下#
----------
* 5折交叉验证