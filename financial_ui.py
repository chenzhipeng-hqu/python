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
        MainWindow.resize(581, 411)
        MainWindow.setMinimumSize(QSize(581, 411))
        MainWindow.setMaximumSize(QSize(581, 411))
        self.actionauthor = QAction(MainWindow)
        self.actionauthor.setObjectName(u"actionauthor")
        self.actionabout = QAction(MainWindow)
        self.actionabout.setObjectName(u"actionabout")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.gridLayout.setContentsMargins(1, 5, 5, 1)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy1)
        self.pushButton.setMaximumSize(QSize(100, 30))

        self.verticalLayout.addWidget(self.pushButton)


        self.gridLayout.addLayout(self.verticalLayout, 1, 1, 1, 1)

        self.mouse_horizontalLayout = QHBoxLayout()
        self.mouse_horizontalLayout.setSpacing(10)
        self.mouse_horizontalLayout.setObjectName(u"mouse_horizontalLayout")
        self.mouse_horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.x_label = QLabel(self.centralwidget)
        self.x_label.setObjectName(u"x_label")
        self.x_label.setMaximumSize(QSize(100, 16777215))
        self.x_label.setLayoutDirection(Qt.LeftToRight)
        self.x_label.setAlignment(Qt.AlignCenter)

        self.mouse_horizontalLayout.addWidget(self.x_label)

        self.y_label = QLabel(self.centralwidget)
        self.y_label.setObjectName(u"y_label")
        self.y_label.setMaximumSize(QSize(100, 16777215))
        self.y_label.setAlignment(Qt.AlignCenter)

        self.mouse_horizontalLayout.addWidget(self.y_label)

        self.mouse_horizontalLayout.setStretch(0, 10)
        self.mouse_horizontalLayout.setStretch(1, 10)

        self.gridLayout.addLayout(self.mouse_horizontalLayout, 3, 1, 1, 1)

        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName(u"textBrowser")
        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy2)
        self.textBrowser.setMaximumSize(QSize(500, 300))

        self.gridLayout.addWidget(self.textBrowser, 1, 0, 3, 1)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy3)
        self.payables_tab = QWidget()
        self.payables_tab.setObjectName(u"payables_tab")
        self.gridLayout_3 = QGridLayout(self.payables_tab)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.payables_horizontalLayout = QHBoxLayout()
        self.payables_horizontalLayout.setSpacing(6)
        self.payables_horizontalLayout.setObjectName(u"payables_horizontalLayout")
        self.payables_horizontalLayout.setContentsMargins(17, 5, 10, 5)
        self.time_label = QLabel(self.payables_tab)
        self.time_label.setObjectName(u"time_label")
        sizePolicy4 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.time_label.sizePolicy().hasHeightForWidth())
        self.time_label.setSizePolicy(sizePolicy4)
        self.time_label.setMaximumSize(QSize(100, 16777215))
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.time_label.setFont(font)
        self.time_label.setLayoutDirection(Qt.LeftToRight)
        self.time_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.payables_horizontalLayout.addWidget(self.time_label)

        self.s_year_lineEdit = QLineEdit(self.payables_tab)
        self.s_year_lineEdit.setObjectName(u"s_year_lineEdit")
        sizePolicy1.setHeightForWidth(self.s_year_lineEdit.sizePolicy().hasHeightForWidth())
        self.s_year_lineEdit.setSizePolicy(sizePolicy1)
        self.s_year_lineEdit.setMaximumSize(QSize(50, 16777215))
        self.s_year_lineEdit.setMouseTracking(False)
        self.s_year_lineEdit.setAlignment(Qt.AlignCenter)

        self.payables_horizontalLayout.addWidget(self.s_year_lineEdit)

        self.s_year_label = QLabel(self.payables_tab)
        self.s_year_label.setObjectName(u"s_year_label")
        sizePolicy4.setHeightForWidth(self.s_year_label.sizePolicy().hasHeightForWidth())
        self.s_year_label.setSizePolicy(sizePolicy4)
        self.s_year_label.setMaximumSize(QSize(10, 16777215))
        self.s_year_label.setLayoutDirection(Qt.LeftToRight)
        self.s_year_label.setAlignment(Qt.AlignCenter)

        self.payables_horizontalLayout.addWidget(self.s_year_label)

        self.s_month_lineEdit = QLineEdit(self.payables_tab)
        self.s_month_lineEdit.setObjectName(u"s_month_lineEdit")
        sizePolicy1.setHeightForWidth(self.s_month_lineEdit.sizePolicy().hasHeightForWidth())
        self.s_month_lineEdit.setSizePolicy(sizePolicy1)
        self.s_month_lineEdit.setMaximumSize(QSize(20, 16777215))
        self.s_month_lineEdit.setAlignment(Qt.AlignCenter)

        self.payables_horizontalLayout.addWidget(self.s_month_lineEdit)

        self.s_month_label = QLabel(self.payables_tab)
        self.s_month_label.setObjectName(u"s_month_label")
        sizePolicy4.setHeightForWidth(self.s_month_label.sizePolicy().hasHeightForWidth())
        self.s_month_label.setSizePolicy(sizePolicy4)
        self.s_month_label.setMaximumSize(QSize(30, 16777215))
        self.s_month_label.setLayoutDirection(Qt.LeftToRight)
        self.s_month_label.setAlignment(Qt.AlignCenter)

        self.payables_horizontalLayout.addWidget(self.s_month_label)

        self.e_year_lineEdit = QLineEdit(self.payables_tab)
        self.e_year_lineEdit.setObjectName(u"e_year_lineEdit")
        sizePolicy1.setHeightForWidth(self.e_year_lineEdit.sizePolicy().hasHeightForWidth())
        self.e_year_lineEdit.setSizePolicy(sizePolicy1)
        self.e_year_lineEdit.setMaximumSize(QSize(50, 16777215))
        self.e_year_lineEdit.setAlignment(Qt.AlignCenter)

        self.payables_horizontalLayout.addWidget(self.e_year_lineEdit)

        self.e_year_label = QLabel(self.payables_tab)
        self.e_year_label.setObjectName(u"e_year_label")
        sizePolicy4.setHeightForWidth(self.e_year_label.sizePolicy().hasHeightForWidth())
        self.e_year_label.setSizePolicy(sizePolicy4)
        self.e_year_label.setMaximumSize(QSize(10, 16777215))
        self.e_year_label.setLayoutDirection(Qt.LeftToRight)
        self.e_year_label.setAlignment(Qt.AlignCenter)

        self.payables_horizontalLayout.addWidget(self.e_year_label)

        self.e_month_lineEdit = QLineEdit(self.payables_tab)
        self.e_month_lineEdit.setObjectName(u"e_month_lineEdit")
        sizePolicy1.setHeightForWidth(self.e_month_lineEdit.sizePolicy().hasHeightForWidth())
        self.e_month_lineEdit.setSizePolicy(sizePolicy1)
        self.e_month_lineEdit.setMaximumSize(QSize(20, 16777215))
        self.e_month_lineEdit.setAlignment(Qt.AlignCenter)
        self.e_month_lineEdit.setCursorMoveStyle(Qt.LogicalMoveStyle)

        self.payables_horizontalLayout.addWidget(self.e_month_lineEdit)

        self.e_month_label = QLabel(self.payables_tab)
        self.e_month_label.setObjectName(u"e_month_label")
        sizePolicy4.setHeightForWidth(self.e_month_label.sizePolicy().hasHeightForWidth())
        self.e_month_label.setSizePolicy(sizePolicy4)
        self.e_month_label.setMaximumSize(QSize(10, 16777215))
        self.e_month_label.setLayoutDirection(Qt.LeftToRight)
        self.e_month_label.setAlignment(Qt.AlignCenter)

        self.payables_horizontalLayout.addWidget(self.e_month_label)

        self.job_label = QLabel(self.payables_tab)
        self.job_label.setObjectName(u"job_label")
        sizePolicy4.setHeightForWidth(self.job_label.sizePolicy().hasHeightForWidth())
        self.job_label.setSizePolicy(sizePolicy4)
        self.job_label.setMinimumSize(QSize(0, 0))
        self.job_label.setMaximumSize(QSize(50, 16777215))
        self.job_label.setFont(font)
        self.job_label.setLayoutDirection(Qt.LeftToRight)
        self.job_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.payables_horizontalLayout.addWidget(self.job_label)

        self.job_lineEdit = QLineEdit(self.payables_tab)
        self.job_lineEdit.setObjectName(u"job_lineEdit")
        sizePolicy1.setHeightForWidth(self.job_lineEdit.sizePolicy().hasHeightForWidth())
        self.job_lineEdit.setSizePolicy(sizePolicy1)
        self.job_lineEdit.setMinimumSize(QSize(0, 0))
        self.job_lineEdit.setMaximumSize(QSize(60, 16777215))
        self.job_lineEdit.setAlignment(Qt.AlignCenter)

        self.payables_horizontalLayout.addWidget(self.job_lineEdit)

        self.subject_label = QLabel(self.payables_tab)
        self.subject_label.setObjectName(u"subject_label")
        sizePolicy4.setHeightForWidth(self.subject_label.sizePolicy().hasHeightForWidth())
        self.subject_label.setSizePolicy(sizePolicy4)
        self.subject_label.setMinimumSize(QSize(0, 0))
        self.subject_label.setMaximumSize(QSize(50, 16777215))
        self.subject_label.setFont(font)
        self.subject_label.setLayoutDirection(Qt.LeftToRight)
        self.subject_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.payables_horizontalLayout.addWidget(self.subject_label)

        self.subject_lineEdit = QLineEdit(self.payables_tab)
        self.subject_lineEdit.setObjectName(u"subject_lineEdit")
        sizePolicy1.setHeightForWidth(self.subject_lineEdit.sizePolicy().hasHeightForWidth())
        self.subject_lineEdit.setSizePolicy(sizePolicy1)
        self.subject_lineEdit.setMinimumSize(QSize(0, 0))
        self.subject_lineEdit.setMaximumSize(QSize(60, 16777215))
        self.subject_lineEdit.setAlignment(Qt.AlignCenter)

        self.payables_horizontalLayout.addWidget(self.subject_lineEdit)

        self.payables_horizontalLayout.setStretch(0, 1)
        self.payables_horizontalLayout.setStretch(1, 1)
        self.payables_horizontalLayout.setStretch(2, 1)
        self.payables_horizontalLayout.setStretch(3, 1)
        self.payables_horizontalLayout.setStretch(4, 1)
        self.payables_horizontalLayout.setStretch(5, 1)
        self.payables_horizontalLayout.setStretch(6, 1)
        self.payables_horizontalLayout.setStretch(7, 1)
        self.payables_horizontalLayout.setStretch(8, 1)
        self.payables_horizontalLayout.setStretch(11, 1)
        self.payables_horizontalLayout.setStretch(12, 2)

        self.verticalLayout_2.addLayout(self.payables_horizontalLayout)

        self.download_horizontalLayout = QHBoxLayout()
        self.download_horizontalLayout.setSpacing(5)
        self.download_horizontalLayout.setObjectName(u"download_horizontalLayout")
        self.download_horizontalLayout.setContentsMargins(6, 5, 10, 5)
        self.save_path_label = QLabel(self.payables_tab)
        self.save_path_label.setObjectName(u"save_path_label")
        sizePolicy4.setHeightForWidth(self.save_path_label.sizePolicy().hasHeightForWidth())
        self.save_path_label.setSizePolicy(sizePolicy4)
        self.save_path_label.setMaximumSize(QSize(60, 16777215))
        self.save_path_label.setFont(font)
        self.save_path_label.setLayoutDirection(Qt.LeftToRight)
        self.save_path_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.download_horizontalLayout.addWidget(self.save_path_label)

        self.save_path_pushButton = QPushButton(self.payables_tab)
        self.save_path_pushButton.setObjectName(u"save_path_pushButton")
        sizePolicy1.setHeightForWidth(self.save_path_pushButton.sizePolicy().hasHeightForWidth())
        self.save_path_pushButton.setSizePolicy(sizePolicy1)
        self.save_path_pushButton.setMaximumSize(QSize(600, 16777215))
        font1 = QFont()
        font1.setFamily(u"\u6977\u4f53")
        font1.setPointSize(11)
        self.save_path_pushButton.setFont(font1)

        self.download_horizontalLayout.addWidget(self.save_path_pushButton)

        self.download_payables_pushButton = QPushButton(self.payables_tab)
        self.download_payables_pushButton.setObjectName(u"download_payables_pushButton")
        sizePolicy1.setHeightForWidth(self.download_payables_pushButton.sizePolicy().hasHeightForWidth())
        self.download_payables_pushButton.setSizePolicy(sizePolicy1)
        self.download_payables_pushButton.setMaximumSize(QSize(100, 16777215))

        self.download_horizontalLayout.addWidget(self.download_payables_pushButton)

        self.download_horizontalLayout.setStretch(0, 1)
        self.download_horizontalLayout.setStretch(1, 10)
        self.download_horizontalLayout.setStretch(2, 2)

        self.verticalLayout_2.addLayout(self.download_horizontalLayout)


        self.gridLayout_3.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.tabWidget.addTab(self.payables_tab, "")
        self.adjust_tab = QWidget()
        self.adjust_tab.setObjectName(u"adjust_tab")
        self.gridLayout_4 = QGridLayout(self.adjust_tab)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.adjust_pushButton = QPushButton(self.adjust_tab)
        self.adjust_pushButton.setObjectName(u"adjust_pushButton")
        sizePolicy.setHeightForWidth(self.adjust_pushButton.sizePolicy().hasHeightForWidth())
        self.adjust_pushButton.setSizePolicy(sizePolicy)

        self.gridLayout_4.addWidget(self.adjust_pushButton, 0, 0, 1, 1)

        self.tabWidget.addTab(self.adjust_tab, "")
        self.cust_ctrl_tab = QWidget()
        self.cust_ctrl_tab.setObjectName(u"cust_ctrl_tab")
        self.gridLayout_5 = QGridLayout(self.cust_ctrl_tab)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.cust_ctrl_pushButton = QPushButton(self.cust_ctrl_tab)
        self.cust_ctrl_pushButton.setObjectName(u"cust_ctrl_pushButton")
        sizePolicy.setHeightForWidth(self.cust_ctrl_pushButton.sizePolicy().hasHeightForWidth())
        self.cust_ctrl_pushButton.setSizePolicy(sizePolicy)

        self.gridLayout_5.addWidget(self.cust_ctrl_pushButton, 0, 0, 1, 1)

        self.tabWidget.addTab(self.cust_ctrl_tab, "")
        self.test_tab = QWidget()
        self.test_tab.setObjectName(u"test_tab")
        self.gridLayout_6 = QGridLayout(self.test_tab)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.test_pushButton = QPushButton(self.test_tab)
        self.test_pushButton.setObjectName(u"test_pushButton")
        sizePolicy.setHeightForWidth(self.test_pushButton.sizePolicy().hasHeightForWidth())
        self.test_pushButton.setSizePolicy(sizePolicy)

        self.gridLayout_6.addWidget(self.test_pushButton, 0, 0, 1, 1)

        self.tabWidget.addTab(self.test_tab, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 2)

        self.size_label = QLabel(self.centralwidget)
        self.size_label.setObjectName(u"size_label")
        self.size_label.setMaximumSize(QSize(200, 16777215))
        self.size_label.setLayoutDirection(Qt.LeftToRight)
        self.size_label.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)

        self.gridLayout.addWidget(self.size_label, 2, 1, 1, 1)

        self.gridLayout.setRowStretch(0, 3)
        self.gridLayout.setRowStretch(1, 7)
        self.gridLayout.setRowStretch(2, 7)
        self.gridLayout.setColumnStretch(0, 4)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnMinimumWidth(0, 4)
        self.gridLayout.setColumnMinimumWidth(1, 1)
        self.gridLayout.setRowMinimumHeight(0, 4)
        self.gridLayout.setRowMinimumHeight(1, 1)
        self.gridLayout.setRowMinimumHeight(2, 1)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 581, 23))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        font2 = QFont()
        font2.setFamily(u"\u6977\u4f53")
        font2.setPointSize(14)
        self.statusbar.setFont(font2)
        self.statusbar.setLayoutDirection(Qt.LeftToRight)
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
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.x_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.y_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.textBrowser.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'SimSun'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">\u6b22\u8fce\u4f7f\u7528\u8d22\u52a1\u5c0f\u5de5\u5177</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt;\"><br /></p></body></html>", None))
        self.time_label.setText(QCoreApplication.translate("MainWindow", u"\u671f\u95f4", None))
        self.s_year_lineEdit.setText(QCoreApplication.translate("MainWindow", u"2019", None))
        self.s_year_label.setText(QCoreApplication.translate("MainWindow", u"\u5e74", None))
        self.s_month_lineEdit.setText(QCoreApplication.translate("MainWindow", u"03", None))
        self.s_month_label.setText(QCoreApplication.translate("MainWindow", u"\u6708  -", None))
        self.e_year_lineEdit.setText(QCoreApplication.translate("MainWindow", u"2020", None))
        self.e_year_label.setText(QCoreApplication.translate("MainWindow", u"\u5e74", None))
        self.e_month_lineEdit.setText(QCoreApplication.translate("MainWindow", u"02", None))
        self.e_month_label.setText(QCoreApplication.translate("MainWindow", u"\u6708", None))
        self.job_label.setText(QCoreApplication.translate("MainWindow", u"    \u4f5c\u4e1a", None))
        self.subject_label.setText(QCoreApplication.translate("MainWindow", u"\u79d1\u76ee", None))
        self.save_path_label.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u8def\u5f84", None))
        self.save_path_pushButton.setText("")
        self.download_payables_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u8f7d", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.payables_tab), QCoreApplication.translate("MainWindow", u"\u5e94\u6536/\u4ed8\u6b3e", None))
        self.adjust_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u8ba2\u5355\u8c03\u6574", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.adjust_tab), QCoreApplication.translate("MainWindow", u"\u5185\u90e8\u8ba2\u5355\u8c03\u6574", None))
        self.cust_ctrl_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.cust_ctrl_tab), QCoreApplication.translate("MainWindow", u"\u81ea\u5b9a\u4e49\u63a7\u5236", None))
        self.test_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u6d4b\u8bd5", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.test_tab), QCoreApplication.translate("MainWindow", u"\u6d4b\u8bd5", None))
        self.size_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"help", None))
#if QT_CONFIG(accessibility)
        self.statusbar.setAccessibleName(QCoreApplication.translate("MainWindow", u"123", None))
#endif // QT_CONFIG(accessibility)
    # retranslateUi

