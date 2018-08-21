from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from urllib import request as pyrequest
from urllib.parse import quote, urlencode
from urllib.error import HTTPError

import string
import json
import jieba
import time


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

    cnt = 0
    success = False
    while not success and cnt < settings.TF_VERSE_GENERATE_MAX_RETRY:
        post_data = urlencode({
            'text': keyword,
            'num_sentence': num_sentence,
            'target_length': target_length,
            'rhyme_mode': rhyme_mode,
            'rhyme_style_id': rhyme_style_id,
        }).encode('utf-8')
        try:
            rst = pyrequest.urlopen(settings.TF_VERSE_GENERATE_API, post_data)
            success = True
            return HttpResponse(rst.read().decode('utf-8'), content_type="application/json")
        except:
            cnt += 1
            print("Failed to call tf_flask ({} try, sleeping {} seconds)".format(
                cnt, settings.TF_VERSE_GENERATE_INTERVAL
            ))
            time.sleep(settings.TF_VERSE_GENERATE_INTERVAL)
    return HttpResponse(status=500)


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


def generate_next_sentence(request):
    if request.POST:
        sentence = request.POST.get('sentence')

        # TODO: call tf to generate next sentence
        return JsonResponse(["腿", "搁", "在", "办公桌", "上"], safe=False)
    else:
        return HttpResponse(status=405)
