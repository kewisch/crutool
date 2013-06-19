# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Portions Copyright (C) Philipp Kewisch, 2013

from urlparse import urlparse
from .exceptions import *
import socks
import httplib2
import base64
import urllib
import json
import os
from .config import config

class Resource(object):
  def __init__(self, username, password, ca_certs=None):
    self.username = username
    self.password = password
    self.ca_certs = ca_certs
    self.ssl_no_verify = config.get('defaults', 'ssl_no_verify', 'false') in ['true', '1', 't', 'True', 'TRUE']

  def _prepare(self, uri, kwargs):
    r = urlparse(uri)
    if r.scheme == "http":
      raise Exception("Refusing to send credentials over http")

    proxyKey = '%s_proxy' % r.scheme
    proxyUri = proxyKey in os.environ and os.environ[proxyKey] or None
    proxyInfo = None
    if proxyUri:
      r = urlparse(proxyUri)
      proxyInfo = httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP, r.hostname, r.port or 3128)

    http = httplib2.Http(ca_certs=self.ca_certs, proxy_info=proxyInfo, disable_ssl_certificate_validation=self.ssl_no_verify)

    if not 'headers' in kwargs:
      kwargs['headers'] = {}

    # We can't force auth through httplib2, do it manually
    auth = base64.encodestring(self.username + ":" + self.password)
    kwargs['headers']['Authorization'] = "Basic " + auth

    kwargs['headers']['Accept'] = 'application/json'
    if 'body' in kwargs:
      kwargs['headers']['Content-Type'] = 'application/json'
      kwargs['body'] = json.dumps(kwargs['body'])

    if 'params' in kwargs:
      uri = uri + '?' + urllib.urlencode(kwargs['params'])
      del kwargs['params']

    return http, uri

  def _postprocess(self, response, content):
    if response.status == 401 or response.status == 403:
      try: msg = response['x-seraph-loginreason']
      except: pass
      raise LoginFailedException(msg)

    if response.status / 100 != 2:
      raise Exception("Request unsuccessful: %s\n%s" % (response.status, content))

    if len(content):
      content = json.loads(content)
    if 'error' in content:
      raise 'API Error %s' % content['error']

    return content

  def request(self, uri, method, **kwargs):
    http, uri = self._prepare(uri, kwargs)
    response, content = http.request(uri, method, **kwargs)
    return self._postprocess(response, content)

  def get(self, uri, **kwargs):
    return self.request(uri, 'GET', **kwargs)

  def post(self, uri, **kwargs):
    return self.request(uri, 'POST', **kwargs)

  def put(self, uri, **kwargs):
    return self.request(uri, 'PUT', **kwargs)

  def delete(self, uri, **kwargs):
    return self.request(uri, 'DELETE', **kwargs)
