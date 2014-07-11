# -*- coding: utf-8 -*-
"""
/***************************************************************************
 HelpWidget
                                 A QGIS plugin
 Principal Component Analysis for rasters
                             -------------------
        begin                : 2013-04-29
        copyright            : (C) 2013, 2014 by Stavros Georgousis
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
"""

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSlot, SIGNAL, SLOT

class HelpWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        # Set up the user interface
        self.initUI()

    def initUI(self):
        self.mainLayout = QtGui.QVBoxLayout()

        self.scrollArea = QtGui.QScrollArea(self)
        self.helpLabel = QtGui.QLabel(self.scrollArea)

        # Set the helpLabel text
        # The text is hardcoded using QtDesigner
        self.helpLabel.setText(self.tr("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:30px; margin-bottom:12px; margin-left:12px; margin-right:12px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:600;\">PCA plugin for QGIS</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:12px; margin-right:12px; -qt-block-indent:0; text-indent:0px;\">PCA version 0.3.1</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:12px; margin-right:12px; -qt-block-indent:0; text-indent:0px;\">Author: Stavros Georgousis</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:12px; margin-right:12px; -qt-block-indent:0; text-indent:0px;\">PCA is licensed under GNU General Public Licence version 3+<br /></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:12px; margin-right:12px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Description</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:12px; margin-right:12px; -qt-block-indent:0; text-indent:0px;\">PCA performs Principal Components Analysis in multidimensional</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:12px; margin-right:12px; -qt-block-indent:0; text-indent:0px;\">raster data.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:12px; margin-right:12px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Usage</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:12px; margin-right:12px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Input Raster File</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:12px; margin-right:12px; -qt-block-indent:0; text-indent:0px;\">In this field you need to choose the input raster file you want</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:12px; margin-right:12px; -qt-block-indent:0; text-indent:0px;\">to process.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:12px; margin-right:12px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Number of output Principal Components</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:12px; margin-right:12px; -qt-block-indent:0; text-indent:0px;\">In this field you select the number of output principal</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:12px; margin-right:12px; -qt-block-indent:0; text-indent:0px;\">components - bands of the output raster file.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:12px; margin-right:12px; -qt-block-indent:0; text-indent:0px;\">This has nothing to do with the algorithm or its operation.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:12px; margin-right:12px; -qt-block-indent:0; text-indent:0px;\">To get all the information contained in the original dataset</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:12px; margin-right:12px; -qt-block-indent:0; text-indent:0px;\">you need to choose the maximum possible components.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:12px; margin-right:12px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Output Raster File</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:12px; margin-right:12px; -qt-block-indent:0; text-indent:0px;\">In this field you need to choose the filename in which the</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:12px; margin-right:12px; -qt-block-indent:0; text-indent:0px;\">output dataset will be saved. Currently the only supported</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:12px; margin-right:12px; -qt-block-indent:0; text-indent:0px;\">format is GeoTIFF (.tif / .tiff), which will be added automatically</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:12px; margin-right:12px; -qt-block-indent:0; text-indent:0px;\">if no file extension is added.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:12px; margin-right:12px; -qt-block-indent:0; text-indent:0px;\">There will be an additional output file with the statistical</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:12px; margin-right:12px; -qt-block-indent:0; text-indent:0px;\">results of the algorithm in plain text. Assuming the output </p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:12px; margin-right:12px; -qt-block-indent:0; text-indent:0px;\">raster filename is &quot;rasterpca.tif&quot;, the statistics text file filename</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:12px; margin-right:12px; -qt-block-indent:0; text-indent:0px;\">will be &quot;rasterpca_statistics.txt&quot; and will be saved in the same</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:12px; margin-right:12px; -qt-block-indent:0; text-indent:0px;\">directory as the output raster file.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:12px; margin-right:12px; -qt-block-indent:0; text-indent:0px;\">In the statistics file you will find various statistics that are</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:12px; margin-right:12px; -qt-block-indent:0; text-indent:0px;\">calculated in the process as well as the eigenvalues of the</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:12px; margin-right:12px; -qt-block-indent:0; text-indent:0px;\">principal components.</p></body></html>"))

        self.scrollArea.setWidget(self.helpLabel)
        self.mainLayout.addWidget(self.scrollArea)
        self.setLayout(self.mainLayout)