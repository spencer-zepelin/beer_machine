import pandas as pd 
import numpy as np 
import time
import requests
from bs4 import BeautifulSoup as bs 
import string


# ### 812 magic hat
# ### 2898 Goose

# brewery_dict = {}


# r = requests.get('https://untappd.com/w/---/264')
# content = bs(r.content, 'lxml')

# # print(content.prettify())

# meat_and_potatoes = content.find('div', {'class':'content'})

# print(meat_and_potatoes.prettify())

# name_info = meat_and_potatoes.find('div', {'class' : 'name'})
# ##name
# brewery_dict['brewery_name'] = name_info.h1.string
# ##type
# brewery_dict['brewery_type'] = name_info.find('p', {'class' : 'style'}).string
# ##location
# brewery_dict['brewery_location'] = name_info.find('p', {'class' : 'brewery'}).string
# ##description
# description = ''
# for element in meat_and_potatoes.find('div', {'class' : 'beer-descrption-read-less'}).contents:
#     if '<' not in str(element): 
#         description += element
# brewery_dict['brewery_description'] = description
# ###subsidiary status
# subsidiary_ids = []
# subsidiary_names = []
# for element in name_info.find('p', {'class' : 'subsidiary'}).find_all('a'):
#     subsidiary_ids.append(int(element.get('href').split('/')[-1]))
#     subsidiary_names.append(element.string)
# if len(subsidiary_ids) == 0:
#     brewery_dict['subsidiary_id'] = None
#     brewery_dict['subsidiary_name'] = None
# elif len(subsidiary_ids) == 1:
#     brewery_dict['subsidiary_id'] = subsidiary_ids[0]
#     brewery_dict['subsidiary_name'] = subsidiary_names[0]
# else:
#     brewery_dict['subsidiary_id'] = subsidiary_ids
#     brewery_dict['subsidiary_name'] = subsidiary_names
# ###checkins
# stats = meat_and_potatoes.find('div', {'class' : 'stats'}).find_all('span', {'class' : 'count'})
# checkins = []
# for element in stats:
#     checkins.append(element.string)
# brewery_dict['total_brewery_checkins'] = checkins[0]
# brewery_dict['unique_brewery_checkins'] = checkins[1]
# brewery_dict['monthly_brewery_checkins'] = checkins[2]
# ### lower bar info
# lower_bar = meat_and_potatoes.find('div', {'class' : 'details brewery claimed'})
# if lower_bar is not None:
#     brewery_dict['brewery_rating'] = lower_bar.find('p', {'class' : 'rating'}).find('span', {'class' : 'num'}).string
#     brewery_dict['brewery_raters'] = lower_bar.find('p', {'class' : 'raters'}).string
#     brewery_dict['brewery_num_beers'] = lower_bar.find('p', {'class' : 'count'}).a.string
#     brewery_dict['date_brewery_added'] = lower_bar.find('p', {'class' : 'date'}).string
#     brewery_dict['brewery_account_status'] = lower_bar.find('p', {'class' : 'claim'}).a.string
# else:
#     lower_bar = meat_and_potatoes.find('div', {'class' : 'details brewery'})
#     brewery_dict['brewery_rating'] = lower_bar.find('p', {'class' : 'rating'}).find('span', {'class' : 'num'}).string
#     brewery_dict['brewery_raters'] = lower_bar.find('p', {'class' : 'raters'}).string
#     brewery_dict['brewery_num_beers'] = lower_bar.find('p', {'class' : 'count'}).a.string
#     brewery_dict['date_brewery_added'] = lower_bar.find('p', {'class' : 'date'}).string
#     brewery_dict['brewery_account_status'] = 'presumed_unclaimed'
# print(brewery_dict)
# print(lower_bar.prettify())

### Import list of brewery ID Numbers here!!!!!

df = pd.read_csv('data/master_untappd_data.csv').iloc[:,1:].copy()
unscraped_breweries = open('data/unscraped_brewery_ids.txt', 'a')

list_of_ids = df.brewery_id.values
set_of_ids = []

for one_id in list_of_ids:
    if one_id not in set_of_ids:
        set_of_ids.append(one_id)
    else:
        pass


print(len(list_of_ids))
print(len(set_of_ids))


