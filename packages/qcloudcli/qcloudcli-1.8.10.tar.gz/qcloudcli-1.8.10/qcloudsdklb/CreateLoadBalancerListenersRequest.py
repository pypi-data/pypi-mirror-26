#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class CreateLoadBalancerListenersRequest(Request):

	def __init__(self):
		Request.__init__(self, 'lb', 'qcloudcliV1', 'CreateLoadBalancerListeners', 'lb.api.qcloud.com')

	def get_loadBalancerId(self):
		return self.get_params().get('loadBalancerId')

	def set_loadBalancerId(self, loadBalancerId):
		self.add_param('loadBalancerId', loadBalancerId)

	def get_listeners(self):
		return self.get_params().get('listeners')

	def set_listeners(self, listeners):
		self.add_param('listeners', listeners)

