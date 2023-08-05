#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class GetUserTempTokenRequest(Request):

	def __init__(self):
		Request.__init__(self, 'market', 'qcloudcliV1', 'GetUserTempToken', 'market.api.qcloud.com')

	def get_orderId(self):
		return self.get_params().get('orderId')

	def set_orderId(self, orderId):
		self.add_param('orderId', orderId)

	def get_duration(self):
		return self.get_params().get('duration')

	def set_duration(self, duration):
		self.add_param('duration', duration)

