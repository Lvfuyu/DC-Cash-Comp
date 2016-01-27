#coding:utf-8

import sys
import codecs

raw_file_name = sys.argv[1]
pred_file_name = sys.argv[2]
output_file_name = sys.argv[3]

raw_file = open(raw_file_name, 'r')
pred_file = open(pred_file_name,'r')
output_file = codecs.open(output_file_name, 'w', 'utf-8')
output_file.write('\"uid\",\"score\"\n')

line1 = raw_file.readline()
while 1:
	line1 = raw_file.readline()
	line2 = pred_file.readline().rstrip()
	if not line1 and not line2:
		break
	uid = line1.rstrip().split(',')[0]
	score = line2.rstrip()
	output_file.write(uid + ',' + score + '\n')

raw_file.close()
pred_file.close()
output_file.close()