#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribeVpnGwRequest(Request):

	def __init__(self):
		Request.__init__(self, 'vpc', 'qcloudcliV1', 'DescribeVpnGw', 'vpc.api.qcloud.com')

	def get_vpcId(self):
		return self.get_params().get('vpcId')

	def set_vpcId(self, vpcId):
		self.add_param('vpcId', vpcId)

	def get_vpnGwId(self):
		return self.get_params().get('vpnGwId')

	def set_vpnGwId(self, vpnGwId):
		self.add_param('vpnGwId', vpnGwId)

	def get_vpnGwName(self):
		return self.get_params().get('vpnGwName')

	def set_vpnGwName(self, vpnGwName):
		self.add_param('vpnGwName', vpnGwName)

	def get_offset(self):
		return self.get_params().get('offset')

	def set_offset(self, offset):
		self.add_param('offset', offset)

	def get_limit(self):
		return self.get_params().get('limit')

	def set_limit(self, limit):
		self.add_param('limit', limit)

	def get_orderField(self):
		return self.get_params().get('orderField')

	def set_orderField(self, orderField):
		self.add_param('orderField', orderField)

	def get_orderDirection(self):
		return self.get_params().get('orderDirection')

	def set_orderDirection(self, orderDirection):
		self.add_param('orderDirection', orderDirection)

	def get_dealId(self):
		return self.get_params().get('dealId')

	def set_dealId(self, dealId):
		self.add_param('dealId', dealId)

	def get_vpnGwAddress(self):
		return self.get_params().get('vpnGwAddress')

	def set_vpnGwAddress(self, vpnGwAddress):
		self.add_param('vpnGwAddress', vpnGwAddress)

