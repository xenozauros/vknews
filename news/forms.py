# -*- coding: utf-8 -*-
from django import forms


class FeedbackForm(forms.Form):
    cityText = forms.CharField(widget=forms.TextInput(attrs={'size': 38}), label='', max_length=100,
                               initial=u'Санкт-Петербург')
    searchString = forms.CharField(widget=forms.TextInput(attrs={'size': 38}), label='', max_length=100,
                                   initial='Сдам квартиру')
    cityID = forms.CharField(widget=forms.HiddenInput, initial=u'2')
    startFrom = forms.CharField(widget=forms.HiddenInput, initial=u'0')     
