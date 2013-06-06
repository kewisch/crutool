# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Portions Copyright (C) Philipp Kewisch, 2013

from .resource import Resource

class JIRAApi(Resource):
  def __init__(self, baseUri, username, password, ca_certs=None):
    self.baseUri = baseUri
    super(JIRAApi, self).__init__(username, password, ca_certs)

  def request(self, uri, *args, **kwargs):
    uri = self.baseUri + uri

    if not 'params' in kwargs:
        kwargs['params'] = {}
    kwargs['params']['os_authType'] = "basic"

    return super(JIRAApi, self).request(uri, *args, **kwargs)

  def getTransitions(self, issue):
    return self.get("/issue/%s/transitions" % issue)

  def transitionIssue(self, issue, transId, fields=None, update=None):
    body = {
      "transition": transId
    }

    if fields:
      body["fields"] = fields
    if update:
      body["update"] = update

    self.post("/issue/%s/transitions" % issue, body=body)

  def issueInfo(self, issue):
    return self.get("/issue/%s" % issue);
