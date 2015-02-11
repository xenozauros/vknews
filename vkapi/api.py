# -*- coding: utf-8 -*-
import urllib2
from urllib import urlencode


def call_api_vk(method, params):
    if isinstance(params, list):
        params_list = [kv for kv in params]
    elif isinstance(params, dict):
        params_list = params.items()
    else:
        params_list = [params]
    url = "https://api.vk.com/method/%s?%s" % (method, urlencode(params_list))
    return urllib2.urlopen(url).read()    


def get_cities_vk(country, q):
    return call_api_vk("places.getCities", [("q", q), ("country", country)])


def get_news_vk(question, start_from, news_num):
    return call_api_vk("newsfeed.search", [("q", question), ("count", news_num), ("start_from", start_from),
                                           ("extended", 0), ("v", "5.20")])


def get_user_vk(uid):
    return call_api_vk("users.get", [("uids", uid), ("fields", "city,photo_100,photo_50")])