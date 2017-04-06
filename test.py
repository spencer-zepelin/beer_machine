


unscraped_breweries = open('data/unscraped_brewery_ids.txt', 'w')


for element in ['a','b','c','d']:
    unscraped_breweries.write('%s\n' % element)