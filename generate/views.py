from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from urllib import request as pyrequest
from urllib.parse import quote, urlencode
import string
import json
import jieba


def generate_verse(request):
    """
    Generate a verse with specific keyword
    :param request: HTTP request
    :return:
    """
    keyword = request.GET.get('keyword')
    num_sentence = request.GET.get('num_sentence')
    target_length = request.GET.get('target_length')
    rhyme_mode = request.GET.get('rhyme_mode')
    rhyme_style_id = request.GET.get('rhyme_style_id')

    # generate first sentence from given keyword
    post_data = urlencode({'keyword': keyword}).encode('utf-8')
    rst = pyrequest.urlopen(settings.FS_GENERATE_API, post_data)
    rst = rst.read().decode('utf-8')
    rst = json.loads(rst)
    if rst['result']:  # TODO: call crawler if first sentence generation failed
        keyword = rst['sentence']

    post_data = urlencode({
        'text': keyword,
        'num_sentence': num_sentence,
        'target_length': target_length,
        'rhyme_mode': rhyme_mode,
        'rhyme_style_id': rhyme_style_id,
    }).encode('utf-8')
    rst = pyrequest.urlopen(settings.TF_VERSE_GENERATE_API, post_data)
    return HttpResponse(rst.read().decode('utf-8'), content_type="application/json")


def generate_first_sentence(request):
    keyword = request.GET.get('keyword')

    # generate first sentence from given keyword
    post_data = urlencode({'keyword': keyword}).encode('utf-8')
    rst = pyrequest.urlopen(settings.FS_GENERATE_API, post_data)
    rst = rst.read().decode('utf-8')
    rst = json.loads(rst)
    if rst['result']:  # TODO: call crawler if first sentence generation failed
        rst['sentence'] = list(jieba.cut(rst['sentence'], cut_all=False))
    return JsonResponse(rst)
