from util import *
data = get_json_file('temp/1.json')
data = data['statuses']
for d in data:
	print(d.get('mblogtype'), d.get('ad_state'), d.get('mblogtypename'), d.get('readtimetype'))
	# if d.get('mblogtype') != 0:
	# 	print(d)
a=1