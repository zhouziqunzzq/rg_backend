from django.shortcuts import render
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
import json
import os
from expansion.models import Vocab
from expansion.models import CoOccurrence
from .crawler import Crawler
from .get_expand_words import load_word_dict, get_expand_words

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def generate_coOcurrence(request):
    try:
        str = request.GET.get('str')
        response = []
        try:
            str_id = Vocab.objects.get(word=str).id
        except:
            return JsonResponse(response, safe=False)

        mylist = CoOccurrence.objects.filter(word1_id=str_id)
        response = []
        for item in mylist:
            response.append(item.word2_id.word)

        return JsonResponse(response, safe=False)

    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


def generate_crawler(request):
    try:
        key_word = request.GET.get('str')
        num = int(request.GET.get('num'))
        my_crawler = Crawler(key_word, num)
        res = my_crawler.generate_list()
        # res.append(my_crawler.wordnum)
        return JsonResponse(res, safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


def generate_rhyme(request):
    try:
        key_word = request.GET.get('str')
        num = int(request.GET.get('num'))
        word_dict = load_word_dict(os.path.join(BASE_DIR, 'expansion', 'word_dict_c.json'))
        rst = get_expand_words(key_word, num, word_dict)
        return JsonResponse(rst, safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
