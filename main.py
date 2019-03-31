import tweepy
import logging
import config
import secrets
from functools import wraps
from flask import Flask, request, Response
from google.cloud import storage

app = Flask(__name__)

def requires_cron(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        cron = request.headers.get("X-Appengine-Cron")
        if not cron:
            return Response('This URL is protected.', 401)
        return f(*args, **kwargs)
    return decorated


class Tweeter:
    def tweet(self):
        self._init_storage_bucket()
        self._setup_api()
        self._read_counter_from_gcs()
        self._fetch_message_from_gcs()
        if self._message is not None:
            self._tweet_message()
            self._increment_counter()
            self._update_counter_to_gcs()
    
    def _init_storage_bucket(self):
        client = storage.Client()
        self._bucket = client.get_bucket(config.BUCKET)
    
    def _setup_api(self):
        auth = tweepy.OAuthHandler(secrets.API_KEY, secrets.API_SECRET) 
        auth.set_access_token(secrets.ACCESS_TOKEN, secrets.ACCESS_TOKEN_SECRET) 
        self._api = tweepy.API(auth) 

    def _read_counter_from_gcs(self):
        blob = self._bucket.get_blob(config.COUNTER)
        self._counter = int(blob.download_as_string())

    def _fetch_message_from_gcs(self):
        blob = self._bucket.get_blob(config.LEXICON)
        lexicon = blob.download_as_string().decode("utf-8").split("\n")
        if self._counter == len(lexicon):
            self._message = None
            logging.warning("The bot has reached the end of the lexicon and will not tweet anymore")
        else:
            self._message = "Jean-Michel {}".format(lexicon[self._counter])
    
    def _tweet_message(self):
        self._api.update_status(status=self._message)
        logging.info("The bot has tweeted \'{}\'".format(self._message))

    def _increment_counter(self):
        self._counter += 1

    def _update_counter_to_gcs(self):
        blob = self._bucket.get_blob(config.COUNTER)
        blob.upload_from_string('{}'.format(self._counter))
        logging.info("Tweet counter updated")


@app.route('/tweet')
@requires_cron
def tweet():
    try:
        t = Tweeter()
        t.tweet()
        resp = Response("Success", 200)
        logging.info("The bot has successfully tweeted")
    except Exception as e:
        resp = Response("Failed", 400)
        logging.error("The bot has failed to tweet (exception: {}".format(e))
    return resp


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
