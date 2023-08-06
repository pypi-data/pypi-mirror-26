# -*- mode: python; encoding: utf-8 -*-
#
# Copyright 2014 the Critic contributors, Opera Software ASA
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.  You may obtain a copy of
# the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations under
# the License.

import api

class Critic(object):
    def __init__(self, impl):
        self._impl = impl

    @property
    def session_type(self):
        return self._impl.session_type

    @property
    def effective_user(self):
        return self._impl.getEffectiveUser(self)

    @property
    def actual_user(self):
        return self._impl.actual_user

    @property
    def access_token(self):
        """Access token used to authenticate"""
        return self._impl.access_token

    @property
    def settings(self):
        """System settings"""
        return self._impl.getSettings(self)

    @property
    def database(self):
        return self._impl.database

    def getDatabaseCursor(self):
        """Return a read-only database cursor object

           This cursor object can only be used to execute SELECT queries."""
        return self._impl.database.readonly_cursor()

    def getUpdatingDatabaseCursor(self, *tables):
        """Return a database cursor for updating

           The return value is a "context manager", which returns the actual
           cursor object when entered and either commits or rolls back the
           current transaction when exited.  The actual cursor object can only
           be used to update the tables specified as arguments, using INSERT,
           UPDATE or DELETE queries.

           The cursor object can also be used to execute SELECT queries (against
           any tables.)"""
        return self._impl.database.updating_cursor(*tables)

    def setActualUser(self, user):
        assert isinstance(user, api.user.User)
        assert self._impl.actual_user is None
        self._impl.actual_user = user

    def setAccessToken(self, access_token):
        """Set the access token used to authenticate"""
        assert self._impl.access_token is None
        self._impl.access_token = access_token

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self._impl.close()
        return False

def startSession(for_user=False, for_system=False, for_testing=False):
    import api.impl
    assert sum((for_user, for_system, for_testing)) == 1
    return api.impl.critic.startSession(for_user, for_system, for_testing)

def settings():
    import api.impl
    assert api.impl.critic.settings is not None
    return api.impl.critic.settings
