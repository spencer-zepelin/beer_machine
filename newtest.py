


# file = open('data/scraped_brewery_ids.txt', 'r')
# for item in file:
# 	filestring = item
# already_scraped = filestring.split(',')

# print(already_scraped)

set_of_ids = [1,2,3,4,5]

already_scraped = ['1','4']

ids_to_scrape = [id_num for id_num in set_of_ids if str(id_num) not in already_scraped]


print(ids_to_scrape)