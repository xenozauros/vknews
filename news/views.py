# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse

from news.forms import FeedbackForm
from vkapi.api import get_cities_vk, get_news_vk, get_user_vk
from models import User, Spammers

import logging
import arrow
import simplejson as json
logger = logging.getLogger(__name__)


def redirect_500_error(request):
    return render_to_response('/static/news/html/500.html', {}, context_instance=RequestContext(request))


def show_initial_form(request):
    form = FeedbackForm()
    if request.user.is_authenticated():
        # firstly we check if user is created
        user_nick_name = str(request.user.username)
        if not User.objects.filter(user_id=user_nick_name).exists():
            local_user = User(user_id=user_nick_name)
            local_user.save()
        #We should get real user name and photo from VK.com
        user = get_user_vk(request.user.username)
        user = json.loads(user, encoding="utf-8")
        user_first_name = user['response'][0]['first_name'].encode("utf-8")
        user_last_name = user['response'][0]['last_name'].encode("utf-8")
        user_photo = str(user['response'][0]['photo_50'])
        context = {'form': form, 'user_nick_name': user_nick_name, 'user_first_name': user_first_name,
                   'user_last_name': user_last_name, 'user_photo': user_photo}

    else:
        context = {'form': form}

    return render_to_response('index.html', context, context_instance=RequestContext(request))


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def ajax_news_by_city(request):
    user_nick_name = 'guestUser'
    if request.method != 'POST':
        return HttpResponse(request.method + " method is not supported, use POST")
    else:
        in_city_id = request.POST['cityID']
        search_string = request.POST['searchString'].encode("utf-8")
        client_ip = get_client_ip(request)
        start_from = request.POST['startFrom']
        city_text = request.POST['cityText'].encode("utf-8")

    news_num = 10
    counter = 0
    total_reply = []
    news_reply = []
    saved_spammers = []

    news = get_news_vk(search_string, start_from, news_num)
    news = json.loads(news, encoding="utf-8")

    if request.user.is_authenticated():
            user_nick_name = str(request.user.username).encode("utf-8")
            saved_spammers = Spammers.objects.filter(user_id=user_nick_name).values_list('spammer_id', flat=True)

    log_string = client_ip + ' : ' + search_string + ' : ' + city_text  #Log first search request for analysis
    if start_from == "0":
        if request.user.is_authenticated():
            log_string += ' : ' + user_nick_name
            logger.debug(log_string)
        else:
            log_string += ' : guestUser'.encode("utf-8")
            logger.debug(log_string)

    for i in range(0, news_num):
        # Now we are cheking that user is not group (his ID must be positive)
        try:
            owner_id = news['response']['items'][i]['owner_id']
            if owner_id > 0 and str(owner_id) not in saved_spammers:
                # now we should get info about user and check his city
                user = get_user_vk(owner_id)
                user = json.loads(user, encoding="utf-8")
                if 'city' in user['response'][0] and user['response'][0]['city'] != '0' and int(
                        user['response'][0]['city']) == int(in_city_id):
                    counter += 1
                    news_text = news['response']['items'][i]['text']
                    news_text = news_text.replace('\n', '<br />')
                    news_link = 'http://vk.com/id' + str(owner_id) + '?w=wall' + str(
                        owner_id) + '_' + str(news['response']['items'][i]['id'])
                    photo_link = str(user['response'][0]['photo_100'])
                    news_time = arrow.get(news['response']['items'][i]['date'])
                    news_time = news_time.humanize(locale='ru_RU')
                    news_reply_text = {"counter": counter, "news_text": news_text, "news_link": news_link,
                                     "photo_link": photo_link, "news_time": news_time,
                                     "user_id": str(owner_id)}
                    news_reply.append(news_reply_text)
        except IndexError:
            return HttpResponse(u"Something happened. Please search again or later")
    strange_string = {"news": news_reply}
    total_reply.append(strange_string)
    next_from = str(news['response']['next_from'])
    news_reply = []
    news_reply_text = {"next_from": next_from}
    news_reply.append(news_reply_text)
    total_reply.append(news_reply_text)
    total_reply = json.dumps(total_reply, encoding="utf-8")
    return HttpResponse(total_reply)


def ajax_city_search(request):
    if request.method != 'POST':
        return HttpResponse(request.method + " method is not supported, use POST")
    else:
        in_city_text = request.POST['cityText']
        cities = get_cities_vk(1, in_city_text.encode("utf-8"))
        cities = json.loads(cities, encoding="utf-8")['response']
        cities_reply = []
        for city in cities:
            city_name = city['title']
            if city.get('region'):
                city_name = city_name + ', ' + city['region']
            if city.get('area'):
                city_name = city_name + ', ' + city['area']
            cities_reply_text = {"city": city_name, "cid": city['cid']}
            cities_reply.append(cities_reply_text)
        suggestion = json.dumps(cities_reply, encoding="utf-8")
        return HttpResponse(suggestion)


def ajax_erase_spam(request):
    if request.method != 'POST':
        return HttpResponse(request.method + " method is not supported, use POST")
    else:
        if request.user.is_authenticated():
            posted_spammers = request.POST.getlist('spammers[]')
            user_nick_name = str(request.user.username)
            saved_spammers = Spammers.objects.filter(user_id=user_nick_name).values_list('spammer_id', flat=True)
            saved_spammers = list(saved_spammers)
            uniq_spammers = []
            for spammer in posted_spammers:
                if spammer not in saved_spammers:
                    uniq_spammers.append(spammer)
            for spammer in uniq_spammers:
                save_spammer = Spammers(user_id=user_nick_name, spammer_id=spammer)
                save_spammer.save()
            response_string = u'Указанные вами авторы больше никогда не появятся в вашей выдаче'
        else:
            response_string = u'К сожалению, не могу сохранить настройки. Пожалуйста, авторизуйтесь'
    return HttpResponse(response_string)


from django.contrib.auth import logout as auth_logout


def logout(request):
    """Logs out user"""
    auth_logout(request)
    form = FeedbackForm()
    context = {'form': form}
    return render_to_response('index.html', context, context_instance=RequestContext(request))
