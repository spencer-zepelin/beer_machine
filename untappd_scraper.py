import pandas as pd 
import numpy as np 
import time
import requests
from bs4 import BeautifulSoup as bs 

untappd_beer_dict = {}

# IF COMMMENTED OUT BELOW, BC FILE ALREADY SCRAPED
r = requests.get('https://untappd.com/b/---/5')

with open('temp_untappd_page.html', 'wb') as f:
    f.write(r.content)

with open('temp_untappd_page.html', 'r') as f:
    content = bs(f.read(), 'lxml')

# print(content.prettify())

meat_and_potatoes = content.find('div', {'class':'content'})

# print(meat_and_potatoes.prettify())

potato = meat_and_potatoes.find('div', {'class' : 'name'})

# print(potato.prettify())

untappd_beer_dict['name'] = potato.h1.string

untappd_beer_dict['brewery'] = potato.find('p', {'class' : 'brewery'}).a.string

untappd_beer_dict['style'] = potato.find('p', {'class' : 'style'}).string

details = meat_and_potatoes.find('div', {'class' : 'details'})

print(details.prettify())

# print(details.find('p', {'class' : 'rating'}).find('span', {'class' : 'num'}).string)



def bleach(string):
    temp = ""
    string = str(string)
    for i in string:
        if i in ["1","2","3","4","5","6","7","8","9","0", "."]:
            temp += i
    if len(temp) > 0:
        return float(temp)


untappd_beer_dict['abv'] = bleach(details.find('p', {'class' : 'abv'}).string)
untappd_beer_dict['ibu'] = details.find('p', {'class' : 'ibu'}).string
untappd_beer_dict['rating'] = details.find('p', {'class' : 'rating'}).find('span', {'class' : 'num'}).string
untappd_beer_dict['raters'] = details.find('p', {'class' : 'raters'}).string
untappd_beer_dict['date_added'] = details.find('p', {'class' : 'date'}).string

print(untappd_beer_dict)
# ### now that we have extracted the movieID, time to abstract the process



# # for potato in meat_and_potatoes.find_all('div', {'class' : 'lister-item-image'}):
# # 	print(potato.img['data-tconst'])

# ### http://www.imdb.com/search/title?release_date=2016&view=simple&sort=num_votes,desc&page=3 <---- this page number is what we want to vary to scrape over pages


# movieID_2016 = []

# for page in range(1, 51):
# 	r = requests.get('http://www.imdb.com/search/title?release_date=2016&view=simple&sort=num_votes,desc&page=%s' % str(page))
# 	content = bs(r.content, 'lxml')
# 	meat_and_potatoes = content.find('div', {'class':'lister-list'})
# 	for potato in meat_and_potatoes.find_all('div', {'class' : 'lister-item-image'}):
# 		movieID_2016.append(potato.img['data-tconst'])
# 	print('Page %s complete!' % page)

# np.save('assets/movie_ids_2016.npy', movieID_2016)

# def hows_that_beer(number):
# meat_and_potatoes = content.find('div', {'class':'content'})
# potato = meat_and_potatoes.find('div', {'class' : 'name'})
# details = meat_and_potatoes.find('div', {'class' : 'details'})

# untappd_beer_dict['name'] = potato.h1.string
# untappd_beer_dict['brewery'] = potato.find('p', {'class' : 'brewery'}).a.string
# untappd_beer_dict['style'] = potato.find('p', {'class' : 'style'}).string
# untappd_beer_dict['abv'] = details.find('p', {'class' : 'abv'}).string
# untappd_beer_dict['ibu'] = details.find('p', {'class' : 'ibu'}).string
# untappd_beer_dict['rating'] = details.find('p', {'class' : 'rating'}).find('span', {'class' : 'num'}).string
# untappd_beer_dict['raters'] = details.find('p', {'class' : 'raters'}).string
# untappd_beer_dict['date_added'] = details.find('p', {'class' : 'date'}).string



