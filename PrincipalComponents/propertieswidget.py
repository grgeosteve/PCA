# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PropertiesWidget
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

class PropertiesWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        # Set up the user interface
        self.initUI()

    def initUI(self):
        self.mainLayout = QtGui.QVBoxLayout()

        self.inputLayout = QtGui.QVBoxLayout()
        self.inputInnerLayout = QtGui.QHBoxLayout()
        self.inputLabel = QtGui.QLabel(self.tr("Input Raster File"), self)
        self.inputLineEdit = QtGui.QLineEdit(self)
        self.inputButton = QtGui.QPushButton("...", self)
        self.inputLayout.addWidget(self.inputLabel)
        self.inputInnerLayout.addWidget(self.inputLineEdit)
        self.inputInnerLayout.addWidget(self.inputButton)
        self.inputLayout.addLayout(self.inputInnerLayout)

        self.pcsLayout = QtGui.QVBoxLayout()
        self.pcsNumLabel = QtGui.QLabel(
                        self.tr("Number of output Principal Components:"),
                        self)
        self.pcsNumComboBox = QtGui.QComboBox(self)
        self.pcsLayout.addWidget(self.pcsNumLabel)
        self.pcsLayout.addWidget(self.pcsNumComboBox)

        self.outputLayout = QtGui.QVBoxLayout()
        self.outputInnerLayout = QtGui.QHBoxLayout()
        self.outputLabel = QtGui.QLabel(self.tr("Output Raster File"), self)
        self.outputLineEdit = QtGui.QLineEdit(self)
        self.outputButton = QtGui.QPushButton("...", self)
        self.outputLayout.addWidget(self.outputLabel)
        self.outputInnerLayout.addWidget(self.outputLineEdit)
        self.outputInnerLayout.addWidget(self.outputButton)
        self.outputLayout.addLayout(self.outputInnerLayout)

        #spacer = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Expanding,
        #                           QtGui.QSizePolicy.Minimum)

        self.buttonBoxLayout = QtGui.QHBoxLayout()
        self.cancelButton = QtGui.QPushButton(self.tr("Cancel"), self)
        self.okButton = QtGui.QPushButton("OK", self)
        self.buttonBoxLayout.addStretch(1)
        self.buttonBoxLayout.addWidget(self.cancelButton)
        self.buttonBoxLayout.addWidget(self.okButton)

        self.mainLayout.addLayout(self.inputLayout)
        self.mainLayout.addLayout(self.pcsLayout)
        self.mainLayout.addLayout(self.outputLayout)
        self.mainLayout.addStretch(1)
        self.mainLayout.addLayout(self.buttonBoxLayout)

        self.setLayout(self.mainLayout)