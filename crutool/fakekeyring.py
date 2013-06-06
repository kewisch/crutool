# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Portions Copyright (C) Philipp Kewisch, 2013

import getpass

print "'pip install keyring' to enhance your experience!"

def get_password(self, context, user):
  return getpass.getpass("[%s] %s's Password:" % (context, user))

def set_password(self, context, user, password):
  pass

def delete_password(self, context, user):
  pass
