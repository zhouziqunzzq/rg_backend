from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from urllib import request as pyrequest
from urllib.parse import quote
import string
import json


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

    # TODO: generate first sentence from given keyword
    url = settings.FS_GENERATE_API + "?keyword={}".format(keyword)
    url = quote(url, safe=string.printable)
    rst = pyrequest.urlopen(url)
    rst = rst.read().decode('utf-8')
    rst = json.loads(rst)
    # print(rst)
    if rst['result']:  # TODO: call crawler if first sentence generation failed
        keyword = rst['sentence']
    # print(keyword)

    url = settings.TF_VERSE_GENERATE_API + "?text={}&num_sentence={}&target_length={}&rhyme_mode={}&rhyme_style_id={}".format(
        keyword, num_sentence, target_length, rhyme_mode, rhyme_style_id
    )
    url = quote(url, safe=string.printable)
    rst = pyrequest.urlopen(url)
    return HttpResponse(rst.read().decode('utf-8'), content_type="application/json")
