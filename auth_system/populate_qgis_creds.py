# -*- coding: utf-8 -*-
"""Pre-populate QGI authentication database with entries

NOTE: this script needs adjusted, or rewritten relative to the desired result
and the existing authentication requirements for the network or user.

As it is coded, the script will take a group of users, with known passwords and
generate an initial qgis-auth.db file, for their QGIS install, which is
pre-populated with configurations to known network resources, using existing PKI
credentials stored in *.p12 (PKCS#12) format, which may be passphrase-protected.

By default QGIS works with the OpenSSL key stores. On Windows, you can try using
the `wincertstore` package to retrieve existing client certs, via OIDs for
enhanced key usages like CLIENT_AUTH, then export those to PEM or PKCS#12
format. See: https://pypi.python.org/pypi/wincertstore

.. note:: This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
"""
__author__ = 'Larry Shaffer'
__date__ = '2014/11/05'
__copyright__ = 'Copyright 2014, Boundless Spatial, Inc.'
# This will get replaced with a git SHA1 when you do a git archive
__revision__ = '$Format:%H$'

import os
import sys
import tempfile
import time

from qgis.core import (
    QgsApplication,
    QgsAuthType,
    QgsAuthManager,
    QgsAuthProvider,
    QgsAuthProviderBasic,
    QgsAuthProviderPkiPaths,
    QgsAuthProviderPkiPkcs12,
    QgsAuthConfigBasic,
    QgsAuthConfigPkiPaths,
    QgsAuthConfigPkiPkcs12
)

from PyQt4.QtCore import *
from PyQt4.QtGui import *

if __name__ == '__main__':
    QGISAPP = QgsApplication(sys.argv, True)

    # Initialize QGIS
    QGISAPP.initQgis()
    s = QGISAPP.showSettings()
    print s

    # Initialize the auth system
    AUTHM = QgsAuthManager.instance()
    # If you do not want to generate indivudal qgis-auth.db for a bunch of
    # users, just do:
    #   AUTHM.init()
    # instead of defining a temp directory. This will use the standard
    # qgis-auth.db location, but the rest of this script will not work if
    # qgis-auth.db already exists and you do not know the user's chosen master
    # password for it.
    authdbdir = tempfile.mkdtemp()
    AUTHM.init(authdbdir)
    # empty, custom qgis-auth.db should now be in temp directory
    print AUTHM.authenticationDbPath()

    # Define pool of users and loop through them, or grab the current user
    USERS = ["user"]

    for user in USERS:
        # Get user's pre-defined QGIS master password
        # This can be done in a variety of ways, depending upon user auth
        # systems, queried from LDAP, etc., using a variety of Python packages.
        # As an example, we hard-code define it as a standard password that must
        # be changed later by the user.
        PASS = 'password'

        # Set master password for QGIS and store it in qgis-auth.db
        # This also verifies it was stored in the database correctly by comparing
        # password against its derived hash in db
        AUTHM.setMasterPassword(PASS, True)

        # Now that we have a master password set/stored, we can use it to
        # encrypt and store authentication configurations.
        # There are 3 configurations that can be stored (as of Nov 2014), and
        # examples of their initialization are in the unit tests for
        # QGIS-with-PKI source tree.
