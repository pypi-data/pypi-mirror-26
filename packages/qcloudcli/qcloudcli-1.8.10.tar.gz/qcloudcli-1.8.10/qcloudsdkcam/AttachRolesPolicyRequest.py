#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class AttachRolesPolicyRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cam', 'qcloudcliV1', 'AttachRolesPolicy', 'cam.api.qcloud.com')

