Python Package for Twitter's Sentiment Analysis
===============================

version number: 0.0.2
author: Shekhar Jha

Overview
--------

A python package to analyse the tweets and extract meaning from the data, can be installed with pip.

Installing/Setup
--------------------

To install use pip:

    $ pip install twittersent


Or clone the repo:

    $ git clone https://github.com/ekchusis/twittersent.git
    $ python setup.py install


Get the tokens/keys by registering at [Twitter Api](https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens) and fill put the values of the following variables in `client.py` file

```python
consumer_key = None
consumer_secret = None
access_token_key = None
access_token_secret = None
```

Contributing
------------

TBD

Example
-------
A simple file that takes a list as an input

```python
from client import TwitterSent

import sys
sys.path.insert(0, '/Users/xanthate/twittersent/twittersent')

print("Enter the list of keywords separated by commas: ")

user_input_as_string = input()
user_input_as_list = user_input_as_string.split(',') #splits the input string on commas

user_input_as_list = [a for a in user_input_as_list]

print("Enter the total number of tweets on which the analysis is to be done: ")
input_total_number_of_tweets = int(input())

T = TwitterSent()
value = TwitterSent.calculate_sentiment(T, user_input_as_list, input_total_number_of_tweets)
TwitterSent.barplot(T, value)
```
