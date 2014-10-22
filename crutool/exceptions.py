# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Portions Copyright (C) Philipp Kewisch, 2013

import sys

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

class LoginFailedException(Exception):
  def __init__(self, reason):
    self.reason = reason

class UsageException(Exception):
  def __init__(self, method, message=None):
    self.method = method
    self.message = message

  def __str__(self):
    msg = "Error: " + self.message + "\n" if self.message else ""
    msg += docstring_trim(self.method.__doc__)
    return msg

class ConfigMissingException(Exception):
  def __init__(self, section, key):
    self.section = section
    self.key = key
  def __str__(self):
    return "Missing config value %s.%s, "  % (self.section, self.key) + \
           "please add this to your ~/.crutoolrc"
