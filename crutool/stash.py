# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Portions Copyright (C) Philipp Kewisch, 2013

from .resource import Resource

class StashApi(Resource):
  def __init__(self, baseUri, username, password, ca_certs=None):
    self.baseUri = baseUri
    super(StashApi, self).__init__(username, password, ca_certs)

  def request(self, uri, *args, **kwargs):
    uri = self.baseUri + uri

    if not 'params' in kwargs:
        kwargs['params'] = {}
    kwargs['params']['os_authType'] = "basic"

    return super(StashApi, self).request(uri, *args, **kwargs)

  def projects(self):
    return self.get("/projects")

  def repos(self, project):
    return self.get("/projects/%s/repos" % project)

  def repoInfo(self, project, repo):
    return self.get("/projects/%s/repos/%s" % (project, repo))

  def pullrequests(self, project, repo):
    return self.get("/projects/%s/repos/%s/pull-requests" % (project, repo))

  def createPullrequest(self, title, description, fromId,
                        fromRepo, fromProject, toId, toRepo, toProject):
    pr = {
      'title': title,
      'description': description,
      'state': 'OPEN',
      'open': True,
      'closed': False,
      'fromRef': {
        'id': fromId,
        'repository': {
          'slug': fromRepo,
          'project': { 'key': fromProject.upper() }
        }
      },
      'toRef': {
        'id': toId,
        'repository': {
          'slug': toRepo,
          'project': { 'key': toProject.upper() }
        }
      }
    }
    return self.post("/projects/%s/repos/%s/pull-requests" % (toProject, toRepo), body=pr)
