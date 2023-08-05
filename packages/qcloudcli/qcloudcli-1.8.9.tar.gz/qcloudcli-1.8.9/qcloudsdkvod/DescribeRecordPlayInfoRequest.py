#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribeRecordPlayInfoRequest(Request):

	def __init__(self):
		Request.__init__(self, 'vod', 'qcloudcliV1', 'DescribeRecordPlayInfo', 'vod.api.qcloud.com')

	def get_vid(self):
		return self.get_params().get('vid')

	def set_vid(self, vid):
		self.add_param('vid', vid)

	def get_notifyUrl(self):
		return self.get_params().get('notifyUrl')

	def set_notifyUrl(self, notifyUrl):
		self.add_param('notifyUrl', notifyUrl)

