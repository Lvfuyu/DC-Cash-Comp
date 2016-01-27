
feature_dir=../feature
raw_data_dir=../data

depth=8
round=1000
run_mode=offline # online

python train_xgboost.py ${feature_dir}/feature_train.txt ${feature_dir}/feature_test.txt pred.txt $depth $round $run_mode
if [ "$run_mode" = "online" ] ; then
python gen_submit.py ${raw_data_dir}/test_x.csv ./pred.txt ../submit.csv
fi