import pandas as pd 
import numpy as np 
import time
import requests
from bs4 import BeautifulSoup as bs 
import string



#### Test Scraping up here


# untappd_beer_dict = {}


# r = requests.get('https://untappd.com/b/---/1')
# with open('temp_untappd_page.html', 'wb') as f:
#     f.write(r.content)
# with open('temp_untappd_page.html', 'r') as f:
#     content = bs(f.read(), 'lxml')

# # print(content.prettify())

# meat_and_potatoes = content.find('div', {'class':'content'})

# # print(meat_and_potatoes.prettify())

# potato = meat_and_potatoes.find('div', {'class' : 'name'})

# # print(potato.prettify())

# untappd_beer_dict['name'] = potato.h1.string

# untappd_beer_dict['brewery'] = potato.find('p', {'class' : 'brewery'}).a.string

# untappd_beer_dict['style'] = potato.find('p', {'class' : 'style'}).string

# details = meat_and_potatoes.find('div', {'class' : 'details'})

# stats = meat_and_potatoes.find('div', {'class' : 'stats'}).find_all('span', {'class' : 'count'})


# checkins = []
# for element in stats:
#     checkins.append(element.string)

# untappd_beer_dict['total_checkins'] = checkins[0]
# untappd_beer_dict['unique_checkins'] = checkins[1]
# untappd_beer_dict['monthly_checkins'] = checkins[2]

# description = ''
# for element in meat_and_potatoes.find('div', {'class' : 'beer-descrption-read-less'}).contents:
#     if '<' not in str(element): 
#         description += element

# untappd_beer_dict['description'] = description.replace('\n', ' ')


# # print(stats.prettify())

# # print(details.prettify())

# # print(details.find('p', {'class' : 'rating'}).find('span', {'class' : 'num'}).string)



# def bleach(string):
#     temp = ""
#     string = str(string)
#     for i in string:
#         if i in ["1","2","3","4","5","6","7","8","9","0", "."]:
#             temp += i
#     if len(temp) > 0:
#         return float(temp)


# untappd_beer_dict['abv'] = bleach(details.find('p', {'class' : 'abv'}).string)
# untappd_beer_dict['ibu'] = bleach(details.find('p', {'class' : 'ibu'}).string)
# untappd_beer_dict['rating'] = bleach(details.find('p', {'class' : 'rating'}).find('span', {'class' : 'num'}).string)
# untappd_beer_dict['raters'] = bleach(details.find('p', {'class' : 'raters'}).string)
# untappd_beer_dict['date_added'] = details.find('p', {'class' : 'date'}).string

# print(untappd_beer_dict)









##### The actual scraping is down here 


beer_fridge = []

for number in range(18601,100001):
    try:
        untappd_beer_dict = {}
        r = requests.get('https://untappd.com/b/---/%s' % number)
        content = bs(r.content, 'lxml')

        meat_and_potatoes = content.find('div', {'class':'content'})
        potato = meat_and_potatoes.find('div', {'class' : 'name'})
        details = meat_and_potatoes.find('div', {'class' : 'details'})
        stats = meat_and_potatoes.find('div', {'class' : 'stats'}).find_all('span', {'class' : 'count'})
        
        checkins = []
        for element in stats:
            checkins.append(element.string)
        untappd_beer_dict['total_checkins'] = checkins[0]
        untappd_beer_dict['unique_checkins'] = checkins[1]
        untappd_beer_dict['monthly_checkins'] = checkins[2]

        description = ''
        for element in meat_and_potatoes.find('div', {'class' : 'beer-descrption-read-less'}).contents:
            if '<' not in str(element): 
                description += element
        untappd_beer_dict['description'] = description.replace('\n', ' ')

        untappd_beer_dict['name'] = potato.h1.string
        untappd_beer_dict['brewery'] = potato.find('p', {'class' : 'brewery'}).a.string
        untappd_beer_dict['style'] = potato.find('p', {'class' : 'style'}).string
        untappd_beer_dict['abv'] = details.find('p', {'class' : 'abv'}).string
        untappd_beer_dict['ibu'] = details.find('p', {'class' : 'ibu'}).string
        untappd_beer_dict['rating'] = details.find('p', {'class' : 'rating'}).find('span', {'class' : 'num'}).string
        untappd_beer_dict['raters'] = details.find('p', {'class' : 'raters'}).string
        untappd_beer_dict['date_added'] = details.find('p', {'class' : 'date'}).string

        row = untappd_beer_dict
        beer_fridge.append(row)

        if number % 5 == 0:
            print('%s beers scraped!!' % number)
        if number % 100 == 0:
            hundred_beers = pd.DataFrame(beer_fridge)
            hundred_beers.to_csv('data/untappd_data_pt%s.csv' % str(int(number/100)))
            print('First %s rows saved to csv!!' % number)
            beer_fridge = []
    except:
        pass


