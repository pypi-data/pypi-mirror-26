#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DeleteSecurityGroupRequest(Request):

	def __init__(self):
		Request.__init__(self, 'dfw', 'qcloudcliV1', 'DeleteSecurityGroup', 'dfw.api.qcloud.com')

	def get_sgId(self):
		return self.get_params().get('sgId')

	def set_sgId(self, sgId):
		self.add_param('sgId', sgId)

	def get_forced(self):
		return self.get_params().get('forced')

	def set_forced(self, forced):
		self.add_param('forced', forced)

