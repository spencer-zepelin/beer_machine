## Project Elements
### Data Acquisition
All the data that I used in this project was scraped off of Untappd[LINK]. Every row in my dataset represents a single beer from Untappd's database and the summary data about that beer based on the aggregation of all user "check-ins" of that beer.

I used a combination of Requests and Beautiful to scrape the data. The scrapers iterated over the following URL:
```https://untappd.com/w/---/BEER_ID_NUMBER```
Every iteration interpolated the beer id number at the end of the URL as it looped over a range of numbers from 1 to 2,048,800. The result was a comprehensive collection of Untappd's beer pages as of April 17, 2017. New beers are being added all the time, and as such, new scraping would be necessary to keep the database totally up-to-date. 

Every page was redirected at least in part. The dashes in the URL were filled with the beer name that the number corresponded to. Frequently, the number itself redirected to another number entirely. As a result, the finished data contained a significant proportion of duplicate entries (almost 350,000 out of the nearly 2 million).

I chose to scrape every beer off of Untappd instead of selecting a random sample for two reasons: First, having all the data allows for more flexibility with subsetting and in no way precludes the possibility of random sampling for a smaller dataset. Second, I wanted to ensure that if someone was interested in a particular case--say Old Style, a hometown favorite here in Chicago--it would be present within my data and the model.

Once I had scraped all the beers, I scraped the brewery pages. Luckily, each beer's page contained a brewery id number. This number took the place of the beer id number as the suffix for the URL following nearly the same paradigm:
```https://untappd.com/w/---/BREWERY_ID_NUMBER```
Forunately, for this round of scraping I already had a list of all the brewery id numbers I needed within the beer data I just scraped. I created a list representing the set of all brewery id numbers present in my beer data. I then had my web scrapers loop over every index in this list to interpolate the brewery id and scrape the appropriate page.

The most salient element of this scraping protocol was the presence of the brewery id number in both the beer data and the brewery data. This allowed me to join the two tables using the brewery id number as the key. Naturally, I performed a one-to-many join since I wanted the data about a given brewery to be present in the row of every beer they made. 

### Data Cleaning and Transformation
Almost all of the data were in string format after being scraped. All of the numerical features had to be stripped of any extraneous characters and transformed into floats or integers. Datetime information was likewise stripped from strings. Even string data had extraneous formatting that had to be systematically cleaned. From there categorical variables were converted into useable dummy format as necessary. 

The most labor-intensive data transformation involved the beer style column. Both the ABV and IBU columns had substantial missing data, and I figured sufficient style information could serve as an effective stand-in in addition to providing other relevant features for the model. To achieve this, I hard-coded a taxonomy of beers, dividing the nearly 170 styles first into broad categories (ales, lagers, and others) and next into more specific subtypes and stylistic groupings.

### Target Operationalization
At the outset, operationalizing the target variable was fairly straightforward. The model was designed to predicted the rating of a beer as a float between 0.25 and 5.0. This information was readily gleaned from Untappd during data acquisition. Ultimately though, regression models were weighting too heavily towards the mean and overpredicting low-values while underpredicting high values. As such, a second target variable was created by binning beers into three score group: under 3.25, between 3.25 and 4.0, and above 4.0. 

### Modeling
A classification model was built to first predicted whether a beer belonged in the low, medium, or high groups. Based on the result, that beer was then passed along to a regressor trained on data from that stratum. 

For classification models, random forests, extra trees, and the XGBoost classifier proved most effective. Depth limitations were placed on all of the models to prevent overfitting and led to a reduction in variance and improved scores on cross-validation. XGBoost was also strongly l2 regularized (lambda=50) and lightly l1 regularized (alpha=0.01). I ended up synthesizing these three models with a soft-voting classifier. 

Throughout the classification process, I used two techniques to combat the data imbalance I experienced. First, I manipulated the thresholds of predicted class probabilities output by the models. This allowed me to selectively overpredict the tails at the cost of increased error for the central class. The other technique was to train my model on data composed equally of all three classes. Eventually, I was able to acheive near 0.70 recall for all three classes.

XGBoost Regressors with depth limitations were used as the three regression models. 

### Results
The Mean Absolute Error on the holdout test data was 0.18. The median of the distribution of absolute errors was 0.133 indicating that at least half of our predictions are less than 0.15 away from the actual value, around 3% off over the range of the target variable. In this sense, the model is a success. Less than 0.5% of predictions were off by 1.0 or more.

### Next Steps
I would still like to wrap this model in a Django or Flask application to give users the opportunity to input potential beers and receive a predicted score. This potential use case was a principal element in the selection and design of this project. Once wrapped in an app, the input features may need to be pared back to facilitate use and interpretability. There is still room for additional feature engineering, particularly for descriptions of beers. I am also curious if restricting the dataset to a certain subset might also improve model quality.