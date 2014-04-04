# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PrincipalComponentsDialog
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
"""

from PyQt4 import QtGui
from ui_principalcomponents import Ui_PrincipalComponents
from osgeo import gdal
from pca import pca
# create the dialog for zoom to point


class PrincipalComponentsDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_PrincipalComponents()
        self.ui.setupUi(self)

        self.setWindowTitle("PCA")

        # Additional code
        self.inFileName = None
        self.outFileName = None
        self.rasterBands = 0

        # For now disable some features
        self.ui.lineEdit.setReadOnly(True)
        self.ui.lineEdit_2.setReadOnly(True)
        self.ui.comboBox.setDisabled(True)
        self.ui.okButton.setDisabled(True)

        # Connect signals
        #self.ui.cancelButton.clicked.connect(self.close)
        self.ui.cancelButton.clicked.connect(self.close)

        self.ui.pushButton.clicked.connect(self.showOpenDialog)
        self.ui.pushButton_2.clicked.connect(self.showSaveDialog)
        self.ui.okButton.clicked.connect(self.calcPca)

    def showOpenDialog(self):
        self.inFileName = str(QtGui.QFileDialog.getOpenFileName(self, "Input Raster File:"))

        gdal.AllRegister()
        dataset = gdal.Open(str(self.inFileName))
        self.rasterBands = dataset.RasterCount
        dataset = None

        self.ui.comboBox.clear()
        for i in range(self.rasterBands, 0, -1):
            self.ui.comboBox.addItem(str(i))
        self.ui.comboBox.setDisabled(False)

        if self.inFileName != None and self.outFileName != None and self.rasterBands != 0:
            self.ui.okButton.setDisabled(False)
        
        self.ui.lineEdit.clear()
        self.ui.lineEdit.setText(self.inFileName)

    def showSaveDialog(self):
        self.outFileName = str(QtGui.QFileDialog.getSaveFileName(self, "Output Raster File:"))

        if self.inFileName != None and self.outFileName != None and self.rasterBands != 0:
            self.ui.okButton.setDisabled(False)
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_2.setText(self.outFileName)

    def pcNum(self):
        pcBands = int(str(self.ui.comboBox.currentText()))
        return pcBands

    def calcPca(self):
        pca(self.inFileName, self.outFileName, self.pcNum())
        self.close()
