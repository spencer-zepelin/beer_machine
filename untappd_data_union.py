import pandas as pd 

missing_frames = []
list_of_dataframes = []
for x in range(1, 808):
	try:
		list_of_dataframes.append(pd.read_csv('data/untappd_newdata_pt%s.csv' % x))
	except:
		print(x)
		missing_frames.append(x)

have = len(list_of_dataframes)
dont_have = len(missing_frames)

assert have + dont_have == len(range(1, 808))

all_the_beers = pd.concat(list_of_dataframes, axis=0)
all_the_beers.to_csv('data/master_untappd_data.csv')



list_of_brewery_dataframes = []
for brewery_page in range(1, 155):
	try:
		list_of_brewery_dataframes.append(pd.read_csv('data/untappd_breweries_pt%s.csv' % brewery_page))
	except:
		print(brewery_page)

all_the_breweries = pd.concat(list_of_brewery_dataframes, axis=0)
all_the_breweries.to_csv('data/master_untappd_brewery_data.csv')




# print(list_of_dataframes[0].shape)
# print(all_the_beers.shape)

