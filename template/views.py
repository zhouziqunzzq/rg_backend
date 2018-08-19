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
from template.models import Template
# from template.models import Sentence
from template.models import Verse


def get_template(request, id):
    try:
        # template_id = int(request.GET.get('id'))
        template_id = id
        template_name = Template.objects.get(pk=template_id).name
        verse_list = list(Verse.objects.filter(template_id=template_id).values())
        # for index in range(len(verseList)):
        #     dict = verseList[index]
        #     dict['sentenceList'] = list(Sentence.objects.filter(verse_id=dict['id']).values())
        my_dict = {
            "template_name": template_name,
            "template_id": template_id,
            "verse_list": verse_list
        }
        return JsonResponse(my_dict, safe=False)
        # return JsonResponse(['love', 'money', 'sex'], safe=False)
    except ValueError as e:
        #
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


def get_templates(request):
    try:
        # template_name = Template.objects.get(pk=template_id).name

        template_list = list(Template.objects.all().values())
        for i in range(len(template_list)):
            mydict = template_list[i]
            verse_list = list(Verse.objects.filter(template_id=mydict['id']).values())
            # for index in range(len(verse_list)):
            #     dict = verse_list[index]
            #     dict['sentenceList'] = list(Sentence.objects.filter(verse_id=dict['id']).values())
            mydict['verse_list'] = verse_list

        return JsonResponse(template_list, safe=False)
        # return JsonResponse(['love', 'money', 'sex'], safe=False)
    except ValueError as e:
        #
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
