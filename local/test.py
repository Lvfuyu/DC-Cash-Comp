import sys
import csv
import pandas as pd

def load_feature_map(fmap_file_name, f_filter_name):
	fmap = pd.read_csv(fmap_file_name)
	fmap.index = fmap.fname
	fmap = fmap.drop('fname', axis = 1)
	fmap = fmap.to_dict()['feature_id']

	feature_filter = pd.read_csv(f_filter_name)
	feature_filter = list(feature_filter.feature)

	return fmap, feature_filter

fmap, feature_filter = load_feature_map('./feature/fmap.csv','./feature/feature_importance.csv')
print fmap
print feature_filter