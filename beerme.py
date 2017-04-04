import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

beers = pd.read_csv('cribbed_beerme.csv')

beers.columns = beers.iloc[0]
beers = beers[1:]


print(beers.columns)

beers.drop(beers.columns[-1], axis=1, inplace=True) 

print(beers.head())

print(beers.Location.value_counts())
print(beers.info())

def USA(location):
	return location.startswith('United States')

us_beers = beers[beers.Location.apply(USA)].copy()


print(us_beers.info())

print(us_beers['Brewery / Beer'].nunique())

def get_state(location):
	return location.split(' - ')[1]

def fix_half(amount_string):
	return float(str(amount_string).replace('½', '.5'))

us_beers['Location'] = us_beers['Location'].apply(get_state)


print(us_beers.Location.nunique())

# print(float(us_beers.iloc[0, 4]))

us_beers['Score'] = us_beers['Score'].apply(fix_half)

print(us_beers.Score.describe())

us_beers.Score.fillna(15.5, inplace=True)






# plt.hist(us_beers.Score, bins=np.arange(4,20,0.5))
# plt.savefig('beerme_distribution.png')


print(us_beers.groupby('Location')['Score'].mean().sort_values(ascending=False))







