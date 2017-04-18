from random import *
import requests

seed(314159)


### This seemingly magic number comes from the final index of untappd beers as of 2:15 pm central April 13, 2017
## sample function chooses elements without replacement
sample_ids = sample(range(1, 2041735), 200000)

print(sample_ids[0:10])
# [403417, 576202, 601553, 206957, 247790, 1196617, 642341, 1272478, 648741, 1072885] for seed(314159)

### TESTING

print(requests.get('https://untappd.com/b/magic-hat-brewing-company-hocus-pocus/1', allow_redirects=False))


# for number in range(161401,250001):
#     sleep(.5)
#     untappd_beer_dict = {}
#     r = requests.get('https://untappd.com/b/---/%s' % number, allow_redirects=False)
#     if r.status_code == 200:
#         content = bs(r.content, 'lxml')
#         meat_and_potatoes = content.find('div', {'class':'content'})
#         if meat_and_potatoes is not None:
#             potato = meat_and_potatoes.find('div', {'class' : 'name'})
#             details = meat_and_potatoes.find('div', {'class' : 'details'})
#             stats = meat_and_potatoes.find('div', {'class' : 'stats'}).find_all('span', {'class' : 'count'})
            
#             checkins = []
#             for element in stats:
#                 checkins.append(element.string)
#             untappd_beer_dict['total_checkins'] = checkins[0]
#             untappd_beer_dict['unique_checkins'] = checkins[1]
#             untappd_beer_dict['monthly_checkins'] = checkins[2]

#             description = ''
#             for element in meat_and_potatoes.find('div', {'class' : 'beer-descrption-read-less'}).contents:
#                 if '<' not in str(element): 
#                     description += element
#             untappd_beer_dict['description'] = description.replace('\n', ' ')

#             untappd_beer_dict['name'] = potato.h1.string
#             untappd_beer_dict['beer_id'] = meat_and_potatoes.find('a', {'class' : 'label'})['href'].split('/')[-1]
#             untappd_beer_dict['brewery'] = potato.find('p', {'class' : 'brewery'}).a.string
#             untappd_beer_dict['brewery_id'] = int(bleach(potato.find('p', {'class' : 'brewery'}).a['href']))
#             untappd_beer_dict['style'] = potato.find('p', {'class' : 'style'}).string
#             untappd_beer_dict['abv'] = details.find('p', {'class' : 'abv'}).string
#             untappd_beer_dict['ibu'] = details.find('p', {'class' : 'ibu'}).string
#             untappd_beer_dict['rating'] = details.find('p', {'class' : 'rating'}).find('span', {'class' : 'num'}).string
#             untappd_beer_dict['raters'] = details.find('p', {'class' : 'raters'}).string
#             untappd_beer_dict['date_added'] = details.find('p', {'class' : 'date'}).string

#             row = untappd_beer_dict
#             beer_fridge.append(row)

#             if number % 5 == 0:
#                 print('%s beers scraped!!' % number)
#             if number % 200 == 0:
#                 hundred_beers = pd.DataFrame(beer_fridge)
#                 hundred_beers.to_csv('data/untappd_newdata_pt%s.csv' % str(int(number/200)))
#                 print('First %s rows saved to csv!!' % number)
#                 beer_fridge = []
#         else:
#             print('Weird redirect at %s' % number)
#     elif r.status_code != 404:
#         print(r.status_code)  
#     else:
#         pass      



