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
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.size_label = QLabel(self.centralwidget)
        self.size_label.setObjectName(u"size_label")
        self.size_label.setMaximumSize(QSize(100, 16777215))
        self.size_label.setLayoutDirection(Qt.LeftToRight)
        self.size_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.size_label, 0, 1, 1, 1)

        self.mouse_label = QLabel(self.centralwidget)
        self.mouse_label.setObjectName(u"mouse_label")
        self.mouse_label.setMaximumSize(QSize(100, 16777215))
        self.mouse_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.mouse_label, 0, 2, 1, 1)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(200, 16777215))
        self.label.setLayoutDirection(Qt.LeftToRight)
        self.label.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)

        self.gridLayout_8.addWidget(self.label, 0, 0, 1, 1)

        self.gridLayout_8.setColumnStretch(0, 5)
        self.gridLayout_8.setColumnStretch(1, 1)
        self.gridLayout_8.setColumnStretch(2, 1)

        self.gridLayout.addLayout(self.gridLayout_8, 2, 0, 1, 1)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy1)
        self.tabWidget.setMaximumSize(QSize(800, 600))
        self.payables_tab = QWidget()
        self.payables_tab.setObjectName(u"payables_tab")
        self.formLayout = QFormLayout(self.payables_tab)
        self.formLayout.setObjectName(u"formLayout")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setSpacing(5)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout_3.setContentsMargins(5, 5, 5, 5)
        self.subject_lineEdit = QLineEdit(self.payables_tab)
        self.subject_lineEdit.setObjectName(u"subject_lineEdit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.subject_lineEdit.sizePolicy().hasHeightForWidth())
        self.subject_lineEdit.setSizePolicy(sizePolicy2)
        self.subject_lineEdit.setMinimumSize(QSize(0, 0))
        self.subject_lineEdit.setMaximumSize(QSize(480, 16777215))
        self.subject_lineEdit.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.subject_lineEdit, 1, 6, 1, 4)

        self.subject_label = QLabel(self.payables_tab)
        self.subject_label.setObjectName(u"subject_label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.subject_label.sizePolicy().hasHeightForWidth())
        self.subject_label.setSizePolicy(sizePolicy3)
        self.subject_label.setMinimumSize(QSize(0, 0))
        self.subject_label.setMaximumSize(QSize(50, 16777215))
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.subject_label.setFont(font)
        self.subject_label.setLayoutDirection(Qt.LeftToRight)
        self.subject_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.subject_label, 1, 5, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.s_year_lineEdit = QLineEdit(self.payables_tab)
        self.s_year_lineEdit.setObjectName(u"s_year_lineEdit")
        sizePolicy.setHeightForWidth(self.s_year_lineEdit.sizePolicy().hasHeightForWidth())
        self.s_year_lineEdit.setSizePolicy(sizePolicy)
        self.s_year_lineEdit.setMaximumSize(QSize(40, 16777215))
        self.s_year_lineEdit.setMouseTracking(False)
        self.s_year_lineEdit.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.s_year_lineEdit)

        self.s_year_label = QLabel(self.payables_tab)
        self.s_year_label.setObjectName(u"s_year_label")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.s_year_label.sizePolicy().hasHeightForWidth())
        self.s_year_label.setSizePolicy(sizePolicy4)
        self.s_year_label.setMaximumSize(QSize(10, 16777215))
        self.s_year_label.setLayoutDirection(Qt.LeftToRight)
        self.s_year_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.s_year_label)

        self.s_month_lineEdit = QLineEdit(self.payables_tab)
        self.s_month_lineEdit.setObjectName(u"s_month_lineEdit")
        sizePolicy.setHeightForWidth(self.s_month_lineEdit.sizePolicy().hasHeightForWidth())
        self.s_month_lineEdit.setSizePolicy(sizePolicy)
        self.s_month_lineEdit.setMaximumSize(QSize(25, 16777215))
        self.s_month_lineEdit.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.s_month_lineEdit)

        self.s_month_label = QLabel(self.payables_tab)
        self.s_month_label.setObjectName(u"s_month_label")
        sizePolicy3.setHeightForWidth(self.s_month_label.sizePolicy().hasHeightForWidth())
        self.s_month_label.setSizePolicy(sizePolicy3)
        self.s_month_label.setMaximumSize(QSize(30, 16777215))
        self.s_month_label.setLayoutDirection(Qt.LeftToRight)
        self.s_month_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.s_month_label)

        self.e_year_lineEdit = QLineEdit(self.payables_tab)
        self.e_year_lineEdit.setObjectName(u"e_year_lineEdit")
        sizePolicy.setHeightForWidth(self.e_year_lineEdit.sizePolicy().hasHeightForWidth())
        self.e_year_lineEdit.setSizePolicy(sizePolicy)
        self.e_year_lineEdit.setMaximumSize(QSize(40, 16777215))
        self.e_year_lineEdit.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.e_year_lineEdit)

        self.e_year_label = QLabel(self.payables_tab)
        self.e_year_label.setObjectName(u"e_year_label")
        sizePolicy4.setHeightForWidth(self.e_year_label.sizePolicy().hasHeightForWidth())
        self.e_year_label.setSizePolicy(sizePolicy4)
        self.e_year_label.setMaximumSize(QSize(10, 16777215))
        self.e_year_label.setLayoutDirection(Qt.LeftToRight)
        self.e_year_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.e_year_label)

        self.e_month_lineEdit = QLineEdit(self.payables_tab)
        self.e_month_lineEdit.setObjectName(u"e_month_lineEdit")
        sizePolicy.setHeightForWidth(self.e_month_lineEdit.sizePolicy().hasHeightForWidth())
        self.e_month_lineEdit.setSizePolicy(sizePolicy)
        self.e_month_lineEdit.setMaximumSize(QSize(25, 16777215))
        self.e_month_lineEdit.setAlignment(Qt.AlignCenter)
        self.e_month_lineEdit.setCursorMoveStyle(Qt.LogicalMoveStyle)

        self.horizontalLayout_2.addWidget(self.e_month_lineEdit)

        self.e_month_label = QLabel(self.payables_tab)
        self.e_month_label.setObjectName(u"e_month_label")
        sizePolicy4.setHeightForWidth(self.e_month_label.sizePolicy().hasHeightForWidth())
        self.e_month_label.setSizePolicy(sizePolicy4)
        self.e_month_label.setMaximumSize(QSize(10, 16777215))
        self.e_month_label.setLayoutDirection(Qt.LeftToRight)
        self.e_month_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.e_month_label)


        self.gridLayout_3.addLayout(self.horizontalLayout_2, 0, 1, 1, 5)

        self.merge_payables_pushButton = QPushButton(self.payables_tab)
        self.merge_payables_pushButton.setObjectName(u"merge_payables_pushButton")
        sizePolicy.setHeightForWidth(self.merge_payables_pushButton.sizePolicy().hasHeightForWidth())
        self.merge_payables_pushButton.setSizePolicy(sizePolicy)
        self.merge_payables_pushButton.setMaximumSize(QSize(50, 16777215))

        self.gridLayout_3.addWidget(self.merge_payables_pushButton, 0, 9, 1, 1)

        self.job_lineEdit = QLineEdit(self.payables_tab)
        self.job_lineEdit.setObjectName(u"job_lineEdit")
        sizePolicy.setHeightForWidth(self.job_lineEdit.sizePolicy().hasHeightForWidth())
        self.job_lineEdit.setSizePolicy(sizePolicy)
        self.job_lineEdit.setMinimumSize(QSize(0, 0))
        self.job_lineEdit.setMaximumSize(QSize(500, 16777215))
        self.job_lineEdit.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.job_lineEdit, 1, 1, 1, 4)

        self.save_path_label = QLabel(self.payables_tab)
        self.save_path_label.setObjectName(u"save_path_label")
        sizePolicy4.setHeightForWidth(self.save_path_label.sizePolicy().hasHeightForWidth())
        self.save_path_label.setSizePolicy(sizePolicy4)
        self.save_path_label.setMaximumSize(QSize(50, 16777215))
        self.save_path_label.setFont(font)
        self.save_path_label.setLayoutDirection(Qt.LeftToRight)
        self.save_path_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.save_path_label, 2, 0, 1, 1)

        self.job_label = QLabel(self.payables_tab)
        self.job_label.setObjectName(u"job_label")
        sizePolicy3.setHeightForWidth(self.job_label.sizePolicy().hasHeightForWidth())
        self.job_label.setSizePolicy(sizePolicy3)
        self.job_label.setMinimumSize(QSize(0, 0))
        self.job_label.setMaximumSize(QSize(50, 16777215))
        self.job_label.setFont(font)
        self.job_label.setLayoutDirection(Qt.LeftToRight)
        self.job_label.setScaledContents(False)
        self.job_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.job_label, 1, 0, 1, 1)

        self.export_payables_pushButton = QPushButton(self.payables_tab)
        self.export_payables_pushButton.setObjectName(u"export_payables_pushButton")
        self.export_payables_pushButton.setEnabled(False)
        sizePolicy.setHeightForWidth(self.export_payables_pushButton.sizePolicy().hasHeightForWidth())
        self.export_payables_pushButton.setSizePolicy(sizePolicy)
        self.export_payables_pushButton.setMaximumSize(QSize(50, 16777215))

        self.gridLayout_3.addWidget(self.export_payables_pushButton, 0, 8, 1, 1)

        self.filter_payables_pushButton = QPushButton(self.payables_tab)
        self.filter_payables_pushButton.setObjectName(u"filter_payables_pushButton")
        self.filter_payables_pushButton.setEnabled(False)
        sizePolicy.setHeightForWidth(self.filter_payables_pushButton.sizePolicy().hasHeightForWidth())
        self.filter_payables_pushButton.setSizePolicy(sizePolicy)
        self.filter_payables_pushButton.setMaximumSize(QSize(50, 16777215))

        self.gridLayout_3.addWidget(self.filter_payables_pushButton, 0, 7, 1, 1)

        self.login_payables_pushButton = QPushButton(self.payables_tab)
        self.login_payables_pushButton.setObjectName(u"login_payables_pushButton")
        sizePolicy.setHeightForWidth(self.login_payables_pushButton.sizePolicy().hasHeightForWidth())
        self.login_payables_pushButton.setSizePolicy(sizePolicy)
        self.login_payables_pushButton.setMaximumSize(QSize(50, 16777215))

        self.gridLayout_3.addWidget(self.login_payables_pushButton, 0, 6, 1, 1)

        self.download_payables_pushButton = QPushButton(self.payables_tab)
        self.download_payables_pushButton.setObjectName(u"download_payables_pushButton")
        sizePolicy.setHeightForWidth(self.download_payables_pushButton.sizePolicy().hasHeightForWidth())
        self.download_payables_pushButton.setSizePolicy(sizePolicy)
        self.download_payables_pushButton.setMaximumSize(QSize(50, 16777215))

        self.gridLayout_3.addWidget(self.download_payables_pushButton, 2, 9, 1, 1)

        self.save_path_pushButton = QPushButton(self.payables_tab)
        self.save_path_pushButton.setObjectName(u"save_path_pushButton")
        sizePolicy.setHeightForWidth(self.save_path_pushButton.sizePolicy().hasHeightForWidth())
        self.save_path_pushButton.setSizePolicy(sizePolicy)
        self.save_path_pushButton.setMaximumSize(QSize(800, 16777215))
        font1 = QFont()
        font1.setFamily(u"\u6977\u4f53")
        font1.setPointSize(11)
        self.save_path_pushButton.setFont(font1)

        self.gridLayout_3.addWidget(self.save_path_pushButton, 2, 1, 1, 8)

        self.time_label = QLabel(self.payables_tab)
        self.time_label.setObjectName(u"time_label")
        sizePolicy4.setHeightForWidth(self.time_label.sizePolicy().hasHeightForWidth())
        self.time_label.setSizePolicy(sizePolicy4)
        self.time_label.setMaximumSize(QSize(50, 16777215))
        self.time_label.setFont(font)
        self.time_label.setLayoutDirection(Qt.LeftToRight)
        self.time_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.time_label, 0, 0, 1, 1)

        self.gridLayout_3.setRowStretch(0, 1)
        self.gridLayout_3.setRowStretch(1, 1)
        self.gridLayout_3.setRowStretch(2, 1)
        self.gridLayout_3.setColumnStretch(0, 1)
        self.gridLayout_3.setColumnStretch(1, 1)
        self.gridLayout_3.setColumnStretch(2, 1)
        self.gridLayout_3.setColumnStretch(3, 1)
        self.gridLayout_3.setColumnStretch(4, 1)
        self.gridLayout_3.setColumnStretch(5, 1)
        self.gridLayout_3.setColumnStretch(6, 1)
        self.gridLayout_3.setColumnStretch(7, 1)
        self.gridLayout_3.setColumnStretch(8, 1)
        self.gridLayout_3.setColumnStretch(9, 1)
        self.gridLayout_3.setColumnMinimumWidth(0, 1)
        self.gridLayout_3.setColumnMinimumWidth(1, 1)
        self.gridLayout_3.setColumnMinimumWidth(2, 1)
        self.gridLayout_3.setColumnMinimumWidth(3, 1)
        self.gridLayout_3.setColumnMinimumWidth(4, 1)
        self.gridLayout_3.setColumnMinimumWidth(5, 1)
        self.gridLayout_3.setColumnMinimumWidth(6, 1)
        self.gridLayout_3.setColumnMinimumWidth(7, 1)
        self.gridLayout_3.setColumnMinimumWidth(8, 1)
        self.gridLayout_3.setColumnMinimumWidth(9, 1)
        self.gridLayout_3.setRowMinimumHeight(0, 1)
        self.gridLayout_3.setRowMinimumHeight(1, 1)
        self.gridLayout_3.setRowMinimumHeight(2, 1)

        self.formLayout.setLayout(0, QFormLayout.SpanningRole, self.gridLayout_3)

        self.treeWidget = QTreeWidget(self.payables_tab)
        self.treeWidget.setObjectName(u"treeWidget")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.treeWidget)

        self.tabWidget.addTab(self.payables_tab, "")
        self.other_tab = QWidget()
        self.other_tab.setObjectName(u"other_tab")
        self.layoutWidget_2 = QWidget(self.other_tab)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.layoutWidget_2.setGeometry(QRect(10, 10, 521, 41))
        self.gridLayout_5 = QGridLayout(self.layoutWidget_2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.merge_path_pushButton = QPushButton(self.layoutWidget_2)
        self.merge_path_pushButton.setObjectName(u"merge_path_pushButton")
        self.merge_path_pushButton.setEnabled(True)
        sizePolicy5 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.merge_path_pushButton.sizePolicy().hasHeightForWidth())
        self.merge_path_pushButton.setSizePolicy(sizePolicy5)
        self.merge_path_pushButton.setMaximumSize(QSize(400, 16777215))

        self.gridLayout_5.addWidget(self.merge_path_pushButton, 0, 0, 1, 1)

        self.merge_pushButton = QPushButton(self.layoutWidget_2)
        self.merge_pushButton.setObjectName(u"merge_pushButton")
        sizePolicy5.setHeightForWidth(self.merge_pushButton.sizePolicy().hasHeightForWidth())
        self.merge_pushButton.setSizePolicy(sizePolicy5)
        self.merge_pushButton.setMinimumSize(QSize(50, 0))
        self.merge_pushButton.setMaximumSize(QSize(70, 16777215))

        self.gridLayout_5.addWidget(self.merge_pushButton, 0, 1, 1, 1)

        self.tabWidget.addTab(self.other_tab, "")
        self.adjust_tab = QWidget()
        self.adjust_tab.setObjectName(u"adjust_tab")
        self.layoutWidget = QWidget(self.adjust_tab)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 541, 71))
        self.gridLayout_4 = QGridLayout(self.layoutWidget)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.blance_subject_lineEdit = QLineEdit(self.layoutWidget)
        self.blance_subject_lineEdit.setObjectName(u"blance_subject_lineEdit")
        sizePolicy.setHeightForWidth(self.blance_subject_lineEdit.sizePolicy().hasHeightForWidth())
        self.blance_subject_lineEdit.setSizePolicy(sizePolicy)
        self.blance_subject_lineEdit.setMaximumSize(QSize(150, 16777215))
        self.blance_subject_lineEdit.setMouseTracking(False)
        self.blance_subject_lineEdit.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.blance_subject_lineEdit, 1, 0, 1, 1)

        self.blance_month_lineEdit = QLineEdit(self.layoutWidget)
        self.blance_month_lineEdit.setObjectName(u"blance_month_lineEdit")
        sizePolicy.setHeightForWidth(self.blance_month_lineEdit.sizePolicy().hasHeightForWidth())
        self.blance_month_lineEdit.setSizePolicy(sizePolicy)
        self.blance_month_lineEdit.setMaximumSize(QSize(150, 16777215))
        self.blance_month_lineEdit.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.blance_month_lineEdit, 1, 1, 1, 1)

        self.fetch_pushButton = QPushButton(self.layoutWidget)
        self.fetch_pushButton.setObjectName(u"fetch_pushButton")
        sizePolicy.setHeightForWidth(self.fetch_pushButton.sizePolicy().hasHeightForWidth())
        self.fetch_pushButton.setSizePolicy(sizePolicy)

        self.gridLayout_4.addWidget(self.fetch_pushButton, 1, 2, 1, 1)

        self.fetch_file_pushButton = QPushButton(self.layoutWidget)
        self.fetch_file_pushButton.setObjectName(u"fetch_file_pushButton")
        self.fetch_file_pushButton.setEnabled(True)
        sizePolicy6 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.fetch_file_pushButton.sizePolicy().hasHeightForWidth())
        self.fetch_file_pushButton.setSizePolicy(sizePolicy6)
        self.fetch_file_pushButton.setMaximumSize(QSize(800, 16777215))

        self.gridLayout_4.addWidget(self.fetch_file_pushButton, 0, 0, 1, 3)

        self.tabWidget.addTab(self.adjust_tab, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.layoutWidget_3 = QWidget(self.tab)
        self.layoutWidget_3.setObjectName(u"layoutWidget_3")
        self.layoutWidget_3.setGeometry(QRect(20, 10, 521, 41))
        self.gridLayout_6 = QGridLayout(self.layoutWidget_3)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.database_fetch_path_pushButton = QPushButton(self.layoutWidget_3)
        self.database_fetch_path_pushButton.setObjectName(u"database_fetch_path_pushButton")
        self.database_fetch_path_pushButton.setEnabled(True)
        sizePolicy5.setHeightForWidth(self.database_fetch_path_pushButton.sizePolicy().hasHeightForWidth())
        self.database_fetch_path_pushButton.setSizePolicy(sizePolicy5)
        self.database_fetch_path_pushButton.setMaximumSize(QSize(400, 16777215))

        self.gridLayout_6.addWidget(self.database_fetch_path_pushButton, 0, 0, 1, 1)

        self.database_fetch_pushButton = QPushButton(self.layoutWidget_3)
        self.database_fetch_pushButton.setObjectName(u"database_fetch_pushButton")
        sizePolicy5.setHeightForWidth(self.database_fetch_pushButton.sizePolicy().hasHeightForWidth())
        self.database_fetch_pushButton.setSizePolicy(sizePolicy5)
        self.database_fetch_pushButton.setMinimumSize(QSize(50, 0))
        self.database_fetch_pushButton.setMaximumSize(QSize(70, 16777215))

        self.gridLayout_6.addWidget(self.database_fetch_pushButton, 0, 1, 1, 1)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.layoutWidget_4 = QWidget(self.tab_2)
        self.layoutWidget_4.setObjectName(u"layoutWidget_4")
        self.layoutWidget_4.setGeometry(QRect(20, 10, 521, 54))
        self.gridLayout_7 = QGridLayout(self.layoutWidget_4)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.merge_expense_path_pushButton = QPushButton(self.layoutWidget_4)
        self.merge_expense_path_pushButton.setObjectName(u"merge_expense_path_pushButton")
        self.merge_expense_path_pushButton.setEnabled(True)
        sizePolicy5.setHeightForWidth(self.merge_expense_path_pushButton.sizePolicy().hasHeightForWidth())
        self.merge_expense_path_pushButton.setSizePolicy(sizePolicy5)
        self.merge_expense_path_pushButton.setMaximumSize(QSize(400, 16777215))

        self.gridLayout_7.addWidget(self.merge_expense_path_pushButton, 0, 0, 1, 1)

        self.merge_expense_file_pushButton = QPushButton(self.layoutWidget_4)
        self.merge_expense_file_pushButton.setObjectName(u"merge_expense_file_pushButton")
        self.merge_expense_file_pushButton.setEnabled(True)
        sizePolicy5.setHeightForWidth(self.merge_expense_file_pushButton.sizePolicy().hasHeightForWidth())
        self.merge_expense_file_pushButton.setSizePolicy(sizePolicy5)
        self.merge_expense_file_pushButton.setMaximumSize(QSize(400, 16777215))

        self.gridLayout_7.addWidget(self.merge_expense_file_pushButton, 1, 0, 1, 1)

        self.merge_expense_pushButton = QPushButton(self.layoutWidget_4)
        self.merge_expense_pushButton.setObjectName(u"merge_expense_pushButton")
        sizePolicy5.setHeightForWidth(self.merge_expense_pushButton.sizePolicy().hasHeightForWidth())
        self.merge_expense_pushButton.setSizePolicy(sizePolicy5)
        self.merge_expense_pushButton.setMinimumSize(QSize(50, 0))
        self.merge_expense_pushButton.setMaximumSize(QSize(70, 16777215))

        self.gridLayout_7.addWidget(self.merge_expense_pushButton, 1, 1, 1, 1)

        self.merge_expense_month_lineEdit = QLineEdit(self.layoutWidget_4)
        self.merge_expense_month_lineEdit.setObjectName(u"merge_expense_month_lineEdit")
        sizePolicy.setHeightForWidth(self.merge_expense_month_lineEdit.sizePolicy().hasHeightForWidth())
        self.merge_expense_month_lineEdit.setSizePolicy(sizePolicy)
        self.merge_expense_month_lineEdit.setMaximumSize(QSize(70, 16777215))
        self.merge_expense_month_lineEdit.setMouseTracking(False)
        self.merge_expense_month_lineEdit.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.merge_expense_month_lineEdit, 0, 1, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.layoutWidget_5 = QWidget(self.tab_3)
        self.layoutWidget_5.setObjectName(u"layoutWidget_5")
        self.layoutWidget_5.setGeometry(QRect(20, 10, 521, 54))
        self.gridLayout_9 = QGridLayout(self.layoutWidget_5)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.hyperlink_file_pushButton = QPushButton(self.layoutWidget_5)
        self.hyperlink_file_pushButton.setObjectName(u"hyperlink_file_pushButton")
        self.hyperlink_file_pushButton.setEnabled(True)
        sizePolicy5.setHeightForWidth(self.hyperlink_file_pushButton.sizePolicy().hasHeightForWidth())
        self.hyperlink_file_pushButton.setSizePolicy(sizePolicy5)
        self.hyperlink_file_pushButton.setMaximumSize(QSize(400, 16777215))

        self.gridLayout_9.addWidget(self.hyperlink_file_pushButton, 0, 0, 1, 1)

        self.hyperlink_pushButton = QPushButton(self.layoutWidget_5)
        self.hyperlink_pushButton.setObjectName(u"hyperlink_pushButton")
        sizePolicy5.setHeightForWidth(self.hyperlink_pushButton.sizePolicy().hasHeightForWidth())
        self.hyperlink_pushButton.setSizePolicy(sizePolicy5)
        self.hyperlink_pushButton.setMinimumSize(QSize(50, 0))
        self.hyperlink_pushButton.setMaximumSize(QSize(70, 16777215))

        self.gridLayout_9.addWidget(self.hyperlink_pushButton, 0, 1, 1, 1)

        self.tabWidget.addTab(self.tab_3, "")

        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)

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
        self.size_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.mouse_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label.setText("")
