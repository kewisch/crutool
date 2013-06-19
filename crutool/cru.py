# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Portions Copyright (C) Philipp Kewisch, 2013

from .resource import Resource
from .config import config
import os
import getpass
import datetime

from . import utils

class CRUApi(Resource):
  def __init__(self, baseUri, username, password, ca_certs=None):
    self.baseUri = baseUri
    super(CRUApi, self).__init__(username, password, ca_certs)

  def request(self, uri, *args, **kwargs):
    uri = self.baseUri + uri
    return super(CRUApi, self).request(uri, *args, **kwargs)

  def setReviewStatus(self, cr, status):
    params = { "action": "action:%sReview" % status }
    return self.post("/reviews-v1/%s/transition" % cr, params=params)
   
  def reviewForIssue(self, issue):
    # TODO reviewsForIssue doesn't work with the bare issue mentioned
    params = { "term": issue, "maxReturn": 20 }
    data = self.get("/search-v1/reviews", params=params)
    reviews = data["reviewData"]
    if len(reviews):
      for rev in reviews:
        if issue in rev["name"]:
          return  rev["permaId"]["id"]
    return None

  def getTransitions(self, cr):
    return self.get("/reviews-v1/%s/transitions" % cr)

  def reviewInfo(self, cr, details=False):
    return self.get("/reviews-v1/%s%s" % (cr,"/details" if details else ""))

  def commitInfo(self, repo, revision):
    # This one uses the fisheye frontend!
    try:
      info = self.get("-fe/revisionData-v1/changeset/%s/%s" % (repo, revision))
      return info
    except:
      return None

  def createReview(self, project, issue, repo, name, csets):
    user = os.getenv("CRU_USER") or config.get('defaults', 'cru_user', getpass.getuser())
    dueDate = utils.isonow(datetime.timedelta(3))
    createDate = utils.isonow()
    revisions = []

    for cset in csets:
      ci = self.commitInfo(repo, cset)
      comment = ci["comment"] if ci else name
      revisions.append("{cs:id=%s|rep=%s}: %s" % (cset, repo, comment))
                       
    userObj = { "userName": user }
    obj = {
      "reviewData": {
        "author": userObj,
        "creator": userObj,
        "moderator": userObj,
        "description": "\n".join(revisions),
        "dueDate": dueDate,
        "projectKey": project,
        "name": name,
        "state": "Review",
        "type": "REVIEW",
        "allowReviewersToJoin" : True,
        "jiraIssueKey": issue,
      },
      "changesets": {
        "changesetData": [ { "id": c } for c in csets ],
        "repository": repo
      }
    }

    return self.post("/reviews-v1", body=obj)

  def addChangeset(self, cr, repo, csets):
    obj = {
      "repository": repo,
      "changesets": {
        "changesetData": [ { "id": c } for c in csets ]
      }
    }

    return self.post("/reviews-v1/%s/addChangeset" % cr,body=obj)
