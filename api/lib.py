import re

def is_valid_tweet(s: str):
    # Urls are parsed by client, tweet id is numeric only
    return s.isdigit()

def is_valid_username(s: str):
    # Urls are expected to be parsed by client, username is alphanumerica w underscore allowed
    return re.search(r'^[A-Za-z0-9_]+$', s) is not None
