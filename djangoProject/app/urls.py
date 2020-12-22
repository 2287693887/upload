#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :urls.py
# @Time      :2020/12/21 15:31
# @Author    :Venn

from django.conf.urls import url
from app import views

urlpatterns = [
    url('upload/', views.UploadPicture.as_view()),
]
