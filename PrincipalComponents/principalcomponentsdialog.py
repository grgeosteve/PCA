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
from osgeo import gdal
from pca import pca
from propertieswidget import PropertiesWidget
from helpwidget import HelpWidget
# create the dialog for zoom to point


class PrincipalComponentsDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)

        # Set up the user interface
        self.initUI()

        # Initial configuration of the user interface
        self.configUI()

        # Set up the signals
        self.connectSignals()

        # Additional code
        self.inFileName = None
        self.outFileName = None
        self.rasterBands = 0

    def initUI(self):
        self.setWindowTitle("PCA")
        # Add a main layout for the dialog
        self.mainLayout = QtGui.QHBoxLayout()
        
        self.tabs = QtGui.QTabWidget()
        self.propWidget = PropertiesWidget()
        self.tabs.addTab(self.propWidget, self.tr("Properties"))
        self.helpWidget = HelpWidget()
        self.tabs.addTab(self.helpWidget, self.tr("Help"))

        self.mainLayout.addWidget(self.tabs)
        self.setLayout(self.mainLayout)

    def configUI(self):
        self.propWidget.inputLineEdit.setReadOnly(True)
        self.propWidget.outputLineEdit.setReadOnly(True)
        self.propWidget.pcsNumComboBox.setDisabled(True)
        self.propWidget.okButton.setDisabled(True)

    def connectSignals(self):
        self.propWidget.cancelButton.clicked.connect(self.close)
        self.propWidget.inputButton.clicked.connect(self.showOpenDialog)
        self.propWidget.outputButton.clicked.connect(self.showSaveDialog)
        self.propWidget.okButton.clicked.connect(self.calcPca)

    def showOpenDialog(self):
        self.inFileName = str(QtGui.QFileDialog.getOpenFileName(self,
                                                        "Input Raster File:"))

        gdal.AllRegister()
        dataset = gdal.Open(str(self.inFileName))
        self.rasterBands = dataset.RasterCount
        dataset = None

        self.propWidget.pcsNumComboBox.clear()
        for i in range(self.rasterBands, 0, -1):
            self.pcsNumComboBox.addItem(str(i))
        self.propWidget.pcsNumComboBox.setDisabled(False)

        if self.inFileName is not None and self.outFileName is not None and self.rasterBands != 0:
            self.propWidget.okButton.setDisabled(False)

        self.propWidget.inputLineEdit.clear()
        self.propWidget.inputLineEdit.setText(self.inFileName)

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
            self.propWidget.okButton.setDisabled(False)
        self.propWidget.outputLineEdit.clear()
        self.propWidget.outputLineEdit.setText(self.outFileName)

    def pcNum(self):
        pcBands = int(str(self.propWidget.pcsNumComboBox.currentText()))
        return pcBands

    def calcPca(self):
        pca(self.inFileName, self.outFileName, self.pcNum())
        self.close()
