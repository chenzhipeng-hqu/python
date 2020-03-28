# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'financial.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(786, 586)
        self.actionauthor = QAction(MainWindow)
        self.actionauthor.setObjectName(u"actionauthor")
        self.actionabout = QAction(MainWindow)
        self.actionabout.setObjectName(u"actionabout")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(650, 220, 111, 211))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.merge_other_payables_pushButton = QPushButton(self.verticalLayoutWidget)
        self.merge_other_payables_pushButton.setObjectName(u"merge_other_payables_pushButton")

        self.verticalLayout.addWidget(self.merge_other_payables_pushButton)

        self.pushButton = QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)

        self.verticalLayout.setStretch(1, 10)
        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(20, 220, 611, 311))
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(650, 500, 111, 31))
        self.mouse_horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.mouse_horizontalLayout.setSpacing(10)
        self.mouse_horizontalLayout.setObjectName(u"mouse_horizontalLayout")
        self.mouse_horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.x_label = QLabel(self.layoutWidget)
        self.x_label.setObjectName(u"x_label")
        self.x_label.setLayoutDirection(Qt.LeftToRight)
        self.x_label.setAlignment(Qt.AlignCenter)

        self.mouse_horizontalLayout.addWidget(self.x_label)

        self.y_label = QLabel(self.layoutWidget)
        self.y_label.setObjectName(u"y_label")
        self.y_label.setAlignment(Qt.AlignCenter)

        self.mouse_horizontalLayout.addWidget(self.y_label)

        self.mouse_horizontalLayout.setStretch(0, 10)
        self.mouse_horizontalLayout.setStretch(1, 10)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(20, 20, 751, 181))
        self.payables_tab = QWidget()
        self.payables_tab.setObjectName(u"payables_tab")
        self.horizontalLayoutWidget = QWidget(self.payables_tab)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(0, 10, 741, 41))
        self.payables_horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.payables_horizontalLayout.setSpacing(6)
        self.payables_horizontalLayout.setObjectName(u"payables_horizontalLayout")
        self.payables_horizontalLayout.setContentsMargins(10, 5, 10, 5)
        self.time_label = QLabel(self.horizontalLayoutWidget)
        self.time_label.setObjectName(u"time_label")
        self.time_label.setLayoutDirection(Qt.LeftToRight)
        self.time_label.setAlignment(Qt.AlignCenter)

        self.payables_horizontalLayout.addWidget(self.time_label)

        self.s_year_lineEdit = QLineEdit(self.horizontalLayoutWidget)
        self.s_year_lineEdit.setObjectName(u"s_year_lineEdit")

        self.payables_horizontalLayout.addWidget(self.s_year_lineEdit)

        self.s_year_label = QLabel(self.horizontalLayoutWidget)
        self.s_year_label.setObjectName(u"s_year_label")
        self.s_year_label.setLayoutDirection(Qt.LeftToRight)
        self.s_year_label.setAlignment(Qt.AlignCenter)

        self.payables_horizontalLayout.addWidget(self.s_year_label)

        self.s_month_lineEdit = QLineEdit(self.horizontalLayoutWidget)
        self.s_month_lineEdit.setObjectName(u"s_month_lineEdit")

        self.payables_horizontalLayout.addWidget(self.s_month_lineEdit)

        self.s_month_label = QLabel(self.horizontalLayoutWidget)
        self.s_month_label.setObjectName(u"s_month_label")
        self.s_month_label.setLayoutDirection(Qt.LeftToRight)
        self.s_month_label.setAlignment(Qt.AlignCenter)

        self.payables_horizontalLayout.addWidget(self.s_month_label)

        self.e_year_lineEdit = QLineEdit(self.horizontalLayoutWidget)
        self.e_year_lineEdit.setObjectName(u"e_year_lineEdit")

        self.payables_horizontalLayout.addWidget(self.e_year_lineEdit)

        self.e_year_label = QLabel(self.horizontalLayoutWidget)
        self.e_year_label.setObjectName(u"e_year_label")
        self.e_year_label.setLayoutDirection(Qt.LeftToRight)
        self.e_year_label.setAlignment(Qt.AlignCenter)

        self.payables_horizontalLayout.addWidget(self.e_year_label)

        self.e_month_lineEdit = QLineEdit(self.horizontalLayoutWidget)
        self.e_month_lineEdit.setObjectName(u"e_month_lineEdit")

        self.payables_horizontalLayout.addWidget(self.e_month_lineEdit)

        self.e_month_label = QLabel(self.horizontalLayoutWidget)
        self.e_month_label.setObjectName(u"e_month_label")
        self.e_month_label.setLayoutDirection(Qt.LeftToRight)
        self.e_month_label.setAlignment(Qt.AlignCenter)

        self.payables_horizontalLayout.addWidget(self.e_month_label)

        self.object_label = QLabel(self.horizontalLayoutWidget)
        self.object_label.setObjectName(u"object_label")
        self.object_label.setLayoutDirection(Qt.LeftToRight)
        self.object_label.setAlignment(Qt.AlignCenter)

        self.payables_horizontalLayout.addWidget(self.object_label)

        self.object_lineEdit = QLineEdit(self.horizontalLayoutWidget)
        self.object_lineEdit.setObjectName(u"object_lineEdit")

        self.payables_horizontalLayout.addWidget(self.object_lineEdit)

        self.download_payables_pushButton = QPushButton(self.horizontalLayoutWidget)
        self.download_payables_pushButton.setObjectName(u"download_payables_pushButton")

        self.payables_horizontalLayout.addWidget(self.download_payables_pushButton)

        self.payables_horizontalLayout.setStretch(0, 1)
        self.payables_horizontalLayout.setStretch(1, 1)
        self.payables_horizontalLayout.setStretch(2, 1)
        self.payables_horizontalLayout.setStretch(3, 1)
        self.payables_horizontalLayout.setStretch(4, 1)
        self.payables_horizontalLayout.setStretch(5, 1)
        self.payables_horizontalLayout.setStretch(6, 1)
        self.payables_horizontalLayout.setStretch(7, 1)
        self.payables_horizontalLayout.setStretch(8, 1)
        self.payables_horizontalLayout.setStretch(9, 1)
        self.payables_horizontalLayout.setStretch(10, 2)
        self.payables_horizontalLayout.setStretch(11, 1)
        self.tabWidget.addTab(self.payables_tab, "")
        self.test_tab = QWidget()
        self.test_tab.setObjectName(u"test_tab")
        self.tabWidget.addTab(self.test_tab, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 786, 23))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        font = QFont()
        font.setFamily(u"\u6977\u4f53")
        font.setPointSize(14)
        self.statusbar.setFont(font)
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.actionabout)
        self.menu.addAction(self.actionauthor)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionauthor.setText(QCoreApplication.translate("MainWindow", u"author", None))
        self.actionabout.setText(QCoreApplication.translate("MainWindow", u"about", None))
        self.merge_other_payables_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u5408\u5e76\u5185\u90e8\u8ba2\u5355", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.textBrowser.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'SimSun'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">\u6b22\u8fce\u4f7f\u7528\u8d22\u52a1\u5c0f\u5de5\u5177</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt;\"><br /></p></body></html>", None))
        self.x_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.y_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.time_label.setText(QCoreApplication.translate("MainWindow", u"\u671f\u95f4", None))
        self.s_year_label.setText(QCoreApplication.translate("MainWindow", u"\u5e74", None))
        self.s_month_label.setText(QCoreApplication.translate("MainWindow", u"\u6708  -", None))
        self.e_year_label.setText(QCoreApplication.translate("MainWindow", u"\u5e74", None))
        self.e_month_label.setText(QCoreApplication.translate("MainWindow", u"\u6708", None))
        self.object_label.setText(QCoreApplication.translate("MainWindow", u"  \u79d1\u76ee", None))
        self.download_payables_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u8f7d", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.payables_tab), QCoreApplication.translate("MainWindow", u"\u5e94\u6536/\u4ed8\u6b3e", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.test_tab), QCoreApplication.translate("MainWindow", u"\u6d4b\u8bd5", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"help", None))
    # retranslateUi

