#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribeCdbInstancesRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cdb', 'qcloudcliV1', 'DescribeCdbInstances', 'cdb.api.qcloud.com')

	def get_cdbInstanceIds(self):
		return self.get_params().get('cdbInstanceIds')

	def set_cdbInstanceIds(self, cdbInstanceIds):
		self.add_param('cdbInstanceIds', cdbInstanceIds)

	def get_cdbInstanceVips(self):
		return self.get_params().get('cdbInstanceVips')

	def set_cdbInstanceVips(self, cdbInstanceVips):
		self.add_param('cdbInstanceVips', cdbInstanceVips)

	def get_offset(self):
		return self.get_params().get('offset')

	def set_offset(self, offset):
		self.add_param('offset', offset)

	def get_limit(self):
		return self.get_params().get('limit')

	def set_limit(self, limit):
		self.add_param('limit', limit)

	def get_projectId(self):
		return self.get_params().get('projectId')

	def set_projectId(self, projectId):
		self.add_param('projectId', projectId)

	def get_vpcId(self):
		return self.get_params().get('vpcId')

	def set_vpcId(self, vpcId):
		self.add_param('vpcId', vpcId)

	def get_subnetId(self):
		return self.get_params().get('subnetId')

	def set_subnetId(self, subnetId):
		self.add_param('subnetId', subnetId)

	def get_status(self):
		return self.get_params().get('status')

	def set_status(self, status):
		self.add_param('status', status)

