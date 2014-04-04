# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_principalcomponents.ui'
#
# Created: Fri Apr  4 18:49:53 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_PrincipalComponents(object):
    def setupUi(self, PrincipalComponents):
        PrincipalComponents.setObjectName(_fromUtf8("PrincipalComponents"))
        PrincipalComponents.resize(476, 530)
        self.layoutWidget = QtGui.QWidget(PrincipalComponents)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 30, 391, 471))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_3.addWidget(self.label)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.pushButton = QtGui.QPushButton(self.layoutWidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.label_2)
        self.comboBox = QtGui.QComboBox(self.layoutWidget)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.verticalLayout_2.addWidget(self.comboBox)
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEdit_2 = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.horizontalLayout.addWidget(self.lineEdit_2)
        self.pushButton_2 = QtGui.QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_4.addLayout(self.verticalLayout)
        self.label_4 = QtGui.QLabel(self.layoutWidget)
        self.label_4.setTextFormat(QtCore.Qt.AutoText)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_4.addWidget(self.label_4)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem1 = QtGui.QSpacerItem(18, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.cancelButton = QtGui.QPushButton(self.layoutWidget)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout_3.addWidget(self.cancelButton)
        self.okButton = QtGui.QPushButton(self.layoutWidget)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.horizontalLayout_3.addWidget(self.okButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.retranslateUi(PrincipalComponents)
        QtCore.QMetaObject.connectSlotsByName(PrincipalComponents)

    def retranslateUi(self, PrincipalComponents):
        PrincipalComponents.setWindowTitle(_translate("PrincipalComponents", "PrincipalComponents", None))
        self.label.setText(_translate("PrincipalComponents", "Input Raster File:", None))
        self.pushButton.setText(_translate("PrincipalComponents", "...", None))
        self.label_2.setText(_translate("PrincipalComponents", "Number of output Principal Components:", None))
        self.label_3.setText(_translate("PrincipalComponents", "Output Raster FIle:", None))
        self.pushButton_2.setText(_translate("PrincipalComponents", "...", None))
        self.label_4.setText(_translate("PrincipalComponents", "<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Help:</span> The output raster file must be in <span style=\" color:#ff0000;\">*.tif </span><span style=\" color:#000000;\">/</span><span style=\" color:#ff0000;\"> *.tiff</span> format.</p><p>Saving in other formats has not implemented yet and</p><p>the plugin won\'t give the desired results.</p><p><br/>There will be an additional output file with the statistical</p><p>results of the algorithm in plain text. Assuming the output </p><p>raster filename is &quot;rasterpca.tif&quot;, the statistics text file filename</p><p>will be &quot;rasterpca_statistics.txt&quot; and will be saved in the same</p><p>directory as the output raster file.</p></body></html>", None))
        self.cancelButton.setText(_translate("PrincipalComponents", "Cancel", None))
        self.okButton.setText(_translate("PrincipalComponents", "OK", None))

