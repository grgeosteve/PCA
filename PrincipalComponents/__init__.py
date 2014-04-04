# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PrincipalComponents
                                 A QGIS plugin
 Principal Component Analysis for rasters
                             -------------------
        begin                : 2013-04-29
        copyright            : (C) 2013 by Stavros Georgousis
        email                : grgeosteve@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 3 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


def name():
    return "PCA"


def description():
    return "Principal Component Analysis for rasters"


def version():
    return "Version 0.1"


def icon():
    return "icon.png"


def qgisMinimumVersion():
    return "2.0"

def author():
    return "Stavros Georgousis"

def email():
    return "grgeosteve@gmail.com"

def classFactory(iface):
    # load PrincipalComponents class from file PrincipalComponents
    from principalcomponents import PrincipalComponents
    return PrincipalComponents(iface)
