# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ayab_about.ui'
#
# Created: Sat Feb  7 20:47:30 2015
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_AboutForm(object):
    def setupUi(self, AboutForm):
        AboutForm.setObjectName(_fromUtf8("AboutForm"))
        AboutForm.resize(583, 312)
        AboutForm.setAutoFillBackground(False)
        AboutForm.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.verticalLayout = QtGui.QVBoxLayout(AboutForm)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(AboutForm)
        font = QtGui.QFont()
        font.setPointSize(144)
        self.label.setFont(font)
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8(":/ayab_logo.jpg")))
        self.label.setScaledContents(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtGui.QLabel(AboutForm)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.label_4 = QtGui.QLabel(AboutForm)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout.addWidget(self.label_4)
        self.label_3 = QtGui.QLabel(AboutForm)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(AboutForm)
        QtCore.QMetaObject.connectSlotsByName(AboutForm)

    def retranslateUi(self, AboutForm):
        AboutForm.setWindowTitle(_translate("AboutForm", "About AYAB", None))
        self.label_2.setText(_translate("AboutForm", "All Yarns Are Beautiful", None))
        self.label_4.setText(_translate("AboutForm", "<html><head/><body><p><a href=\"http://ayab-knitting.com\"><span style=\" text-decoration: underline; color:#0000ff;\">http://ayab-knitting.com</span></a></p></body></html>", None))
        self.label_3.setText(_translate("AboutForm", "Version 0.7", None))

import resources_rc