## Actual Scraping

list_of_breweries = []

for i in range(8200, len(set_of_ids)):
    brewery_dict = {}
    r = requests.get('https://untappd.com/w/---/%s' % set_of_ids[i])
    if r.status_code == 200:
        content = bs(r.content, 'lxml')
            ### ID
        brewery_dict['brewery_id'] = set_of_ids[i]

        meat_and_potatoes = content.find('div', {'class':'content'})

        name_info = meat_and_potatoes.find('div', {'class' : 'name'})
        ##name
        brewery_dict['brewery_name'] = name_info.h1.string
        ##type
        brewery_dict['brewery_type'] = name_info.find('p', {'class' : 'style'}).string
        ##location
        brewery_dict['brewery_location'] = name_info.find('p', {'class' : 'brewery'}).string
        ##description
        description = ''
        for element in meat_and_potatoes.find('div', {'class' : 'beer-descrption-read-less'}).contents:
            if '<' not in str(element): 
                description += element
        brewery_dict['brewery_description'] = description
        ###subsidiary status
        subsidiary_ids = []
        subsidiary_names = []
        subsidiaries = name_info.find('p', {'class' : 'subsidiary'})
        if subsidiaries is not None:
            for element in subsidiaries.find_all('a'):
                subsidiary_ids.append(int(element.get('href').split('/')[-1]))
                subsidiary_names.append(element.string)
            if len(subsidiary_ids) == 1:
                brewery_dict['subsidiary_id'] = subsidiary_ids[0]
                brewery_dict['subsidiary_name'] = subsidiary_names[0]
            else:
                brewery_dict['subsidiary_id'] = subsidiary_ids
                brewery_dict['subsidiary_name'] = subsidiary_names
        else:
            brewery_dict['subsidiary_id'] = None
            brewery_dict['subsidiary_name'] = None
        ###checkins
        stats = meat_and_potatoes.find('div', {'class' : 'stats'}).find_all('span', {'class' : 'count'})
        checkins = []
        for element in stats:
            checkins.append(element.string)
        brewery_dict['total_brewery_checkins'] = checkins[0]
        brewery_dict['unique_brewery_checkins'] = checkins[1]
        brewery_dict['monthly_brewery_checkins'] = checkins[2]
        ### lower bar info
        lower_bar = meat_and_potatoes.find('div', {'class' : 'details brewery claimed'})
        if lower_bar is not None:
            brewery_dict['brewery_rating'] = lower_bar.find('p', {'class' : 'rating'}).find('span', {'class' : 'num'}).string
            brewery_dict['brewery_raters'] = lower_bar.find('p', {'class' : 'raters'}).string
            brewery_dict['brewery_num_beers'] = lower_bar.find('p', {'class' : 'count'}).a.string
            brewery_dict['date_brewery_added'] = lower_bar.find('p', {'class' : 'date'}).string
            brewery_dict['brewery_account_status'] = lower_bar.find('p', {'class' : 'claim'}).a.string
        else:
            lower_bar = meat_and_potatoes.find('div', {'class' : 'details brewery'})
            brewery_dict['brewery_rating'] = lower_bar.find('p', {'class' : 'rating'}).find('span', {'class' : 'num'}).string
            brewery_dict['brewery_raters'] = lower_bar.find('p', {'class' : 'raters'}).string
            brewery_dict['brewery_num_beers'] = lower_bar.find('p', {'class' : 'count'}).a.string
            brewery_dict['date_brewery_added'] = lower_bar.find('p', {'class' : 'date'}).string
            brewery_dict['brewery_account_status'] = 'presumed_unclaimed'
        row = brewery_dict
        list_of_breweries.append(row)
        if (i+1) % 5 == 0:
            print('%s breweries scraped!!' % (i+1))
        if (i+1) % 100 == 0:
            hundred_breweries = pd.DataFrame(list_of_breweries)
            hundred_breweries.to_csv('data/untappd_breweries_pt%s.csv' % str(int((i+1)/100)))
            print('First %s rows saved to csv!!' % (i+1))
            list_of_breweries = []
    elif r.status_code != 404:
        print(r.status_code)
        unscraped_breweries.write('%s,' % set_of_ids[i])
    else:
        pass










