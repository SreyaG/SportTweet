#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API
access_token = "368589545-hk1s3DMHjn8460ZnJOE2Lr4qCd3GEXl35s4iCUD4"
access_token_secret = "lPgiQeCtee8WIvKuUHgVg0Ifa6BbvkkD5eVa0Uh60akat"
consumer_key = "xF7p2JoAGc3uvE8CfqFVTKZNl"
consumer_secret = "XzV9H9YA7gRp9429yZalmyUys7FKRi92rhbS3kZE4jD7sXtEZt"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print (data)
        return True

    def on_error(self, status):
        print (status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    stream.filter(track=['Simone Biles','Serena Williams','Maria Sharapova','Ronda Rousey','Lindsey Vonn','Danica Patrick','Sania Mirza', 'Angeiszka Radwanska',\
                         'Carolina Wozniacki','Jessica Ennis-Hill','Garbine Muguruza','Genzebe Dibaba','Ana Ivanovic','Victoria Azarnacka','Alex Morgan',\
                         'Cristiano Ronaldo', 'Lionel Messi','Micheal Phelps','Chris Froome','LeBron James','Roger Federer','James Anderson',\
                         'Mo Farrah','Kevin Durant','Novak Djokovic','Dustin Johnson','Usain Bolt','Virat Kohli',\
                         '	Cam Newton','	Phil Mickelson','	Jordan Spieth','Kobe Bryant'])
   