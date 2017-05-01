### TO EXPLORE: 
# - Is being a subsidiary substantively different than number subsidiaries? 



### columns to work on: 'name', 'brewery', 'style', 
                     #  , 'beer_id', 'brewery_id', 
       #, 'brewery_id', , 'brewery_name',
       #   'brewery_type',



## COLUMNS PARTIALLY COMPLETE: 
# 'description' --> boolean and wordcount done, no NLP yet
# 'brewery_description' ---> boolean and wordcount done, no NLP yet
#'subsidiary_id', 'subsidiary_name', ----> boolean done, no further
#'brewery_location' ---> 'in us' complete



#### Features accounted for:
## Numeric: 'rating', 'raters', 'abv', 'ibu', 'total_checkins', 'unique_checkins', 'monthly_checkins','total_brewery_checkins', 'unique_brewery_checkins', 'monthly_brewery_checkins', 'brewery_raters', 'brewery_rating', 'brewery_num_beers',

### Datetime: 'date_added', 'date_brewery_added', ---> time delta????

### Naturally Boolean: 'oop', 'brewery_account_status',


from datetime import datetime
import pandas as pd

#### HELPER FUNCTIONS

def bleach(string):
    temp = ""
    string = str(string)
    if 'M' in string:
        for i in string:
            if i in ["1","2","3","4","5","6","7","8","9","0", "."]:
                temp += i
        if len(temp) > 0:
            return float(temp) * 1000000
    else:
        for i in string:
            if i in ["1","2","3","4","5","6","7","8","9","0", "."]:
                temp += i
        if len(temp) > 0:
            return float(temp)


def bleach_date(string):
    temp = ""
    string = str(string)
    for i in string:
        if i in ["1","2","3","4","5","6","7","8","9","0", ".", "/"]:
            temp += i
    if len(temp) > 0:
        return temp


def string_cleaner(string):
    return string.replace('\n', '').replace('\t', '').strip()
# Use on numerics: 'rating', 'raters', 'abv', 'ibu', 'total_checkins', 'unique_checkins', 'monthly_checkins', 'total_brewery_checkins', 'unique_brewery_checkins', 'brewery_raters', 'brewery_rating', 'brewery_num_beers',

## I think I'm gonna impute missing IBU data to 0, but I'm not sure if that's the best solution






### DATETIME

###Date Added: let's convert it to a datetime object
# Looks to be zero-padded, so I think it can be first bleached and then converted on this format:

def get_datetime(dataframe):
    dataframe['date'] = dataframe['date_added'].apply(lambda x: datetime.strptime(bleach_date(x), "%d/%m/%y"))
    dataframe['brewery_date'] = dataframe['date_brewery_added'].apply(lambda x: datetime.strptime(bleach_date(x), "%d/%m/%y"))
    return dataframe[['date', 'brewery_date']].values

# print(datetime.strptime(bleach_date('listen up!!!! its 12/12/12!!!!'), "%d/%m/%y"))

# print(pd.to_datetime(str(bleach('this beer added on 10/04/15')), format='%m%d%y'))







### TEXT Data

def has_description(dataframe):
    dataframe['description_present'] = dataframe['description'].apply(lambda x: 1 if x is not None else 0)
    dataframe['brewery_description_present'] = dataframe['brewery_description'].apply(lambda x: 1 if x is not None else 0)
    return dataframe[['description_present', 'brewery_description_present']].values

def length_description(dataframe):
    dataframe['wordcount'] = dataframe['description'].apply(lambda x: len(x) if x is not None else 0)
    dataframe['brewery_wordcount'] = dataframe['brewery_description'].apply(lambda x: len(x) if x is not None else 0)
    return dataframe[['wordcount', 'brewery_wordcount']].values








### BOOLEANS
def get_oop(dataframe):
    return dataframe['oop'].values.reshape(-1, 1)

def get_account_status(dataframe):
    dataframe['official_account'] = dataframe['brewery_account_status'].apply(lambda x: 1 if x == 'Official' else 0)
    return dataframe['official_account'].values

def get_subsidiary(dataframe):
    dataframe['is_subsidiary'] = dataframe['subsidiary_id'].apply(lambda x: 1 if x is not None else 0)






## CATEGORICAL
### COLUMNS: styles, brewery type
# Style ought to be categorical, maybe create umbrellas for edge cases or large categories





### LOCATION DATA
### could break down into dummies by country, state, etc

def get_in_usa(dataframe):
    dataframe['in_usa'] = dataframe['brewery_location'].apply(lambda x: 1 if 'United States' in x else 0)




