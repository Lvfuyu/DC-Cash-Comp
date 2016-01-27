# folder directory 
data_dir=./data
out_dir=./feature

# generate train feature
python feature_format.py ${data_dir}/features_type.csv ${data_dir}/train_x.csv ${data_dir}/category_level.txt ${out_dir}/feature_train.txt train ${data_dir}/train_y.csv

# generate test feature
python feature_format.py ${data_dir}/features_type.csv ${data_dir}/test_x.csv ${data_dir}/category_level.txt ${out_dir}/feature_test.txt test
