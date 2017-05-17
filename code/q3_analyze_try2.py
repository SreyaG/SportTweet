import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
from textblob import TextBlob
import matplotlib.cm as cm
import operator as o
from mpl_toolkits.basemap import Basemap

datafile=['try2','partsaa','partsab','partsac']
#datafile=['try2']
tweets_data = []
for tweets_data_path in datafile:
    #tweets_data_path = 'try2'
    tweets_file = open(tweets_data_path, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        except:
            continue

print (len(tweets_data))
tweets = pd.DataFrame()

#sentiment analysis
def clean_tweet(tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())

def get_tweet_sentiment(tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'


tweets['text'] = [tweet.get('text','') for tweet in tweets_data]
tweets['created_at'] = [tweet.get('created_at','') for tweet in tweets_data]

tweets['lang'] = [tweet.get('lang','') for tweet in tweets_data]
tweets['country'] = [tweet['place']['country'] if "place" in tweet and tweet['place']
                      else np.nan for tweet in tweets_data]

tweets['lat']=[tweet["geo"]["coordinates"][1] if "geo" in tweet and tweet['geo']
                      else np.nan for tweet in tweets_data]
tweets['long'] = [tweet["geo"]["coordinates"][0] if "geo" in tweet and tweet['geo']
                      else np.nan for tweet in tweets_data]
tweets['sentiment'] = [get_tweet_sentiment(tweet.get('text','')) for tweet in tweets_data]



tweets_by_lang = tweets['lang'].value_counts()
tweets_by_country = tweets['country'].value_counts()
tweets_by_cordinates=tweets['lat'].value_counts()
#tweets_by_created_at=tweets['time'].value_counts()


fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=10)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Languages', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=10)
ax.set_title('Top 5 languages', fontsize=10, fontweight='bold')
tweets_by_lang[:5].plot(ax=ax, kind='bar', color='red')

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=10)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Country', fontsize=10)
ax.set_ylabel('Number of tweets' , fontsize=10)
ax.set_title('Top 5 countries', fontsize=10, fontweight='bold')
tweets_by_country[:5].plot(ax=ax, kind='bar', color='red')
fig.savefig('by_country.png')







#search for words
def word_in_text(wordcorpus, text):
    for word in wordcorpus:
        word = word.lower()
        text = text.lower()
        match = re.search(word, text)
        if match:
            return True
    return False
def partofday(time):
        for t in time[11:13]:
            t=int(str(time[11:13]))
        #if (t==05 or (t==12 or (t==06 or (t==07 or (t==08 or (t==09 or (t==10 or t==11))))))) :
            if t >=5 and t <=12 :
                return 'morning'
            elif t>12 and t <=17:
                return 'afternoon'
            else:
                return 'night'



femaleplayers=['Maria Sharapova','Ronda Rousey','Lindsey Vonn','Danica Patrick','Sania Mirza', 'Angeiszka Radwanska',\
                         'Carolina Wozniacki','Jessica Ennis-Hill','Simone Biles','Garbine Muguruza','Genzebe Dibaba','Ana Ivanovic','Victoria Azarnacka','Alex Morgan']
maleplayers=[ 'Cristiano Ronaldo','Lionel Messi','Micheal Phelps','Chris Froome','LeBron James','Roger Federer','James Anderson',\
                         'Mo Farrah','Kevin Durant','Novak Djokovic','Dustin Johnson','Usain Bolt','Virat Kohli',\
                         '	Cam Newton','	Phil Mickelson','	Jordan Spieth','Kobe Bryant']
tweets['female'] = tweets['text'].apply(lambda tweet: word_in_text(femaleplayers, tweet))
tweets['male'] = tweets['text'].apply(lambda tweet: word_in_text(maleplayers, tweet))
tweets['time'] = tweets['created_at'].apply(lambda tweet: partofday(tweet))

tweets_by_country = tweets['country'].value_counts()
tweets_by_country_female = tweets.groupby('female')['country'].value_counts()[True]
tweets_by_country_male = tweets.groupby('male')['country'].value_counts()[True]
tweets_by_time = tweets['time'].value_counts()

