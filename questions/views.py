# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
import time
import numpy as np

def get_questions(request):
    context = {}
    #get current date
    today = datetime.date.today()
    #convert current date to unix timestamp
    todayTimeStamp = int(time.mktime(datetime.datetime.strptime(str(today), "%Y-%m-%d").timetuple()))
    #get the date from 2 days ago
    nDaysago = today - datetime.timedelta(days=2)
    # conver the 2 days ago date to unix timestamp
    nDaysTimeStamp = int(time.mktime(datetime.datetime.strptime(str(nDaysago), "%Y-%m-%d").timetuple()))
    dataList = []
    
    # counters
    number_of_questions = 0
    number_of_answered_questions = 0
    average_number_of_views = []
    average_number_of_answers = []

    url = "https://api.stackexchange.com/2.2/questions" 
    params = {  
        'fromdate':nDaysTimeStamp,
         #'todate':todayTimeStamp,
        'pagesize':'100',
        'order':'desc',
        'tagged':'python',
        'site':'stackoverflow',
        'sort':'creation',
        
    }
    r = requests.get(url, params=params)
    print r.url
    data = r.json()

    
    # create list of question objects 
    for item in data['items']:
        dataList.append({
            'owner': item['owner']['display_name'],
            'title': item['title'],
            'creation_date': datetime.datetime.fromtimestamp(float(item['creation_date'])),
            'is_answered': item['is_answered'], # (yes / no)
            'view_count': item['view_count'],
            'score':item['score'],
            'link':item['link'],
            'answer_count':item['answer_count']
        })
        if item['question_id']:
            number_of_questions+=1
        
        if item['is_answered'] == True:
            number_of_answered_questions+=1
        average_number_of_views.append(item['view_count'])
        average_number_of_answers.append(item['answer_count'])

        
    #get average number of views and answers using numpy library
    
    context['average_number_of_answers'] = int(np.mean(average_number_of_answers))
    context['average_number_of_views'] = int(np.mean(average_number_of_views))

    context['number_of_questions'] = number_of_questions
    context['number_of_answered_questions'] = number_of_answered_questions
    template = 'questions/questions_list.html'
    context['fromDate'] = nDaysago
    context['today'] = today
    context['data'] = dataList
    return render(request,template,context)