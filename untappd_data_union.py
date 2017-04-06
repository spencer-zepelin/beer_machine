import pandas as pd 

missing_frames = []
list_of_dataframes = []
for x in range(1, 101):
	try:
		list_of_dataframes.append(pd.read_csv('data/untappd_newdata_pt%s.csv' % x))
	except:
		print(x)
		missing_frames.append('%s,' % x)



have = len(list_of_dataframes)
dont_have = len(missing_frames)

assert have + dont_have == len(range(1, 101))

print(list_of_dataframes[0].shape)

all_the_beers = pd.concat(list_of_dataframes, axis=0)

print(all_the_beers.shape)

all_the_beers.to_csv('data/master_untappd_data.csv')

