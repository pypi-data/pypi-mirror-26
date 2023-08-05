#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class QueryProjectRequest(Request):

	def __init__(self):
		Request.__init__(self, 'helix', 'qcloudcliV1', 'QueryProject', 'helix.api.qcloud.com')

	def get_projectId(self):
		return self.get_params().get('projectId')

	def set_projectId(self, projectId):
		self.add_param('projectId', projectId)

