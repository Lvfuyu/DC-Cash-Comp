#encoding:utf-8

import sys
import csv
import pandas as pd

def load_feature_map(fmap_file_name, f_filter_name):
	fmap = pd.read_csv(fmap_file_name)
	fmap.index = fmap.fname
	fmap = fmap.drop('fname', axis = 1)
	fmap = fmap.to_dict()['feature_id']

	feature_filter = pd.read_csv(f_filter_name)
	feature_filter.index = feature_filter.feature
	feature_filter = feature_filter.drop('feature', axis = 1)
	feature_filter = feature_filter.to_dict()['fscore']

	return fmap, feature_filter

'''
transform category feature to one-pot numberic feature 
'''
def trans_cat2numb(cat2level, f_id, index):
	
	f_num = cat2level[f_id][0]
	f_begin = cat2level[f_id][1]
	interval = index - f_begin + 1
	onepot = '0' * (interval - 1)
	onepot += '1'
	onepot += '0' * (f_num - interval)
	return onepot

'''
load category-level file, format: feature_id, level_num, level_min
'''
def load_cat_level(cat_file_name):
	cat_file = open(cat_file_name, 'r')
	
	cat2level = {}
	line = cat_file.readline()
	while line:
		f_id, f_num, f_begin = line.strip('\n').split('\t')
		cat2level[f_id] = [int(f_num), int(f_begin)]
		line = cat_file.readline()

	cat_file.close()
	return cat2level

''' 
load feature type 
'''
def load_feature_type(feature_type_name):

	feature_type_file = file(feature_type_name, 'r')
	reader = csv.reader(feature_type_file)

	feature2type = {}
	for line in reader:
		if len(line) < 2:
			continue
		feature2type[line[0]] = line[1]
	
	feature_type_file.close()
	return feature2type
#print feature2type['x1']

'''
load the target 
'''

def load_target(target_name):

	if (target_name == ''):
		return {}

	target_file = file(target_name, 'r')
	reader = csv.reader(target_file)

	user2y = {}
	for line in reader:
		if reader.line_num == 1:
			continue
		user2y[line[0]] = line[1]

	target_file.close()
	return user2y

''' 
merge feature and target into libsvm format file
'''

def gen_feature_libsvm(feature_name, svm_name, feature2type, user2y, 
					   cat2level, file_type, fmap, feature_filter):
	
	svm_file = open(svm_name, 'w')
	feature_file = file(feature_name, 'r')
	reader = csv.reader(feature_file)

	for line in reader:
		if reader.line_num == 1:
			continue
		# line is a feature list 
		uid = line[0]
		target = '0'
		if file_type == 'train':
			if user2y.has_key(uid):
				target = user2y[uid]
			else:
				continue
		svm_file.write(target)

		num_feature = -1
		num_write_feature = 0
		for f in line:
			if num_feature == -1:
				num_feature = 0
				continue
			
			num_feature += 1
			# temporally omitting category feature
			f_id = 'x'+str(num_feature)

			if feature2type[f_id] == 'category':
				f = f.strip('\"')
				index = int(f)
				onepot = trans_cat2numb(cat2level, f_id, index)
				for loc, bit in enumerate(onepot):
					if not feature_filter.has_key(fmap[f_id + '_' + str(loc)]):
						continue
					if bit == '1':
						svm_file.write(' ' + str(num_write_feature) + ':' + bit)
					num_write_feature += 1
			else:
				if not feature_filter.has_key(fmap[f_id]):
					continue
				if f != '0' and f != '0.0':
					svm_file.write(' ' + str(num_write_feature) + ':' + f)
				num_write_feature += 1
		
		svm_file.write('\n')

	feature_file.close()
	svm_file.close()
	return num_write_feature

if __name__ == '__main__':
	feature_type_name = sys.argv[1]
	feature_name = sys.argv[2]
	cat_level_name = sys.argv[3]
	svm_name = sys.argv[4]
	file_type = sys.argv[5]

	target_name = ''
	if file_type == 'train':
		target_name = sys.argv[6]
	user2y = load_target(target_name)

	feature2type = load_feature_type(feature_type_name)
	cat2level = load_cat_level(cat_level_name)
	fmap, feature_filter = load_feature_map('./feature/fmap.csv','./feature/feature_importance.csv')
	num_write_feature = gen_feature_libsvm(feature_name, svm_name, feature2type, user2y, 
					   					   cat2level, file_type, fmap, feature_filter)
	print 'Total feature is : ' + str(num_write_feature)
