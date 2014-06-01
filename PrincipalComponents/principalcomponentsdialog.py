# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PrincipalComponentsDialog
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
        self.inFileName = str(QtGui.QFileDialog.getOpenFileName(self,
                                                        "Input Raster File:"))

        gdal.AllRegister()
        dataset = gdal.Open(str(self.inFileName))
        self.rasterBands = dataset.RasterCount
        dataset = None

        self.ui.comboBox.clear()
        for i in range(self.rasterBands, 0, -1):
            self.ui.comboBox.addItem(str(i))
        self.ui.comboBox.setDisabled(False)

        if self.inFileName is not None and self.outFileName is not None and self.rasterBands != 0:
            self.ui.okButton.setDisabled(False)

        self.ui.lineEdit.clear()
        self.ui.lineEdit.setText(self.inFileName)

    def showSaveDialog(self):
        #self.outFileName = str(QtGui.QFileDialog.getSaveFileName(self,
        #        'Output Raster File:', '', '*.tif'))

        # Declare the filetype in which to save the output file
        # Currently the plugin only supports GeoTIFF files
        fileTypes = 'GeoTIFF Files (*.tif *.tiff)'
        fileName, filter = QtGui.QFileDialog.getSaveFileNameAndFilter(
            self, 'Output Raster File:', '', fileTypes)

        if fileName is None:
            return
        else:
            # Extract the base filename without the suffix if it exists
            # Convert the fileName from QString to python string
            fileNameStr = str(fileName)

            # Split the fileNameStr where/if a '.' exists
            splittedFileName = fileNameStr.split('.')

            # Finally extract the base filename from the splitted filename
            baseFileName = splittedFileName[0]

            # Initialize the suffix string
            suffixStr = ''

            # Check if the user entered a suffix
            suffixExists = False
            existingSuffix = ''
            if len(splittedFileName) != 1:
                existingSuffix = splittedFileName[len(splittedFileName) - 1]
                if existingSuffix is not None:
                    suffixExists = True
                    

            # Extract the suffix from the selected filetype filter
            # Convert the selected filter from QString to python string
            filterStr = str(filter)

            # Split the filter string where/if an asterisk (*) exists
            # I do this to find where the first suffix of the selected filetype
            # occurs
            splittedFilter = filterStr.split('*')

            # If a suffix is not supplied by the user it will be automatically
            # added to the filename. The default suffix will be the first
            # available suffix for the chosen filetype
            if not suffixExists:
                # Extract the 'dirty' suffix string where the first suffix is located
                dirtySuffixStr = splittedFilter[1]

                # Find out the number of the available suffixes
                suffixNum = len(splittedFilter) - 1

                if suffixNum == 1:
                    # Split the dirty suffix string where a ')' occurs
                    # which indicates where the selected filetype ends
                    splittedDirtySuffixStr = dirtySuffixStr.split(')')
                else:
                    # Split the dirty suffix string where a space occurs which
                    # indicates where the selected filetype suffix ends
                    splittedDirtySuffixStr = dirtySuffixStr.split(' ')
                suffixStr = splittedDirtySuffixStr[0]
            else:
                # WE NEED TO CHECK IF THE SUPPLIED SUFFIX CORRESPONDS TO THE
                # SELECTED FILETYPE

                # Extract all the suffixes available for the selected filetype
                # First find out the number of the available suffixes
                suffixNum = len(splittedFilter) - 1

                if suffixNum == 1:
                    # Extract the 'dirty' suffix string where the suffix is located
                    dirtySuffixStr = splittedFilter[1]

                    # Split the dirty suffix string where a space occurs which
                    # indicates where the selected filetype suffix ends
                    splittedDirtySuffixStr = dirtySuffixStr.split(' ')
                    suffixStr = splittedDirtySuffixStr[0]

                    
                else:
                    suffixList = []
                    if suffixNum == 2:
                        # Extract the first suffix and put it in the list
                        dirtySuffixStr = splittedFilter[1]
                        splittedDirtySuffixStr = dirtySuffixStr.split(' ')
                        suffixList.append(splittedDirtySuffixStr[0])

                        # Extract the second suffix and put it in the list
                        dirtySuffixStr = splittedFilter[2]
                        splittedDirtySuffixStr = dirtySuffixStr.split(')')
                        suffixList.append(splittedDirtySuffixStr[0])

                    else:
                        # Extract the first suffix and put it in the list
                        dirtySuffixStr = splittedFilter[1]
                        splittedDirtySuffixStr = dirtySuffixStr.split(' ')
                        suffixList.append(splittedDirtySuffixStr[0])

                        # Extract the last suffix and put it in the list
                        dirtySuffixStr = splittedFilter[suffixNum]
                        splittedDirtySuffixStr = dirtySuffixStr.split(')')
                        suffixList.append(splittedDirtySuffixStr[0])

                        # Extract the rest of the suffixes and put them in the list
                        for i in xrange(2, suffixNum):
                            dirtySuffixStr = splittedFilter[i]
                            splittedDirtySuffixStr = dirtySuffixStr.split(' ')
                            suffixList.append(splittedDirtySuffixStr[0])

                    # Find if the user supplied suffix is valid for the
                    # chosen filetype and set it as the filename suffix
                    isValidSuffix = False
                    userSuffix = '.' + existingSuffix
                    for i in xrange(suffixNum + 1):
                        if userSuffix == suffixList[i]:
                            isValidSuffix = True
                            suffixStr = userSuffix
                            break

                    # If the supplied suffix is not valid replace it
                    # with the default suffix for the chosen filetype
                    if not isValidSuffix:
                        suffixStr = suffixList[0]         

            self.outFileName = baseFileName + suffixStr

        if self.inFileName is not None and self.outFileName is not None and self.rasterBands != 0:
            self.ui.okButton.setDisabled(False)
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_2.setText(self.outFileName)

    def pcNum(self):
        pcBands = int(str(self.ui.comboBox.currentText()))
        return pcBands

    def calcPca(self):
        pca(self.inFileName, self.outFileName, self.pcNum())
        self.close()
