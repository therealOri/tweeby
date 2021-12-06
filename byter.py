import json
import tweepy
import time
import sqlite3
import random
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()




# Get keys and set up api
with open('config.json', 'r') as f:
    config = json.load(f)    
    auth = tweepy.OAuthHandler(config["API_KEY"], config["API_SECRET"])
    auth.set_access_token(config["ACCESS_TOKEN"], config["ACCESS_SECRET_TOKEN"])
    api = tweepy.API(auth, wait_on_rate_limit=True)



#----------------------Functions----------------------#

def tweet(msg):
    api.update_status(msg)
    print("Tweet sent! Refresh and Check your page!")




# Do not change or remove.
def banner():
    byte = """
          ██████╗ ██╗   ██╗████████╗███████╗██████╗ 
          ██╔══██╗╚██╗ ██╔╝╚══██╔══╝██╔════╝██╔══██╗
          ██████╔╝ ╚████╔╝    ██║   █████╗  ██████╔╝
          ██╔══██╗  ╚██╔╝     ██║   ██╔══╝  ██╔══██╗
          ██████╔╝   ██║      ██║   ███████╗██║  ██║
          ╚═════╝    ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝
                                          
Made by Ori#6338 | @therealOri_ | https://github.com/therealOri

                (Connected to Twitter)




            """
    p = print(byte)
    return p


def check_mentions(api, keywords, since_id):
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        time.sleep(1.5)
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            logger.info(f"Answering {tweet.user.screen_name}'s mention to Opt-Out.")

            if not tweet.favorited:
                api.create_favorite(tweet.id)
            else:
                pass

            # Do DB add stuff here
            database = sqlite3.connect('tweet_blacklist.db')
            c = database.cursor()
            c.execute(f"INSERT INTO blist VALUES ('{tweet.user.screen_name}')")
            database.commit()
            database.close()
            logger.info(f'{tweet.user.screen_name} has been added to the do not tweet list!')

            # Reply to user that mentoned me and generates the tweet
            api.update_status(
                status=f"@{tweet.user.screen_name}\n\nYou have successfully Opt out of being replied to! I will no longer reply to your tweets!",
                n_reply_to_status_id=tweet.id,
            )
    return new_since_id




def tag_reply(tag: str, num: int):
    hashtag = tag
    num_tweet = num

    #fetching tweets
    for tweet in tweepy.Cursor(api.search_tweets, q=f'{hashtag} -filter:retweets', lang='en', tweet_mode='extended').items(num_tweet):
        time.sleep(1.5)

        #---------------Functions---------------#
        def like():
            #if tweet.user.screen_name != 'oByteBot':
            if tbl(tweet.user.screen_name) == False: # False = Not in blacklist
                api.create_favorite(tweet.id)
                print(f'Liked tweet!  |  {tweet.id} from user {tweet.user.screen_name}')
                time.sleep(5)
            elif tbl(tweet.user.screen_name) == True:
                pass
            else:
                pass


        def reply():
            if tbl(tweet.user.screen_name) == False:
                message = f'Hello @{tweet.user.screen_name},\n\nThis is an automated reply! (No reply).\n\nI have detected that your tweet contains the hashtag "{tag}". If you are an artist and like to watermark your art, then please visit me on github! (Check my Bio). <3\n\nOpt-out? (Check my Bio)'
                api.update_status(status=message, in_reply_to_status_id=tweet.id)
                print(f'Replied to a tweet!  |  {tweet.id} from user {tweet.user.screen_name}')
                time.sleep(5)
            elif tbl(tweet.user.screen_name) == True:
                pass
            else:
                pass


        def retweet():
            if tbl(tweet.user.screen_name) == False:
                api.retweet(tweet.id)
                print(f"Retweeted a tweet!  |  {tweet.id}")
                time.sleep(5)
            elif tbl(tweet.user.screen_name) == True:
                pass
            else:
                pass



        def tbl(username):
            database = sqlite3.connect('tweet_blacklist.db')
            c = database.cursor()

            # Gets usernames list
            c.execute(f'SELECT username FROM blist')
            ldb = c.fetchall()
            ldb = str(ldb).replace("(", "").replace(",)", "").replace("'", "")
            blist = ldb.strip('][').split(', ')

            
            if not username in blist:
                name = False

            if username in blist:
                name = True

            return name

#---------------Functions End---------------#




        #---------------Code---------------#
        #if tweet.user.screen_name != 'oByteBot': #'oByteBot'
        if tbl(tweet.user.screen_name) == False:
            if not tweet.favorited:
                try:
                    #Like
                    like()
                except Exception as e:
                    break
                except StopIteration:
                    break
            else:
                pass


            if not tweet.in_reply_to_status_id:
                try:
                    #Reply
                    reply()
                except Exception as e:
                    break
                except StopIteration:
                    break
            else:
                pass

        elif tbl(tweet.user.screen_name) == True:
            pass
        else:
            raise error
        #---------------Code---------------#



def main():
    func_api = api
    since_id = 1
    since_id = check_mentions(func_api, ["opt-out"], since_id)

    time.sleep(3)

    tags = ["#ArtistOnTwitter", "#furryart", "#furryartist", "#digitalart", "#furrycommission"]
    tag = random.choice(tags)
    print(f'Now searching for: {tag}\n\n')
    tag_reply(tag, 1)


def debug():
    func_api = api
    since_id = 1

    since_id = check_mentions(func_api, ["opt-out"], since_id)
    time.sleep(3)
    tag_reply("#byte_uwu6969", 10)




if __name__ == '__main__':
    while True:
        #debug()
        os.system('clear||cls')
        banner()
        main()
        time.sleep(900)
