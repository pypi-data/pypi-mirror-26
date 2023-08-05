#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class MigrateNetworkInterfaceRequest(Request):

	def __init__(self):
		Request.__init__(self, 'vpc', 'qcloudcliV1', 'MigrateNetworkInterface', 'vpc.api.qcloud.com')

	def get_vpcId(self):
		return self.get_params().get('vpcId')

	def set_vpcId(self, vpcId):
		self.add_param('vpcId', vpcId)

	def get_networkInterfaceId(self):
		return self.get_params().get('networkInterfaceId')

	def set_networkInterfaceId(self, networkInterfaceId):
		self.add_param('networkInterfaceId', networkInterfaceId)

	def get_oldInstanceId(self):
		return self.get_params().get('oldInstanceId')

	def set_oldInstanceId(self, oldInstanceId):
		self.add_param('oldInstanceId', oldInstanceId)

	def get_newInstanceId(self):
		return self.get_params().get('newInstanceId')

	def set_newInstanceId(self, newInstanceId):
		self.add_param('newInstanceId', newInstanceId)

