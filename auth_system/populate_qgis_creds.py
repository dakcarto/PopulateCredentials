# -*- coding: utf-8 -*-
"""Pre-populate QGI authentication database with entries

NOTE: this script needs adjusted, or rewritten, relative to the desired result
and the existing authentication requirements for the network or user.

As it is coded, script will work for the current user, with a known password,
and generate an initial qgis-auth.db file, or use an existing one, for their
QGIS install, which will be pre-populated with configurations to known network
resources, using existing PKI credentials, which may be passphrase-protected.

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

from qgis.core import (
    QgsApplication,
    QgsAuthType,
    QgsAuthManager,
    QgsAuthConfigBasic,
    QgsAuthConfigPkiPaths,
    QgsAuthConfigPkiPkcs12
)

from PyQt4.QtCore import *
from PyQt4.QtGui import *

HOME = os.path.expanduser('~')
USER = os.path.split(HOME)[-1]
PKIDATA = os.path.join(HOME, 'PKI')

if __name__ == '__main__':
    qgsapp = QgsApplication(sys.argv, True)

    # These are for referencing the correct QSettings for the QGIS app
    QCoreApplication.setOrganizationName('QGIS')
    QCoreApplication.setOrganizationDomain('qgis.org')
    QCoreApplication.setApplicationName('QGIS2')

    # Initialize QGIS
    qgsapp.initQgis()
    print qgsapp.showSettings()

    # Initialize the auth system
    # noinspection PyArgumentList
    authm = QgsAuthManager.instance()
    authm.init()
    # This will use the standard qgis-auth.db location, but the rest of this
    # script will not work if qgis-auth.db already exists and you do NOT know
    # the user's chosen master password already stored in it.

    # If you want to generate individual qgis-auth.db for a list of users, just
    # do:
    #   authdbdir = tempfile.mkdtemp()
    #   authm.init(authdbdir)
    # Note that the saved paths to PKI components in the db will need to be the
    # same absolute paths as when the auth db is copied to the user's machine.
    # This means paths with the current user's name in them will not work when
    # copied to a different user (unless names are the same).

    print authm.authenticationDbPath()

    # Define pool of users and loop through them, or use the current user.
    # USERS = ["user"]
    # for user in USERS:

    # Get user's pre-defined QGIS master password.
    # This can be done in a variety of ways, depending upon user auth
    # systems, queried from LDAP, etc., using a variety of Python packages.
    # As an example, we hard-code define it as a standard password that must
    # be changed later by the user, OR if we know the user's defined password.
    mpass = 'password'

    # Set master password for QGIS and (optionally) store it in qgis-auth.db.
    # This also verifies the set password against by comparing password
    # against its derived hash stored in auth db.
    if not authm.setMasterPassword(mpass, True):
        print 'Failed to verify or store/verify password'
        sys.exit(1)

    # Now that we have a master password set/stored, we can use it to
    # encrypt and store authentication configurations.
    # There are 3 configurations that can be stored (as of Nov 2014), and
    # examples of their initialization are in the unit tests for
    # QGIS-with-PKI source tree (test_qgsauthsystem.py).

    # Add authentication configuration.
    # You can add as many auth configs as needed, but only one can be linked
    # to a given custom server config; although, you can create as many custom
    # server configs as needed. In this example, we are defining only one auth
    # config and linking it to multiple custom server configs, representing
    # different OWS services located at the same domain.

    # NOTE: PKI file components need to *already* exists on the filesystem in a
    # location that doesn't change, as their paths are stored in the auth db.
    # These particular components are from the test data samples.

    # # Basic configuration
    # configname = 'My Basic Config'
    # config = QgsAuthConfigBasic()
    # config.setName(kind)
    # config.setUri('https://localhost:8443')
    # config.setUsername('username')
    # config.setPassword('password')
    # config.setRealm('Realm')

    # ^^  OR  vv

    # # PKI-Paths (PEM-based) configuration
    # configname = 'My PKI Paths Config'
    # config = QgsAuthConfigPkiPaths()
    # config.setName(configname)
    # config.setUri('https://localhost:8443')
    # config.setCertId(os.path.join(PKIDATA, 'rod_cert.pem'))
    # config.setKeyId(os.path.join(PKIDATA, 'rod_key.pem'))
    # config.setKeyPassphrase('')
    # config.setIssuerId(os.path.join(PKIDATA, 'ca.pem'))
    # config.setIssuerSelfSigned(True)

    # ^^  OR  vv

    # PKI-PKCS#12 (*.p12-based) configuration
    configname = 'My PKI PKCS#12 Config'
    config = QgsAuthConfigPkiPkcs12()
    config.setName(configname)
    config.setUri('https://localhost:8443')
    config.setBundlePath(os.path.join(PKIDATA, 'rod.p12'))
    config.setBundlePassphrase('password')
    config.setIssuerPath(os.path.join(PKIDATA, 'ca.pem'))
    config.setIssuerSelfSigned(True)

    # Securely store the config in database (encrypted with master password)
    if not authm.storeAuthenticationConfig(config):
        print 'Failed to store {0} config'.format(configname)
        sys.exit(1)

    # The auth config has been given a unique ID from the auth system when it
    # was stored; retrieve it, so it can be linked to a custom server config.
    configid = config.id()

    # If the user does not have the OWS connection(s) that this auth config is
    # meant to connect to, define now.
    # NOTE: this assumes the individual connections do not already exist. If the
    # connection settings do exist, this will OVERWRITE them.

    settings = QSettings()  # get application's settings object

    print 'settings.fileName(): {0}'.format(settings.fileName())
    print 'settings.organizationName(): {0}'.format(settings.organizationName())
    print 'settings.applicationName(): {0}'.format(settings.applicationName())

    # WMS
    connkind = 'WMS'
    connname = 'My {0} SSL Server'.format(connkind)
    credskey = '/Qgis/{0}/{1}'.format(connkind, connname)
    connkey = '/Qgis/connections-{0}/{1}'.format(connkind.lower(), connname)

    settings.setValue(credskey + '/authid', configid)  # link to auth config
    settings.setValue(credskey + '/username', '')  # deprecated; use auth config
    settings.setValue(credskey + '/password', '')  # deprecated; use auth config

    settings.setValue(connkey + '/url', 'https://localhost:8443/geoserver/wms')

    # Optional settings for WMS (these are the defaults)
    # dpiMode: 0=Off, 1=QGIS, 2=UMN, 4=GeoServer, 7=All (default)
    settings.setValue(connkey + '/dpiMode', 7)
    settings.setValue(connkey + '/ignoreAxisOrientation', False)
    settings.setValue(connkey + '/ignoreGetFeatureInfoURI', False)
    settings.setValue(connkey + '/ignoreGetMapURI', False)
    settings.setValue(connkey + '/invertAxisOrientation', False)
    settings.setValue(connkey + '/referer', '')
    settings.setValue(connkey + '/smoothPixmapTransform', False)

    # WCS
    connkind = 'WCS'
    connname = 'My {0} SSL Server'.format(connkind)
    credskey = '/Qgis/{0}/{1}'.format(connkind, connname)
    connkey = '/Qgis/connections-{0}/{1}'.format(connkind.lower(), connname)

    settings.setValue(credskey + '/authid', configid)  # link to auth config
    settings.setValue(credskey + '/username', '')  # deprecated; use auth config
    settings.setValue(credskey + '/password', '')  # deprecated; use auth config

    settings.setValue(connkey + '/url', 'https://localhost:8443/geoserver/wcs')

    # Optional settings for WCS (these are the defaults)
    # dpiMode: 0=Off, 1=QGIS, 2=UMN, 4=GeoServer, 7=All (default)
    settings.setValue(connkey + '/dpiMode', 7)
    settings.setValue(connkey + '/ignoreAxisOrientation', False)
    settings.setValue(connkey + '/ignoreGetMapURI', False)
    settings.setValue(connkey + '/invertAxisOrientation', False)
    settings.setValue(connkey + '/referer', '')
    settings.setValue(connkey + '/smoothPixmapTransform', False)

    # WFS
    connkind = 'WFS'
    connname = 'My {0} SSL Server'.format(connkind)
    credskey = '/Qgis/{0}/{1}'.format(connkind, connname)
    connkey = '/Qgis/connections-{0}/{1}'.format(connkind.lower(), connname)

    settings.setValue(credskey + '/authid', configid)  # link to auth config
    settings.setValue(credskey + '/username', '')  # deprecated; use auth config
    settings.setValue(credskey + '/password', '')  # deprecated; use auth config

    settings.setValue(connkey + '/url', 'https://localhost:8443/geoserver/wfs')

    # Optional settings for WFS (these are the defaults)
    settings.setValue(connkey + '/referer', '')
