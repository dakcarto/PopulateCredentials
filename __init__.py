# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PopulateCredentials
                                 A QGIS plugin
 Plugin to populate existing credentials into authentication database
                             -------------------
        begin                : 2014-11-05
        copyright            : (C) 2014 by Larry Shaffer / Boundless Spatial Inc.
        email                : lshaffer@boundlessgeo.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load PopulateCredentials class from file PopulateCredentials.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .populate_credentials import PopulateCredentials
    return PopulateCredentials(iface)