tweets_no_na=tweets[['lat','long','female']].copy()
tweets_no_na['female']= (tweets_no_na['female']).astype(int)
tf=tweets_no_na.groupby([tweets_no_na['lat'],tweets_no_na['long']])['female'].agg(['sum']).reset_index()

tweets_no_nam=tweets[['lat','long','male']].copy()
tweets_no_nam['male']= (tweets_no_nam['male']).astype(int)
tm=tweets_no_nam.groupby([tweets_no_nam['lat'],tweets_no_nam['long']])['male'].agg(['sum']).reset_index()          


print (tweets_by_country_female)
print (tweets_by_country_male)

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.tick_params(axis='x', labelsize=10)
ax1.tick_params(axis='y', labelsize=10)
ax1.set_xlabel('Countries', fontsize=10)
ax1.set_ylabel('Number of tweets' , fontsize=10)
ax1.set_title('Time', fontsize=10, fontweight='bold')
tweets_by_time.plot(ax=ax1, kind='bar', color='pink')




fig = plt.figure()
ax1 = fig.add_subplot(111)
ax2=fig.add_subplot(111)

ax1.tick_params(axis='x', labelsize=10)
ax1.tick_params(axis='y', labelsize=10)
ax1.set_xlabel('Countries', fontsize=10)
ax1.set_ylabel('Number of tweets for Female Athletes' , fontsize=10)
ax1.set_title('Top 10 countries', fontsize=10, fontweight='bold')
tweets_by_country_female[:10].plot(ax=ax1, kind='bar', color='blue')
plt.savefig('athletes by Female country.png')



ax2.tick_params(axis='x', labelsize=10)
ax2.tick_params(axis='y', labelsize=10)
ax2.set_xlabel('Countries', fontsize=10)
ax2.set_ylabel('Number of tweets for Male Athletes' , fontsize=10)
ax2.set_title('Top 10 countries', fontsize=10, fontweight='bold')
tweets_by_country_male[:10].plot(ax=ax2, kind='bar', color='green')
plt.savefig('athletes by Male country.png')
#%%
fig, ax = plt.subplots()
earth = Basemap(ax=ax,resolution = 'l', area_thresh = 1000.0,
              lat_0=0, lon_0=0)
earth.drawmapboundary(fill_color='lightblue')
earth.drawcountries(color='#556655', linewidth=0.9)
earth.drawcoastlines(color='#556655', linewidth=0.9)
earth.fillcontinents(color='lightgrey',zorder=1)
earth.drawmapboundary()
f=ax.scatter(tf['lat'],tf['long'],c=tf['sum']+1, marker='x',color='y',zorder=10)
m=ax.scatter(tm['lat'],tm['long'],c=tm['sum']+1,marker='o', color='b',zorder=5)
ax.set_xlabel("Tweets about Athletes")
ax.legend((f,m),('Female Athletes','Male Athletes'),scatterpoints=1,
           loc='lower left',
           ncol=3,
           fontsize=8)
fig.savefig('Map_athletes.png')
#%%
#sentiment data
tweets_by_sentiment = tweets['sentiment'].value_counts()
tweets_by_sentiment_female = tweets.groupby('female')['sentiment'].value_counts()[True]
tweets_by_sentiment_male = tweets.groupby('male')['sentiment'].value_counts()[True]

print (tweets_by_sentiment_female)
print (tweets_by_sentiment_male)
#%%
#pi chart

labels = ['Positive', 'Negative', 'Neutral']
den=tweets_by_sentiment_female.sum()/100.00
sizes = [tweets_by_sentiment_female['positive']/den,tweets_by_sentiment_female['negative']/den,tweets_by_sentiment_female['neutral']/den]
colors = ['lightgrey', 'gold', 'lightskyblue', 'lightcoral']
colors1 = ['lightpink', 'seagreen', 'lightblue']

