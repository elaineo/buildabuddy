import nltk
from collections import OrderedDict, defaultdict
import re
import requests
from bs4 import BeautifulSoup
from urlparse import urlparse

SLEEP_COMMAND = ' go to sleep'
WAKE_COMMAND = ' wake up'
QUIET_COMMAND = ' no reply'
LOUD_COMMAND = ' reply on'
ADMIN_ID = 21455761

def filter_tweet(tweet, userid, botname, friends=None):
    skip = False
    sleep = False
    wake = False
    debug = False
    end_debug = False

    # filter RTs
    if tweet.get('retweet_count') > 0:
        skip = True
    # only reply to target user
    sender = None
    """ tweets to reply to:
        if sender is owner and not a reply
        if sender if owner's friend and mentions my name
    """
    try:
        sender = tweet.get('user').get('id')
        if sender not in [userid, ADMIN_ID] + friends:
            skip = True
    except:
        sender = None
        skip = True

    t = tweet.get('text')
    if not t:
        skip = True
    else:
        t = t.lower()
        if t[:3] == "rt ":
            skip = True
        if sender in [userid, ADMIN_ID]:
            if SLEEP_COMMAND in t:
                sleep = True
            elif WAKE_COMMAND in t:
                wake = True
            if QUIET_COMMAND in t:
                debug = True
            elif LOUD_COMMAND in t:
                end_debug = True
            if tweet.get('in_reply_to_status_id') and botname not in t:
                skip = True
            if t[0] == "@" and botname not in t:
                skip = True
        elif botname not in t:
            skip = True
        elif tweet.get('in_reply_to_status_id'):
            skip = True
    return skip, sleep, wake, debug, end_debug

def word_count(sentence, words):
    s = nltk.word_tokenize(sentence)
    return len(set(s) & set(words))

def ok_tweet(c, minlen, maxlen):
    if c.endswith(':') or c.endswith(','):
        return False
    if len(c) > maxlen or len(c) < minlen:
        return False
    else:
        return True


GARBAGE = [",", "--", "\'s", ".", "``","n\'t","\'\'",")","(","%","!","\'","?","percent",":"]


# semantic tools
def remove_stopwords(documents, sents=False):
    texts = []
    for d in documents:
        if sents:
            doc = d #d[0]+d[1]
        else:
            doc = documents[d]
        doc = clean_str(doc)
        tokens = nltk.word_tokenize(doc.lower())
        tokens = [t for t in tokens if t not in nltk.corpus.stopwords.words('english')]
        tokens = [t for t in tokens if t not in GARBAGE]
        texts.append(tokens)
    return texts


def clean_str(text):
    # remove words that start with @
    # remove urls
    y = " ".join(filter(lambda x:(x[0]!='@' and x[:4]!='http'), text.split()))
    return re.sub('[#$*|]', '', y)

def remove_infreq(inputs, minfreq):
    frequency = defaultdict(int)
    for text in inputs:
        for token in text:
            frequency[token] += 1
    texts = [[token for token in text if frequency[token] > minfreq]
             for text in inputs]
    return texts

NEWS_DOMAINS = "thenewyorktimes moneybeat"

""" deal with urls in tweets """
def pull_headlines(tweet):
    ent = tweet.get('entities')
    urls = ent.get('urls')
    t = ""
    if urls:
        for u in urls:
            try:
                url = u.get('expanded_url')
                r = requests.get(url)
                headlines = BeautifulSoup(r.content).find('title')
                if not headlines:
                    headlines = BeautifulSoup(r.content).find('h1')
                # remove domain
                domain = '{uri.netloc}'.format(uri=urlparse(url)) + NEWS_DOMAINS
                hwords = [h for h in headlines.getText().split() if h.lower() not in domain]

                t = "%s %s" % (t,' '.join(hwords))
            except:
                continue

    # also pull quoted tweets
    if tweet.get('is_quote_status'):
        try:
            quote = tweet.get('quoted_status').get('text')
        except:
            quote = ''
        t+=quote
    return t


""" break and chunk tweets """

def send_frag(api, tweet, id_str, name=None):
    if name:
        twit = api.request('statuses/update', {'status': "@%s %s" % (name, tweet), 'in_reply_to_status_id': id_str})
    else:
        twit = api.request('statuses/update', {'status': tweet, 'in_reply_to_status_id': id_str})
    return twit.response.json()

def send_tweet(api, tweet, id_0, name=None):
    # if too long, break it up
    id_str = id_0
    r = send_frag(api, tweet, id_str, name)

    if r.get('errors'):
        maxlen = 138 - name
        rtweets = break_tweet(rtweet,maxlen)
        for rt in rtweets:
            print rt
            rt_resp = send_frag(api, rt, id_str, name)
            if rt_resp.get('errors'):
                continue
            else:
                id_str = rt_resp.get('id_str')

def chunks(l, n):
    """Yield successive n-sized chunks from l.
        Chunks prioritize commas. after that, spaces
    """
    q = []
    total = 0
    remainder = l
    while len(remainder) > 0:
        if len(remainder) <= n:
            q.append(remainder[:idx])
            break

        x = remainder[:n]
        idx = x.rfind(',')
        if idx > 0:
            if idx > 50:
                q.append(remainder[:idx+1])
                remainder = remainder[idx+1:]
                continue
        idx = x.rfind(' ')
        q.append(remainder[:idx])
        remainder = remainder[idx+1:]

    #for i in xrange(0, len(l), n):
        # yield l[i:i+n]
    return q

def break_tweet(tweet, n):
    # first break into sentences
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    rtweets = sent_detector.tokenize(tweet.strip())
    for idx, rt in enumerate(rtweets):
        if len(rt) > n:
            clauses = rt.split('\n')
            for cdx, c in enumerate(clauses):
                d = '?'
                commas = [e+d for e in c.split(d) if e != '']
                commas[-1] = commas[-1][:-1]
                clauses[cdx:cdx+len(commas)] = commas
            rtweets[idx:idx+len(clauses)] = clauses
    for idx, rt in enumerate(rtweets):
        if len(rt) > n:
            chunkt = chunks(rt, n)
            rtweets[idx:idx+len(chunkt)] = chunkt
    return rtweets

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

import re
import random
def create_tweet(text, username):
    """ create a tweet from mult long sentences
        This process will vary by user.
     """
    # up to 2 tweets
    #maxlen = 263-2*len(username)
    maxlen = 139-len(username)
    for t in text:
        if ok_tweet(t, 40, maxlen):
            return t
    # go through again and break them up
        else:
            sents = sent_detector.tokenize(t)
            for s in sents:
                if ok_tweet(s, 40, maxlen):
                    return s
    return None


## for big corpuses
# username = 'elaine'
# class MyCorpus(object):
#     def __iter__(self):
#         for line in open('data/%s-corpus.mm' % username):
#             # assume there's one document per line, tokens separated by whitespace
#             yield dictionary.doc2bow(line.lower().split())

#corpus_memory_friendly = MyCorpus(username)
#dictionary = corpora.Dictionary(line.lower().split() for line in open('mycorpus.txt'))

# client = AppClient(CONSUMER_KEY, CONSUMER_SECRET)
# access_token = client.get_access_token()
