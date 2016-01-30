#coding:utf-8

import sys
import csv
from feature_format import load_feature_type, load_cat_level, trans_cat2numb

feature_map = open('./feature/fmap.csv','w')
feature_file = file('./data/train_x.csv', 'r')
feature2type = load_feature_type('./data/features_type.csv')
cat2level = load_cat_level('./data/category_level.txt')

feature_map.write('fname,feature_id\n')
reader = csv.reader(feature_file)

for line in reader:
	if reader.line_num == 1:
		continue
	uid = line[0]
	num_feature = -1
	num_write_feature = 0
	for f in line:
		if num_feature == -1:
			num_feature = 0
			continue
		
		num_feature += 1
		f_id = 'x'+str(num_feature)
		if feature2type[f_id] == 'category':
			f = f.strip('\"')
			index = int(f)
			onepot = trans_cat2numb(cat2level, f_id, index)
			for loc, bit in enumerate(onepot):
				feature_map.write(f_id + '_' + str(loc) + ',' + 
								  'f' + str(num_write_feature)+'\n')	
				num_write_feature += 1
		else:
			feature_map.write(f_id + ',' + 'f' + str(num_write_feature) +'\n')
			num_write_feature += 1
	break

feature_file.close()
feature_map.close()