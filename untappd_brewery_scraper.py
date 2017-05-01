import pandas as pd 
import numpy as np 
import time
import requests
from bs4 import BeautifulSoup as bs 
import string


# ### 812 magic hat
# ### 2898 Goose

# brewery_dict = {}


# r = requests.get('https://untappd.com/w/---/16205')
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

# if meat_and_potatoes.find('div', {'class' : 'oop error'}) is not None:
#     brewery_dict['brewery_closed'] = 1
# else:
#     brewery_dict['brewery_closed'] = 0




# ###subsidiary status
# subsidiary_ids = []
# subsidiary_names = []
# if name_info.find('p', {'class' : 'subsidiary'}) is not None:
#     for element in name_info.find('p', {'class' : 'subsidiary'}).find_all('a'):
#         subsidiary_ids.append(int(element.get('href').split('/')[-1]))
#         subsidiary_names.append(element.string)
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

# print(brewery_dict)

### Import list of brewery ID Numbers here!!!!!

# dtypes_dict = {
# 'Unnamed: 0':object, 'abv':object, 'beer_id':object, 'brewery':object, 'brewery_id':object, 'date_added':object, 'description':object, 'ibu':object, 'monthly_checkins':object, 'name':object, 'oop':object, 'raters':object, 'rating':object, 'style':object, 'total_checkins':object, 'unique_checkins':object 
# }

# df = pd.read_csv('data/master_all_untappd_data.csv', dtype=dtypes_dict).iloc[:,1:].copy()



# list_of_ids = df.brewery_id.values
# print(len(list_of_ids))
# set_of_ids = []

# for i, one_id in enumerate(list_of_ids):
#     if one_id not in set_of_ids:
#         set_of_ids.append(one_id)
#     else:
#         print(i)



# print(len(set_of_ids))


# brewery_id_list = open('data/brewery_id_list.txt', 'w')
# for one_id in set_of_ids:
#     brewery_id_list.write(str(one_id)+',')

id_file = open('data/brewery_id_list.txt', 'r')
set_of_ids = id_file.read().split(',')
print(len(set_of_ids)) ### 179156
print(set_of_ids[:100])


unscraped_breweries = open('data/unscraped_brewery_ids.txt', 'a')


## Actual Scraping

list_of_breweries = []

for i in range(179100, len(set_of_ids)):
    brewery_dict = {}
    r = requests.get('https://untappd.com/w/---/%s' % set_of_ids[i])
    if r.status_code == 200:
        content = bs(r.content, 'lxml')
            ### ID
        brewery_dict['brewery_id'] = set_of_ids[i]

        meat_and_potatoes = content.find('div', {'class':'content'})
        if meat_and_potatoes is not None:
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


            #### BREWERY STILL OPEN
            if meat_and_potatoes.find('div', {'class' : 'oop error'}) is not None:
                brewery_dict['brewery_closed'] = 1
            else:
                brewery_dict['brewery_closed'] = 0

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
                hundred_breweries.to_csv('data/fresh_brew_scrape/untappd_breweries_pt1792.csv')
                print('First %s rows saved to csv!!' % str(int((i+1)/100)))
                list_of_breweries = []
        else:
            print('Weird redirect at %s' % set_of_ids[i])
    else:
        print(r.status_code)
        unscraped_breweries.write('%s,' % set_of_ids[i])