explode = (0, 0.1, 0)  
plt.rcParams.update({'font.size': 12})
fig,ax1 = plt.subplots()
#ax1 = fig.add_subplot(131)
#ax2=fig.add_subplot(133)
#fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',colors=colors1,
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax1.set_title('Female Athletes')  
plt.show() 
fig.savefig('Pie_chart_female.png')


fig,ax2 = plt.subplots()

den=tweets_by_sentiment_male.sum()/100.00
sizes = [tweets_by_sentiment_male['positive']/den,tweets_by_sentiment_male['negative']/den,tweets_by_sentiment_male['neutral']/den]
ax2.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',colors=colors,shadow=True, startangle=90)
ax2.axis('equal') 
ax2.set_title('Male Athletes')       
plt.show()
fig.savefig('Pie_chart_male.png')

tweets_no_na=tweets[['sentiment','country','female']].copy().dropna()
tweets_no_na['female']= (tweets_no_na['female']).astype(int)
tf=tweets_no_na.groupby([tweets_no_na['country'],tweets_no_na['sentiment']])['female'].agg(['sum']).reset_index().dropna()

tweets_no_nam=tweets[['sentiment','country','male']].copy().dropna()
tweets_no_nam['male']= (tweets_no_nam['male']).astype(int)
tm=tweets_no_nam.groupby([tweets_no_nam['country'],tweets_no_nam['sentiment']])['male'].agg(['sum']).reset_index().dropna()

fig= plt.subplots()
tm=tm[tm['sum']!=0]
tm=tm.sort(['sum'], ascending=0)
x=(tm[:25])
sub_df = x.groupby(['country','sentiment'])['sum'].sum().unstack()
sub_df.plot(kind='bar',stacked=True, title='Male Athlete')
plt.show()
plt.savefig('Male_bar_stack.png')

fig= plt.subplots()
tf=tf[tf['sum']!=0]
tf=tf.sort(['sum'], ascending=0)
x=(tf[:25])
sub_df = x.groupby(['country','sentiment'])['sum'].sum().unstack()
sub_df.plot(kind='bar',stacked=True, title='Female Athlete')
plt.show()
plt.savefig('Female_bar_stack.png')

### time
#%%
tweets_timef=tweets[['sentiment','time','female']].copy().dropna()
tweets_timef['female']= (tweets_timef['female']).astype(int)
tf=tweets_timef.groupby([tweets_timef['time'],tweets_timef['sentiment']])['female'].agg(['sum']).reset_index().dropna()

tweets_timem=tweets[['sentiment','time','male']].copy().dropna()
tweets_timem['male']= (tweets_timem['male']).astype(int)
tm=tweets_timem.groupby([tweets_timem['time'],tweets_timem['sentiment']])['male'].agg(['sum']).reset_index().dropna()

fig= plt.figure()
tm=tm[tm['sum']!=0]
tm=tm.sort(['sum'], ascending=0)
x=(tm[:15])
sub_df = x.groupby(['time','sentiment'])['sum'].sum().unstack()
sub_df.plot(kind='bar',stacked=True, title='Male Athlete')
plt.show()
plt.savefig('Male_bar_stack_time.png')

fig= plt.figure()
tf=tf[tf['sum']!=0]
tf=tf.sort(['sum'], ascending=0)
x=(tf[:15])
sub_df = x.groupby(['time','sentiment'])['sum'].sum().unstack()
sub_df.plot(kind='bar',stacked=True, title='Female Athlete')
plt.show()
plt.savefig('Female_bar_stack_time.png')


###
#%%
tweets_timef=tweets[['time','country']].copy().dropna()
tf=tweets_timef.groupby([tweets_timef['country']])['time'].agg(['count']).reset_index().dropna()


fig= plt.figure()
tf=tf[tf['count']!=0]
x=(tf[:25])
sub_df = x.groupby(['country'])['count'].count().unstack()
sub_df.plot(kind='bar',stacked=True, title='Country')
plt.show()
plt.savefig('Country_bar_stack_time.png')




