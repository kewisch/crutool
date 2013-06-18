# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Portions Copyright (C) Philipp Kewisch, 2013

from .utils import *
from .config import *

import locale
import datetime
import dateutil.parser

class JSONDisplayer(object):
  @staticmethod
  def issue(obj, htmlLink=None):
    fields = obj["fields"]
    fields["htmlURL"] = htmlLink
    # Uncomment to edit template:
    #print json_pp(fields)
    print config.format("templates", "issue", fields)

  @staticmethod
  def jiraTransitions(obj):
    for trans in obj.itervalues():
      fields = []
      for field in trans["fields"]:
        if field["required"]:
          fields.append("\033[1m%s\033[0m" % field["id"])
        else:
          fields.append(field["id"])
      print "%s (%s)" % (trans["name"], ",".join(fields))

  @staticmethod
  def jiraDashboard(obj):
    # print json_pp(obj)
    for issue in obj["issues"]:
      if "fields" in issue and "summary" in issue["fields"]:
        print "%s - %s" % (issue["key"], issue["fields"]["summary"]["value"])
      else:
        print "%s" % issue["key"]

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

    # Replace versioned comments array with formatted comments
    cmtstr = ""
    for cmt in obj["versionedComments"]["comments"]:
      cmtstr += "Line %s: <initial comment and file not provided by API>\n" % cmt["toLineRange"]

      for r in cmt["replies"]:
        if r["draft"] or r["deleted"]: continue

        if r["defectRaised"]:
          cmtstr += "\033[31m[defect]\033[0m"

        cmtstr += "\033[34m%s\033[0m:" % r["user"]["displayName"]
        cmtstr += "\n"
        cmtstr += r["message"]
        cmtstr += "\n"
      if len(cmt["replies"]):
        cmtstr += "\n" 
    obj["fmt_versioned_comments"] = cmtstr.strip()

    # Uncomment to edit template:
    # print json_pp(obj)
    print config.format("templates", "review", obj)

  @staticmethod
  def pullRequest(obj):
    return config.format("templates", "pullrequest", obj)
    
