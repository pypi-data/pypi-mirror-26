#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class TextKeywordsRequest(Request):

	def __init__(self):
		Request.__init__(self, 'wenzhi', 'qcloudcliV1', 'TextKeywords', 'wenzhi.api.qcloud.com')

	def get_title(self):
		return self.get_params().get('title')

	def set_title(self, title):
		self.add_param('title', title)

	def get_channel(self):
		return self.get_params().get('channel')

	def set_channel(self, channel):
		self.add_param('channel', channel)

	def get_content(self):
		return self.get_params().get('content')

	def set_content(self, content):
		self.add_param('content', content)

