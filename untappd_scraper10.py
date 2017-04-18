import pandas as pd 
import numpy as np 
from time import sleep
import requests
from bs4 import BeautifulSoup as bs 
import string




def bleach(string):
    temp = ""
    string = str(string)
    for i in string:
        if i in ["1","2","3","4","5","6","7","8","9","0", "."]:
            temp += i
    if len(temp) > 0:
        return float(temp)


### Test Scraping up here
###200441 infinite redirect

# untappd_beer_dict = {}

# try:
#     r = requests.get('https://untappd.com/b/---/200441')
# except requests.exceptions.TooManyRedirects:
#     print('got it right!!!')
    # print(type(inst))    # the exception instance
    # print(inst.args)     # arguments stored in .args
    # print(inst) 



# with open('temp_untappd_page.html', 'wb') as f:
#     f.write(r.content)
# with open('temp_untappd_page.html', 'r') as f:
#     content = bs(f.read(), 'lxml')

# # print(content.prettify())

# meat_and_potatoes = content.find('div', {'class':'content'})

# if meat_and_potatoes.find('div', {'class' : 'oop error'}) is not None:
#     untappd_beer_dict['oop'] = 1
# else:
#     untappd_beer_dict['oop'] = 0


# # print(meat_and_potatoes.prettify())

# print(untappd_beer_dict['oop'])

# potato = meat_and_potatoes.find('div', {'class' : 'name'})

# print(potato.prettify())


# print(int(bleach(meat_and_potatoes.find('a', {'class' : 'label'})['href'])))

# untappd_beer_dict['name'] = potato.h1.string
# untappd_beer_dict['beer_id'] = int(bleach(meat_and_potatoes.find('a', {'class' : 'label'})['href']))
# untappd_beer_dict['brewery'] = potato.find('p', {'class' : 'brewery'}).a.string
# untappd_beer_dict['brewery_id'] = int(bleach(potato.find('p', {'class' : 'brewery'}).a['href']))
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




# untappd_beer_dict['abv'] = bleach(details.find('p', {'class' : 'abv'}).string)
# untappd_beer_dict['ibu'] = bleach(details.find('p', {'class' : 'ibu'}).string)
# untappd_beer_dict['rating'] = bleach(details.find('p', {'class' : 'rating'}).find('span', {'class' : 'num'}).string)
# untappd_beer_dict['raters'] = int(bleach(details.find('p', {'class' : 'raters'}).string))
# untappd_beer_dict['date_added'] = details.find('p', {'class' : 'date'}).string

# # print(untappd_beer_dict)






    


#### The actual scraping is down here 


beer_fridge = []


for number in range(1030801, 1100001):
    untappd_beer_dict = {}
    try:
        try:
            r = requests.get('https://untappd.com/b/---/%s' % number)
            if r.status_code == 200:
                content = bs(r.content, 'lxml')
                meat_and_potatoes = content.find('div', {'class':'content'})
                if meat_and_potatoes is not None:
                    potato = meat_and_potatoes.find('div', {'class' : 'name'})
                    details = meat_and_potatoes.find('div', {'class' : 'details'})
                    stats = meat_and_potatoes.find('div', {'class' : 'stats'}).find_all('span', {'class' : 'count'})
                    
                    if meat_and_potatoes.find('div', {'class' : 'oop error'}) is not None:
                        untappd_beer_dict['oop'] = 1
                    else:
                        untappd_beer_dict['oop'] = 0

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
                    untappd_beer_dict['beer_id'] = meat_and_potatoes.find('a', {'class' : 'label'})['href'].split('/')[-1]
                    untappd_beer_dict['brewery'] = potato.find('p', {'class' : 'brewery'}).a.string
                    untappd_beer_dict['brewery_id'] = int(bleach(potato.find('p', {'class' : 'brewery'}).a['href']))
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
                    if number % 200 == 0:
                        hundred_beers = pd.DataFrame(beer_fridge)
                        hundred_beers.to_csv('data/all_untappd/beer10/untappd_beers_pt%s.csv' % str(int(number/200)))
                        print('First %s rows saved to csv!!' % number)
                        beer_fridge = []
                else:
                    print('Weird redirect at %s' % number)
            elif r.status_code != 404:
                print(r.status_code)  
            else:
                pass
        except requests.exceptions.TooManyRedirects:
            print("It's a trap!!!")
            pass      
    except (requests.exceptions.SSLError, requests.exceptions.ConnectionError, http.client.RemoteDisconnected, requests.packages.urllib3.exceptions.ProtocolError):
        print('quick gang! They\'re onto us!!')
        sleep(10)


