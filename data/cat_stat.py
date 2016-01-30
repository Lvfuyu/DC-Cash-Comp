#encoding:utf-8
# shell usage: python cat_stat.py features_type.csv train_x.csv test_x.csv train_unlabeled.csv cat_level.txt

import sys
import csv

def update_cat_stat(feature2level, feature_file_name):
	feature_file = file(feature_file_name, 'r')
	reader = csv.reader(feature_file)

	for line in reader:
		if reader.line_num == 1:
			continue
		# line is a feature list 
		num_feature = 0
		for f in line:
			if num_feature  == 0:
				num_feature = 1
				continue
			f_key = 'x'+str(num_feature)
			if feature2level.has_key(f_key):
				feature2level[f_key].add(f)
			num_feature += 1
	
	feature_file.close()
	pass

feature_type_name = sys.argv[1]
feature_type_file = file(feature_type_name, 'r')
reader = csv.reader(feature_type_file)

feature2level = {}
for line in reader:
	if line[1] == 'category':
		feature2level[line[0]] = set([])
feature_type_file.close()

update_cat_stat(feature2level, sys.argv[2])
update_cat_stat(feature2level, sys.argv[3])
update_cat_stat(feature2level, sys.argv[4])

output_file_name = sys.argv[5]
output_file = open(output_file_name, 'w')
for (key, level) in feature2level.items():
	output_file.write(key + '\t' + str(len(level)) + '\t')
	for it in level:
		output_file.write(it)
		output_file.write(' ')
	output_file.write('\n')
output_file.close()



