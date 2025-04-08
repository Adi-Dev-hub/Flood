# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(402, 114)
        self.actionFRZI = QAction(MainWindow)
        self.actionFRZI.setObjectName(u"actionFRZI")
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionFRZ_IA = QAction(MainWindow)
        self.actionFRZ_IA.setObjectName(u"actionFRZ_IA")
        self.actionInterpolation = QAction(MainWindow)
        self.actionInterpolation.setObjectName(u"actionInterpolation")
        self.actionClipping_Raster = QAction(MainWindow)
        self.actionClipping_Raster.setObjectName(u"actionClipping_Raster")
        self.actionSlope = QAction(MainWindow)
        self.actionSlope.setObjectName(u"actionSlope")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 402, 26))
        self.menuFRZA = QMenu(self.menuBar)
        self.menuFRZA.setObjectName(u"menuFRZA")
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuInterpolation = QMenu(self.menuBar)
        self.menuInterpolation.setObjectName(u"menuInterpolation")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuFRZA.menuAction())
        self.menuBar.addAction(self.menuInterpolation.menuAction())
        self.menuFRZA.addAction(self.actionFRZI)
        self.menuFRZA.addAction(self.actionFRZ_IA)
        self.menuFile.addAction(self.actionOpen)
        self.menuInterpolation.addAction(self.actionInterpolation)
        self.menuInterpolation.addAction(self.actionClipping_Raster)
        self.menuInterpolation.addAction(self.actionSlope)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionFRZI.setText(QCoreApplication.translate("MainWindow", u"FRZI", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionFRZ_IA.setText(QCoreApplication.translate("MainWindow", u"FRZ-IA", None))
        self.actionInterpolation.setText(QCoreApplication.translate("MainWindow", u"Interpolation", None))
        self.actionClipping_Raster.setText(QCoreApplication.translate("MainWindow", u"Clipping Raster", None))
        self.actionSlope.setText(QCoreApplication.translate("MainWindow", u"Slope", None))
        self.menuFRZA.setTitle(QCoreApplication.translate("MainWindow", u"Flood-Analysis", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuInterpolation.setTitle(QCoreApplication.translate("MainWindow", u"Tools", None))
    # retranslateUi

