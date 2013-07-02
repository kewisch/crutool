# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Portions Copyright (C) Philipp Kewisch, 2013

from .utils import docstring_trim

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