#if QT_CONFIG(tooltip)
        self.tabWidget.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.tabWidget.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
#if QT_CONFIG(accessibility)
        self.tabWidget.setAccessibleDescription(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u76ee\u7684\u6587\u4ef6", None))
#endif // QT_CONFIG(accessibility)
        self.subject_label.setText(QCoreApplication.translate("MainWindow", u"\u79d1\u76ee", None))
        self.s_year_lineEdit.setText(QCoreApplication.translate("MainWindow", u"2019", None))
        self.s_year_label.setText(QCoreApplication.translate("MainWindow", u"\u5e74", None))
        self.s_month_lineEdit.setText(QCoreApplication.translate("MainWindow", u"03", None))
        self.s_month_label.setText(QCoreApplication.translate("MainWindow", u"\u6708  -", None))
        self.e_year_lineEdit.setText(QCoreApplication.translate("MainWindow", u"2020", None))
        self.e_year_label.setText(QCoreApplication.translate("MainWindow", u"\u5e74", None))
        self.e_month_lineEdit.setText(QCoreApplication.translate("MainWindow", u"02", None))
        self.e_month_label.setText(QCoreApplication.translate("MainWindow", u"\u6708", None))
        self.merge_payables_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u5408\u5e76", None))
        self.save_path_label.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u8def\u5f84", None))
        self.job_label.setText(QCoreApplication.translate("MainWindow", u"\u4f5c\u4e1a", None))
        self.export_payables_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u51fa", None))
        self.filter_payables_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u8fc7\u6ee4", None))
        self.login_payables_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u767b\u5165", None))
        self.download_payables_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u8f7d", None))
        self.save_path_pushButton.setText("")
        self.time_label.setText(QCoreApplication.translate("MainWindow", u"\u671f\u95f4", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("MainWindow", u"4", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("MainWindow", u"3", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"2", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"1", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.payables_tab), QCoreApplication.translate("MainWindow", u"\u5e94\u6536/\u4ed8\u6b3e", None))
#if QT_CONFIG(statustip)
        self.merge_path_pushButton.setStatusTip(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u9700\u8981\u5408\u5e76\u7684\u6587\u4ef6\u5939", None))
#endif // QT_CONFIG(statustip)
        self.merge_path_pushButton.setText("")
        self.merge_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u5408\u5e76", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.other_tab), QCoreApplication.translate("MainWindow", u"\u5408\u5e76\u5de5\u4f5c\u7c3f", None))
#if QT_CONFIG(tooltip)
        self.blance_subject_lineEdit.setToolTip(QCoreApplication.translate("MainWindow", u"\u586b\u5199\u9879\u76ee", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.blance_subject_lineEdit.setStatusTip(QCoreApplication.translate("MainWindow", u"\u586b\u5199\u9879\u76ee", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.blance_subject_lineEdit.setWhatsThis(QCoreApplication.translate("MainWindow", u"\u586b\u5199\u9879\u76ee", None))
#endif // QT_CONFIG(whatsthis)
        self.blance_subject_lineEdit.setText("")
#if QT_CONFIG(tooltip)
        self.blance_month_lineEdit.setToolTip(QCoreApplication.translate("MainWindow", u"\u586b\u5199\u6708\u4efd", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.blance_month_lineEdit.setStatusTip(QCoreApplication.translate("MainWindow", u"\u586b\u5199\u6708\u4efd", None))
#endif // QT_CONFIG(statustip)
        self.blance_month_lineEdit.setText("")
        self.fetch_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u63d0\u53d6", None))
#if QT_CONFIG(statustip)
        self.fetch_file_pushButton.setStatusTip(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u9700\u8981\u63d0\u53d6\u7684\u6587\u4ef6", None))
#endif // QT_CONFIG(statustip)
        self.fetch_file_pushButton.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.adjust_tab), QCoreApplication.translate("MainWindow", u"\u63d0\u53d6", None))
#if QT_CONFIG(statustip)
        self.database_fetch_path_pushButton.setStatusTip(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6570\u636e\u6e90\u6587\u4ef6\u5939", None))
#endif // QT_CONFIG(statustip)
        self.database_fetch_path_pushButton.setText("")
        self.database_fetch_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u63d0\u53d6", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\u6570\u636e\u5e93SAP", None))
#if QT_CONFIG(statustip)
        self.merge_expense_path_pushButton.setStatusTip(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6570\u636e\u6e90\u6587\u4ef6\u5939", None))
#endif // QT_CONFIG(statustip)
        self.merge_expense_path_pushButton.setText("")
#if QT_CONFIG(statustip)
        self.merge_expense_file_pushButton.setStatusTip(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u76ee\u7684\u6587\u4ef6", None))
#endif // QT_CONFIG(statustip)
        self.merge_expense_file_pushButton.setText("")
        self.merge_expense_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u5408\u5e76", None))
#if QT_CONFIG(tooltip)
        self.merge_expense_month_lineEdit.setToolTip(QCoreApplication.translate("MainWindow", u"\u586b\u5199\u9879\u76ee", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.merge_expense_month_lineEdit.setStatusTip(QCoreApplication.translate("MainWindow", u"\u586b\u5199\u9879\u76ee", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.merge_expense_month_lineEdit.setWhatsThis(QCoreApplication.translate("MainWindow", u"\u586b\u5199\u9879\u76ee", None))
#endif // QT_CONFIG(whatsthis)
        self.merge_expense_month_lineEdit.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\u5408\u5e76\u8d39\u7528\u62a5\u8868", None))
#if QT_CONFIG(statustip)
        self.hyperlink_file_pushButton.setStatusTip(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u76ee\u7684\u6587\u4ef6", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.hyperlink_file_pushButton.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.hyperlink_file_pushButton.setText("")
        self.hyperlink_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u751f\u6210", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"\u76ee\u5f55", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"help", None))
#if QT_CONFIG(accessibility)
        self.statusbar.setAccessibleName(QCoreApplication.translate("MainWindow", u"123", None))
#endif // QT_CONFIG(accessibility)
    # retranslateUi

