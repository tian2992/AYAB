# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ayab_gui.ui'
#
# Created by: PyQt4 UI code generator 4.10.3
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 581)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.knitting_options_dock = QtGui.QDockWidget(self.centralwidget)
        self.knitting_options_dock.setObjectName(_fromUtf8("knitting_options_dock"))
        self.dockWidgetContents_2 = QtGui.QWidget()
        self.dockWidgetContents_2.setObjectName(_fromUtf8("dockWidgetContents_2"))
        self.knitting_options_dock.setWidget(self.dockWidgetContents_2)
        self.gridLayout.addWidget(self.knitting_options_dock, 2, 1, 2, 1)
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 4, 0, 1, 1)
        self.assistant_dock = QtGui.QDockWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.assistant_dock.sizePolicy().hasHeightForWidth())
        self.assistant_dock.setSizePolicy(sizePolicy)
        self.assistant_dock.setMinimumSize(QtCore.QSize(500, 254))
        self.assistant_dock.setAcceptDrops(True)
        self.assistant_dock.setObjectName(_fromUtf8("assistant_dock"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.dockWidgetContents)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.widget = QtGui.QWidget(self.dockWidgetContents)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_3 = QtGui.QLabel(self.widget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.module_dropdown = QtGui.QComboBox(self.widget)
        self.module_dropdown.setObjectName(_fromUtf8("module_dropdown"))
        self.verticalLayout.addWidget(self.module_dropdown)
        spacerItem = QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addWidget(self.widget)
        self.widget_4 = QtGui.QWidget(self.dockWidgetContents)
        self.widget_4.setObjectName(_fromUtf8("widget_4"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.widget_4)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.label_2 = QtGui.QLabel(self.widget_4)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_4.addWidget(self.label_2)
        self.load_file_button = QtGui.QPushButton(self.widget_4)
        self.load_file_button.setObjectName(_fromUtf8("load_file_button"))
        self.verticalLayout_4.addWidget(self.load_file_button)
        self.filename_lineedit = QtGui.QLineEdit(self.widget_4)
        self.filename_lineedit.setText(_fromUtf8(""))
        self.filename_lineedit.setObjectName(_fromUtf8("filename_lineedit"))
        self.verticalLayout_4.addWidget(self.filename_lineedit)
        spacerItem1 = QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)
        self.horizontalLayout.addWidget(self.widget_4)
        self.widget_3 = QtGui.QWidget(self.dockWidgetContents)
        self.widget_3.setObjectName(_fromUtf8("widget_3"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.widget_3)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label_4 = QtGui.QLabel(self.widget_3)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_3.addWidget(self.label_4)
        self.knit_button = QtGui.QPushButton(self.widget_3)
        self.knit_button.setObjectName(_fromUtf8("knit_button"))
        self.verticalLayout_3.addWidget(self.knit_button)
        spacerItem2 = QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.horizontalLayout.addWidget(self.widget_3)
        self.assistant_dock.setWidget(self.dockWidgetContents)
        self.gridLayout.addWidget(self.assistant_dock, 2, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.image_pattern_view = QtGui.QGraphicsView(self.centralwidget)
        self.image_pattern_view.setObjectName(_fromUtf8("image_pattern_view"))
        self.horizontalLayout_2.addWidget(self.image_pattern_view)
        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuTools = QtGui.QMenu(self.menubar)
        self.menuTools.setObjectName(_fromUtf8("menuTools"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionLoad_AYAB_Firmware = QtGui.QAction(MainWindow)
        self.actionLoad_AYAB_Firmware.setObjectName(_fromUtf8("actionLoad_AYAB_Firmware"))
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionOpen_Knitting_Project = QtGui.QAction(MainWindow)
        self.actionOpen_Knitting_Project.setObjectName(_fromUtf8("actionOpen_Knitting_Project"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionHelp = QtGui.QAction(MainWindow)
        self.actionHelp.setObjectName(_fromUtf8("actionHelp"))
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuTools.addAction(self.actionLoad_AYAB_Firmware)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "All Yarns Are Beautiful", None))
        self.knitting_options_dock.setWindowTitle(_translate("MainWindow", "Knitting Options", None))
        self.assistant_dock.setWindowTitle(_translate("MainWindow", "Asistant", None))
        self.label_3.setText(_translate("MainWindow", "Select Module", None))
        self.label_2.setText(_translate("MainWindow", "Load File", None))
        self.load_file_button.setText(_translate("MainWindow", "Load File", None))
        self.label_4.setText(_translate("MainWindow", "Control", None))
        self.knit_button.setText(_translate("MainWindow", "Knit!", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.menuTools.setTitle(_translate("MainWindow", "Tools", None))
        self.actionLoad_AYAB_Firmware.setText(_translate("MainWindow", "Load AYAB Firmware", None))
        self.actionQuit.setText(_translate("MainWindow", "Quit", None))
        self.actionOpen_Knitting_Project.setText(_translate("MainWindow", "Open Knitting Project", None))
        self.actionAbout.setText(_translate("MainWindow", "Help - About", None))
        self.actionHelp.setText(_translate("MainWindow", "Help", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

