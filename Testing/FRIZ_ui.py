# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FRIZ_v2.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QDoubleSpinBox, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QScrollArea, QSizePolicy,
    QTabWidget, QTableWidget, QTableWidgetItem, QTextBrowser,
    QToolButton, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1098, 900)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.scrollArea = QScrollArea(Dialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1053, 864))
        self.gridLayout_3 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.tabWidget = QTabWidget(self.scrollAreaWidgetContents)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_8 = QGridLayout(self.tab)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.groupBox = QGroupBox(self.tab)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEdit = QLineEdit(self.groupBox)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_2.addWidget(self.lineEdit)

        self.toolButton = QToolButton(self.groupBox)
        self.toolButton.setObjectName(u"toolButton")

        self.horizontalLayout_2.addWidget(self.toolButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lineEdit_2 = QLineEdit(self.groupBox)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.horizontalLayout_3.addWidget(self.lineEdit_2)

        self.toolButton_2 = QToolButton(self.groupBox)
        self.toolButton_2.setObjectName(u"toolButton_2")

        self.horizontalLayout_3.addWidget(self.toolButton_2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.lineEdit_3 = QLineEdit(self.groupBox)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.horizontalLayout_4.addWidget(self.lineEdit_3)

        self.toolButton_3 = QToolButton(self.groupBox)
        self.toolButton_3.setObjectName(u"toolButton_3")

        self.horizontalLayout_4.addWidget(self.toolButton_3)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.gridLayout_8.addWidget(self.groupBox, 0, 0, 1, 1)

        self.groupBox_3 = QGroupBox(self.tab)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy1)
        self.gridLayout_2 = QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.pushButton_2 = QPushButton(self.groupBox_3)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy2)

        self.gridLayout_2.addWidget(self.pushButton_2, 1, 0, 1, 1)

        self.tableWidget = QTableWidget(self.groupBox_3)
        if (self.tableWidget.columnCount() < 4):
            self.tableWidget.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        if (self.tableWidget.rowCount() < 4):
            self.tableWidget.setRowCount(4)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget.setItem(0, 0, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget.setItem(0, 1, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget.setItem(0, 2, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget.setItem(0, 3, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableWidget.setItem(1, 0, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableWidget.setItem(1, 1, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableWidget.setItem(1, 2, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tableWidget.setItem(1, 3, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tableWidget.setItem(2, 0, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.tableWidget.setItem(2, 1, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.tableWidget.setItem(2, 2, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.tableWidget.setItem(2, 3, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.tableWidget.setItem(3, 0, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.tableWidget.setItem(3, 1, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.tableWidget.setItem(3, 2, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.tableWidget.setItem(3, 3, __qtablewidgetitem23)
        self.tableWidget.setObjectName(u"tableWidget")
        sizePolicy2.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy2)
        self.tableWidget.setMinimumSize(QSize(580, 180))
        self.tableWidget.setMaximumSize(QSize(580, 180))

        self.gridLayout_2.addWidget(self.tableWidget, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.groupBox_3, 1, 0, 1, 1)

        self.groupBox_2 = QGroupBox(self.tab)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.gridLayout_6 = QGridLayout(self.groupBox_2)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.groupBox_5 = QGroupBox(self.groupBox_2)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.gridLayout_4 = QGridLayout(self.groupBox_5)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_10 = QLabel(self.groupBox_5)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_4.addWidget(self.label_10, 0, 0, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.doubleSpinBox_weigh_1 = QDoubleSpinBox(self.groupBox_5)
        self.doubleSpinBox_weigh_1.setObjectName(u"doubleSpinBox_weigh_1")
        self.doubleSpinBox_weigh_1.setValue(0.200000000000000)

        self.verticalLayout_2.addWidget(self.doubleSpinBox_weigh_1)


        self.gridLayout_4.addLayout(self.verticalLayout_2, 1, 0, 1, 1)

        self.label_13 = QLabel(self.groupBox_5)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_4.addWidget(self.label_13, 2, 0, 1, 1)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.doubleSpinBox_weigh_2 = QDoubleSpinBox(self.groupBox_5)
        self.doubleSpinBox_weigh_2.setObjectName(u"doubleSpinBox_weigh_2")
        self.doubleSpinBox_weigh_2.setValue(0.200000000000000)

        self.verticalLayout_3.addWidget(self.doubleSpinBox_weigh_2)


        self.gridLayout_4.addLayout(self.verticalLayout_3, 3, 0, 1, 1)

        self.label_11 = QLabel(self.groupBox_5)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_4.addWidget(self.label_11, 4, 0, 1, 1)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.doubleSpinBox_weigh_3 = QDoubleSpinBox(self.groupBox_5)
        self.doubleSpinBox_weigh_3.setObjectName(u"doubleSpinBox_weigh_3")
        self.doubleSpinBox_weigh_3.setValue(0.250000000000000)

        self.verticalLayout_5.addWidget(self.doubleSpinBox_weigh_3)


        self.gridLayout_4.addLayout(self.verticalLayout_5, 5, 0, 1, 1)

        self.label_12 = QLabel(self.groupBox_5)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_4.addWidget(self.label_12, 6, 0, 1, 1)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.doubleSpinBox_weigh_4 = QDoubleSpinBox(self.groupBox_5)
        self.doubleSpinBox_weigh_4.setObjectName(u"doubleSpinBox_weigh_4")
        self.doubleSpinBox_weigh_4.setValue(0.350000000000000)

        self.verticalLayout_4.addWidget(self.doubleSpinBox_weigh_4)


        self.gridLayout_4.addLayout(self.verticalLayout_4, 7, 0, 1, 1)


        self.gridLayout_6.addWidget(self.groupBox_5, 0, 0, 1, 1)

        self.groupBox_6 = QGroupBox(self.groupBox_2)
        self.groupBox_6.setObjectName(u"groupBox_6")
        sizePolicy.setHeightForWidth(self.groupBox_6.sizePolicy().hasHeightForWidth())
        self.groupBox_6.setSizePolicy(sizePolicy)
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_21 = QLabel(self.groupBox_6)
        self.label_21.setObjectName(u"label_21")

        self.verticalLayout_6.addWidget(self.label_21)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.lineEdit_4 = QLineEdit(self.groupBox_6)
        self.lineEdit_4.setObjectName(u"lineEdit_4")

        self.horizontalLayout_8.addWidget(self.lineEdit_4)

        self.toolButton_4 = QToolButton(self.groupBox_6)
        self.toolButton_4.setObjectName(u"toolButton_4")

        self.horizontalLayout_8.addWidget(self.toolButton_4)


        self.verticalLayout_6.addLayout(self.horizontalLayout_8)

        self.label_22 = QLabel(self.groupBox_6)
        self.label_22.setObjectName(u"label_22")

        self.verticalLayout_6.addWidget(self.label_22)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.lineEdit_5 = QLineEdit(self.groupBox_6)
        self.lineEdit_5.setObjectName(u"lineEdit_5")

        self.horizontalLayout_9.addWidget(self.lineEdit_5)

        self.toolButton_5 = QToolButton(self.groupBox_6)
        self.toolButton_5.setObjectName(u"toolButton_5")

        self.horizontalLayout_9.addWidget(self.toolButton_5)


        self.verticalLayout_6.addLayout(self.horizontalLayout_9)

        self.label_23 = QLabel(self.groupBox_6)
        self.label_23.setObjectName(u"label_23")

        self.verticalLayout_6.addWidget(self.label_23)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.lineEdit_6 = QLineEdit(self.groupBox_6)
        self.lineEdit_6.setObjectName(u"lineEdit_6")

        self.horizontalLayout_10.addWidget(self.lineEdit_6)

        self.toolButton_6 = QToolButton(self.groupBox_6)
        self.toolButton_6.setObjectName(u"toolButton_6")

        self.horizontalLayout_10.addWidget(self.toolButton_6)


        self.verticalLayout_6.addLayout(self.horizontalLayout_10)


        self.gridLayout_6.addWidget(self.groupBox_6, 0, 1, 1, 1)

        self.groupBox_4 = QGroupBox(self.groupBox_2)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.gridLayout_7 = QGridLayout(self.groupBox_4)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.label_14 = QLabel(self.groupBox_4)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_7.addWidget(self.label_14, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_4 = QLabel(self.groupBox_4)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout.addWidget(self.label_4)

        self.doubleSpinBox_low_1 = QDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBox_low_1.setObjectName(u"doubleSpinBox_low_1")
        self.doubleSpinBox_low_1.setDecimals(3)
        self.doubleSpinBox_low_1.setMaximum(9999.989999999999782)
        self.doubleSpinBox_low_1.setValue(570.000000000000000)

        self.horizontalLayout.addWidget(self.doubleSpinBox_low_1)

        self.label_5 = QLabel(self.groupBox_4)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout.addWidget(self.label_5)

        self.doubleSpinBox_upp_1 = QDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBox_upp_1.setObjectName(u"doubleSpinBox_upp_1")
        self.doubleSpinBox_upp_1.setMaximum(9999.989999999999782)
        self.doubleSpinBox_upp_1.setValue(700.000000000000000)

        self.horizontalLayout.addWidget(self.doubleSpinBox_upp_1)


        self.gridLayout_7.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.label_15 = QLabel(self.groupBox_4)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_7.addWidget(self.label_15, 2, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_6 = QLabel(self.groupBox_4)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_5.addWidget(self.label_6)

        self.doubleSpinBox_low_2 = QDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBox_low_2.setObjectName(u"doubleSpinBox_low_2")
        self.doubleSpinBox_low_2.setDecimals(3)
        self.doubleSpinBox_low_2.setMaximum(999.990000000000009)
        self.doubleSpinBox_low_2.setValue(20.000000000000000)

        self.horizontalLayout_5.addWidget(self.doubleSpinBox_low_2)

        self.label_7 = QLabel(self.groupBox_4)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_5.addWidget(self.label_7)

        self.doubleSpinBox_upp_2 = QDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBox_upp_2.setObjectName(u"doubleSpinBox_upp_2")
        self.doubleSpinBox_upp_2.setMaximum(999.990000000000009)
        self.doubleSpinBox_upp_2.setValue(40.000000000000000)

        self.horizontalLayout_5.addWidget(self.doubleSpinBox_upp_2)


        self.gridLayout_7.addLayout(self.horizontalLayout_5, 3, 0, 1, 1)

        self.label_17 = QLabel(self.groupBox_4)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_7.addWidget(self.label_17, 4, 0, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_8 = QLabel(self.groupBox_4)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_6.addWidget(self.label_8)

        self.doubleSpinBox_low_3 = QDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBox_low_3.setObjectName(u"doubleSpinBox_low_3")
        self.doubleSpinBox_low_3.setMaximum(999.990000000000009)
        self.doubleSpinBox_low_3.setValue(20.000000000000000)

        self.horizontalLayout_6.addWidget(self.doubleSpinBox_low_3)

        self.label_9 = QLabel(self.groupBox_4)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_6.addWidget(self.label_9)

        self.doubleSpinBox_upp_3 = QDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBox_upp_3.setObjectName(u"doubleSpinBox_upp_3")
        self.doubleSpinBox_upp_3.setMaximum(999.990000000000009)
        self.doubleSpinBox_upp_3.setValue(40.000000000000000)

        self.horizontalLayout_6.addWidget(self.doubleSpinBox_upp_3)


        self.gridLayout_7.addLayout(self.horizontalLayout_6, 5, 0, 1, 1)

        self.label_16 = QLabel(self.groupBox_4)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_7.addWidget(self.label_16, 6, 0, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_18 = QLabel(self.groupBox_4)
        self.label_18.setObjectName(u"label_18")

        self.horizontalLayout_7.addWidget(self.label_18)

        self.doubleSpinBox_low_4 = QDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBox_low_4.setObjectName(u"doubleSpinBox_low_4")
        self.doubleSpinBox_low_4.setValue(0.300000000000000)

        self.horizontalLayout_7.addWidget(self.doubleSpinBox_low_4)

        self.label_19 = QLabel(self.groupBox_4)
        self.label_19.setObjectName(u"label_19")

        self.horizontalLayout_7.addWidget(self.label_19)

        self.doubleSpinBox_upp_4 = QDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBox_upp_4.setObjectName(u"doubleSpinBox_upp_4")
        self.doubleSpinBox_upp_4.setValue(0.700000000000000)

        self.horizontalLayout_7.addWidget(self.doubleSpinBox_upp_4)


        self.gridLayout_7.addLayout(self.horizontalLayout_7, 7, 0, 1, 1)

        self.label_20 = QLabel(self.groupBox_4)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_7.addWidget(self.label_20, 8, 0, 1, 1)


        self.gridLayout_6.addWidget(self.groupBox_4, 0, 2, 1, 1)


        self.gridLayout_8.addWidget(self.groupBox_2, 2, 0, 1, 1)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_5 = QGridLayout(self.tab_2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.textBrowser = QTextBrowser(self.tab_2)
        self.textBrowser.setObjectName(u"textBrowser")

        self.gridLayout_5.addWidget(self.textBrowser, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.pushButton = QPushButton(Dialog)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy2.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Input Parameters", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Insert the DEM file of the Study Region", None))
        self.toolButton.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Insert the Rainfall  Interpolation of the Study Region", None))
        self.toolButton_2.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Insert the Proximity to Waterbodies  file of the Study Region", None))
        self.toolButton_3.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Dialog", u"AHP", None))
        self.pushButton_2.setText(QCoreApplication.translate("Dialog", u"OK", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"Elevation", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Slope", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"Proximity ", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog", u"Rainfall", None));
        ___qtablewidgetitem4 = self.tableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Dialog", u"Elevation", None));
        ___qtablewidgetitem5 = self.tableWidget.verticalHeaderItem(1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Dialog", u"Slope", None));
        ___qtablewidgetitem6 = self.tableWidget.verticalHeaderItem(2)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Dialog", u"Proximity", None));
        ___qtablewidgetitem7 = self.tableWidget.verticalHeaderItem(3)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Dialog", u"Rainfall", None));

        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        ___qtablewidgetitem8 = self.tableWidget.item(0, 0)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Dialog", u"1.00", None));
        ___qtablewidgetitem9 = self.tableWidget.item(0, 1)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("Dialog", u"1.00", None));
        ___qtablewidgetitem10 = self.tableWidget.item(0, 2)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("Dialog", u"0.80", None));
        ___qtablewidgetitem11 = self.tableWidget.item(0, 3)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("Dialog", u"0.57", None));
        ___qtablewidgetitem12 = self.tableWidget.item(1, 0)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("Dialog", u"1.00", None));
        ___qtablewidgetitem13 = self.tableWidget.item(1, 1)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("Dialog", u"1.00", None));
        ___qtablewidgetitem14 = self.tableWidget.item(1, 2)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("Dialog", u"0.80", None));
        ___qtablewidgetitem15 = self.tableWidget.item(1, 3)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("Dialog", u"0.57", None));
        ___qtablewidgetitem16 = self.tableWidget.item(2, 0)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("Dialog", u"1.25", None));
        ___qtablewidgetitem17 = self.tableWidget.item(2, 1)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("Dialog", u"1.25", None));
        ___qtablewidgetitem18 = self.tableWidget.item(2, 2)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("Dialog", u"1.00", None));
        ___qtablewidgetitem19 = self.tableWidget.item(2, 3)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("Dialog", u"0.71", None));
        ___qtablewidgetitem20 = self.tableWidget.item(3, 0)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("Dialog", u"1.75", None));
        ___qtablewidgetitem21 = self.tableWidget.item(3, 1)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("Dialog", u"1.75", None));
        ___qtablewidgetitem22 = self.tableWidget.item(3, 2)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("Dialog", u"1.40", None));
        ___qtablewidgetitem23 = self.tableWidget.item(3, 3)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("Dialog", u"1.00", None));
        self.tableWidget.setSortingEnabled(__sortingEnabled)

        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"Weights and Range", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("Dialog", u"Assign weights", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Elevation", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"Slope", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"Proximity to WaterBodies", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"Rainfall ", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("Dialog", u"Range-Color", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"High", None))
        self.lineEdit_4.setPlaceholderText(QCoreApplication.translate("Dialog", u"#FF0000", None))
        self.toolButton_4.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"Middle", None))
        self.lineEdit_5.setPlaceholderText(QCoreApplication.translate("Dialog", u"#FFA500", None))
        self.toolButton_5.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.label_23.setText(QCoreApplication.translate("Dialog", u"Low", None))
        self.lineEdit_6.setPlaceholderText(QCoreApplication.translate("Dialog", u"#FFFF00", None))
        self.toolButton_6.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Dialog", u"Middle Range", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"Elevation", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Lower Limit", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Upper Limit", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"Slope", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Lower Limit", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Upper Limit", None))
        self.label_17.setText(QCoreApplication.translate("Dialog", u"Rainfall ", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Lower Limit", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Upper Limit", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"Proximity to WaterBodies", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"Lower Limit", None))
        self.label_19.setText(QCoreApplication.translate("Dialog", u"Upper Limit", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", u"Note: Lower class and Higher class will be assumed based on above range", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Dialog", u"Input", None))
        self.textBrowser.setHtml(QCoreApplication.translate("Dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Hello</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Dialog", u"Log", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"Run", None))
    # retranslateUi

