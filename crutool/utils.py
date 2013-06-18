# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Portions Copyright (C) Philipp Kewisch, 2013

import os
import sys
import json
import datetime

def json_pp(obj):
  return json.dumps(obj, sort_keys=True, indent=2, separators=(',', ': '))

def textOptions(kv):
  optprompt = []
  opts = {}
  for v,s in kv.iteritems():
    x = 0
    while s[x].lower() in opts: x += 1
    opts[s[x].lower()] = v

    s = s[:x] + ("(%s)" % s[x]) + s[x+1:]
    optprompt.append(s)

  return opts,", ".join(optprompt)

def dict_merge(a, b):
    if not isinstance(b, dict):
        return b
    for k, v in b.iteritems():
        if k in a and isinstance(a[k], dict):
                a[k] = dict_merge(a[k], v)
        else:
            a[k] = v
    return a


def isonow(delta=None):
  dtnow = datetime.datetime.now()
  utcnow = datetime.datetime.utcnow()

  if delta:
    dtnow += delta
    utcnow += delta

  delta = dtnow - utcnow
  hh,mm = divmod((delta.days * 86400 + delta.seconds + 30) // 60, 60)
  return "%s%+03d:%02d" % (dtnow.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3], hh, mm)


def gitroot(path):
  while not path == "/":
    if os.path.exists(os.path.join(path, ".git")):
      return path
    path = os.path.dirname(path)
  return None

def docstring_trim(docstring):
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxint
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxint:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return '\n'.join(trimmed)
