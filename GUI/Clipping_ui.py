# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Clipping.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QPlainTextEdit,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(458, 371)
        self.verticalLayoutWidget = QWidget(Dialog)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(60, 50, 361, 231))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.plainTextEdit = QPlainTextEdit(self.verticalLayoutWidget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")

        self.verticalLayout.addWidget(self.plainTextEdit)

        self.plainTextEdit_2 = QPlainTextEdit(self.verticalLayoutWidget)
        self.plainTextEdit_2.setObjectName(u"plainTextEdit_2")

        self.verticalLayout.addWidget(self.plainTextEdit_2)

        self.plainTextEdit_3 = QPlainTextEdit(self.verticalLayoutWidget)
        self.plainTextEdit_3.setObjectName(u"plainTextEdit_3")

        self.verticalLayout.addWidget(self.plainTextEdit_3)

        self.pushButton = QPushButton(Dialog)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(350, 330, 75, 24))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Clipping", None))
        self.plainTextEdit.setPlainText(QCoreApplication.translate("Dialog", u"Input Raster", None))
        self.plainTextEdit_2.setPlainText(QCoreApplication.translate("Dialog", u"Mask Raster\n"
"", None))
        self.plainTextEdit_3.setPlainText(QCoreApplication.translate("Dialog", u"No Data calue", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"Run", None))
    # retranslateUi

