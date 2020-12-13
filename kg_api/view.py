# -*- coding: utf-8 -*-
# @Time    : 2020/4/14 17:15
# @Author  : ztwu4
# @Email   : ztwu4@iflytek.com
# @File    : view.py
# @Software: PyCharm
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from entity_ner import entity_ner

@csrf_exempt
def entityner(request):
    method = request.method
    if method == "POST":
        post_data = request.body
        data_dict = json.loads(post_data, strict=False)
        content = data_dict['content']
        result = entity_ner(content)
        return HttpResponse(json.dumps(result,ensure_ascii=False))

@csrf_exempt
def test(request):
    method = request.method
    if method == "GET":
        id = request.GET.get('id',default='01')
        print(id)
        return HttpResponse(json.dumps({"code":0,"message":id},ensure_ascii=False))