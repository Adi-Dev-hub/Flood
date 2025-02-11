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
        MainWindow.resize(661, 407)
        self.actionFRZA = QAction(MainWindow)
        self.actionFRZA.setObjectName(u"actionFRZA")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 661, 26))
        self.menuFRZA = QMenu(self.menuBar)
        self.menuFRZA.setObjectName(u"menuFRZA")
        self.menuInterpolation = QMenu(self.menuBar)
        self.menuInterpolation.setObjectName(u"menuInterpolation")
        self.menuProximity = QMenu(self.menuBar)
        self.menuProximity.setObjectName(u"menuProximity")
        self.menuSlope = QMenu(self.menuBar)
        self.menuSlope.setObjectName(u"menuSlope")
        self.menuClipping = QMenu(self.menuBar)
        self.menuClipping.setObjectName(u"menuClipping")
        self.menuLuLc_indexing = QMenu(self.menuBar)
        self.menuLuLc_indexing.setObjectName(u"menuLuLc_indexing")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuFRZA.menuAction())
        self.menuBar.addAction(self.menuInterpolation.menuAction())
        self.menuBar.addAction(self.menuProximity.menuAction())
        self.menuBar.addAction(self.menuSlope.menuAction())
        self.menuBar.addAction(self.menuClipping.menuAction())
        self.menuBar.addAction(self.menuLuLc_indexing.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionFRZA.setText(QCoreApplication.translate("MainWindow", u"FRZA", None))
        self.menuFRZA.setTitle(QCoreApplication.translate("MainWindow", u"FRZA", None))
        self.menuInterpolation.setTitle(QCoreApplication.translate("MainWindow", u"Interpolation", None))
        self.menuProximity.setTitle(QCoreApplication.translate("MainWindow", u"Proximity", None))
        self.menuSlope.setTitle(QCoreApplication.translate("MainWindow", u"Slope", None))
        self.menuClipping.setTitle(QCoreApplication.translate("MainWindow", u"Clipping", None))
        self.menuLuLc_indexing.setTitle(QCoreApplication.translate("MainWindow", u"LuLc indexing", None))
    # retranslateUi

