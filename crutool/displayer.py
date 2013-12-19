# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Portions Copyright (C) Philipp Kewisch, 2013

from .utils import *
from .config import *

import locale
import datetime
import dateutil.parser
from textwrap import TextWrapper

class JSONDisplayer(object):
  @staticmethod
  def issue(obj, htmlLink=None):
    fields = obj["fields"]
    fields["htmlURL"] = htmlLink
    # Uncomment to edit template:
    # print json_pp(fields)
    print config.format("templates", "issue", fields)

  @staticmethod
  def jiraTransitions(obj):
    for trans in obj["transitions"]:
      fields = []
      for name, field in trans["fields"].iteritems():
        if field["required"]:
          fields.append("\033[1m%s\033[0m" % name)
        else:
          fields.append(name)
      print "%s (%s)" % (trans["name"], ",".join(fields))

  @staticmethod
  def jiraDashboard(obj):
    # print json_pp(obj)
    for issue in obj["issues"]:
      print "%s - %s" % (issue["key"], issue["fields"]["summary"])

    total = int(obj["total"])
    maxres = int(obj["maxResults"])
    if total > maxres:
      print "... (%d more)" % (total - maxres)


  @staticmethod
  def cruReview(obj, htmlLink=None):
    obj["htmlURL"] = htmlLink

    # Replace reviewer array with formatted reviewers
    reviewers = []
    reviewers_color = []
    reviewers_completed_color = []
    reviewers_uncompleted_color = []
    for r in obj["reviewers"]["reviewer"]:
      reviewers.append(r["displayName"])
      if r["completed"]:
        name = "\033[32m%s\033[0m" % r["displayName"]
        reviewers_color.insert(0, name)
        reviewers_completed_color.append(name)
      else:
        name = "\033[31m%s\033[0m" % r["displayName"]
        reviewers_color.append(name)
        reviewers_uncompleted_color.append(name)
    obj["fmt_reviewers"] = ", ".join(reviewers)
    obj["fmt_reviewers_color"] = ", ".join(reviewers_color)
    obj["fmt_reviewers_uncompleted_color"] = ", ".join(reviewers_uncompleted_color)
    obj["fmt_reviewers_completed_color"] = ", ".join(reviewers_completed_color)


    # Replace dates with formatted dates
    def replaceFmtDate(field):
        fmt = locale.nl_langinfo(locale.D_T_FMT)
        dt = dateutil.parser.parse(obj[field])
        strtime = dt.strftime(fmt)
        obj["fmt_" + field] = strtime
        if dt < datetime.datetime.now(dt.tzinfo):
          obj["fmt_%s_color" % field] = "\033[32m%s\033[0m" % strtime
        else:
          obj["fmt_%s_color" % field] = "\033[31m%s\033[0m" % strtime
    for field in ["dueDate", "createDate"]: replaceFmtDate(field)

    # Replace general comments array with formatted comments
    cmtstr = ""
    for cmt in obj["generalComments"]["comments"]:
      if cmt["draft"] or cmt["deleted"]: continue

      if cmt["defectRaised"]:
        cmtstr += "\033[31m[defect]\033[0m"

      cmtstr += "\033[34m%s\033[0m:" % cmt["user"]["displayName"]
      cmtstr += "\n"
      cmtstr += cmt["message"]
      cmtstr += "\n\n"
    obj["fmt_general_comments"] = cmtstr.strip()

    def addComment(cmt):
      cmtstr = ""
      if cmt.get("draft", False) or cmt.get("deleted", False): return

      if cmt.get("defectRaised", False):
        cmtstr += "\033[31m[defect]\033[0m"

      cmtstr += "\033[34m%s\033[0m:" % cmt["user"]["displayName"]
      cmtstr += "\n"
      if "toLineRange" in cmt:
        cmtstr += "Line %s: " % cmt["toLineRange"]
      cmtstr += cmt["message"]
      return cmtstr

    # Replace versioned comments array with formatted comments
    cmtstr = ""
    wrapper = TextWrapper(initial_indent="    ", subsequent_indent="    ", width=120)
    for cmt in obj["versionedComments"]["comments"]:
      cmtstr += addComment(cmt) + "\n"

      for r in cmt["replies"]:
        cmtstr += wrapper.fill(addComment(r)) + "\n"

      cmtstr += "\n\n" 
    obj["fmt_versioned_comments"] = cmtstr.strip()

    # Uncomment to edit template:
    # print json_pp(obj)
    print config.format("templates", "review", obj)

  @staticmethod
  def pullRequest(obj):
    return config.format("templates", "pullrequest", obj)

  @staticmethod
  def stashProjects(obj, baseUri):
    for project in obj["values"]:
      print "{: >10} {: <30} {: <20}".format(project["key"], project["name"], baseUri + project['link']['url'])
    
  @staticmethod
  def stashRepos(obj):
    for repos in obj["values"]:
      print "{: <40} {}".format(repos["name"] + ":", repos["cloneUrl"])

  @staticmethod
  def stashPullrequests(obj, baseUri):
    # Uncomment to edit template:
    # print json_pp(obj)

    for pr in obj["values"]:
      reviewers = []
      reviewers_color = []
      reviewers_completed_color = []
      reviewers_uncompleted_color = []
      for r in pr["reviewers"]:
        if r["user"]["active"]:
          reviewers.append(r["user"]["displayName"])
          if r["approved"]:
            name = "\033[32m%s\033[0m" % r["user"]["displayName"]
            reviewers_completed_color.append(name)
            reviewers_color.append(name)
          else:
            name = "\033[31m%s\033[0m" % r["user"]["displayName"]
            reviewers_uncompleted_color.append(name)
            reviewers_color.append(name)
      pr["fmt_reviewers"] = ", ".join(reviewers)
      pr["fmt_reviewers_color"] = ", ".join(reviewers_color)
      pr["fmt_reviewers_uncompleted_color"] = ", ".join(reviewers_uncompleted_color)
      pr["fmt_reviewers_completed_color"] = ", ".join(reviewers_completed_color)
      pr["fmt_baseUri"] = baseUri

      print config.format("templates", "stashPullrequest", pr),"\n"
