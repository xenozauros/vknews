from django.conf.urls import patterns, include, url

#from django.contrib import admin
#admin.autodiscover()

# noinspection PyPep8
urlpatterns = patterns('',
                       (r'^$', 'news.views.show_initial_form'),
                       url(r'^logout/$', 'news.views.logout'),
                       url(r'^ajax/ajax_news_by_city/$', 'news.views.ajax_news_by_city'),
                       url(r'^ajax/citysearch/$', 'news.views.ajax_city_search'),
                       url(r'^ajax/erasespam/$', 'news.views.ajax_erase_spam'),
                       url(r'', include('social_auth.urls')),
)

#handler500 = 'news.views.redirect_500_error'