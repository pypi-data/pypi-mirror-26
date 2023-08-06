#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DeleteLVBChannelRequest(Request):

	def __init__(self):
		Request.__init__(self, 'live', 'qcloudcliV1', 'DeleteLVBChannel', 'live.api.qcloud.com')

	def get_channelIds(self):
		return self.get_params().get('channelIds')

	def set_channelIds(self, channelIds):
		self.add_param('channelIds', channelIds)

