# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/03/26
# @Author  : 陈志鹏
# @File    : financial_tools.py

import os
import sys
import codecs
import logging
import pyautogui
import xml.sax
import configparser
import pandas as pd
from financial_ui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from other_payables import *
from internal_orders import *
from database_match import *
from custom_control import *
from others.merge import *
from others.fetch import *

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

logging.basicConfig(
    level=logging.DEBUG,
    filename='out.log',
    datefmt='%Y/%m/%d %H:%M:%S',
    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')

logger = logging.getLogger(__name__)


class UIMainWindow(Ui_MainWindow, QMainWindow):

    def __init__(self):
        super(UIMainWindow, self).__init__()
        logger.info('\r\nwelcome to use financial tools')
        self.initUI()
        self.configure_init()
        self.payables_init()
        self.inner_order_init()
        self.cust_ctrl_init()
        self.other_fetch_init()
        self.database_match_init()

    def initUI(self):
        self.setupUi(self)

        # payables
        self.download_payables_pushButton.clicked.connect(
            self.download_payables)

        # 自定义文本验证器
        validator = QRegExpValidator(self)
        # 设置属性 设置文本允许出现的字符内容
        validator.setRegExp(QRegExp('^(20[1-2][0-9])$'))
        self.s_year_lineEdit.setValidator(validator)
        self.e_year_lineEdit.setValidator(validator)

        # 自定义文本验证器
        validator = QRegExpValidator(self)
        # 设置属性 设置文本允许出现的字符内容
        validator.setRegExp(QRegExp('^(1[0-2]|0?[1-9])$'))
        self.s_month_lineEdit.setValidator(validator)
        self.e_month_lineEdit.setValidator(validator)

        self.s_year_lineEdit.editingFinished.connect(
            self.s_year_editingFinished)
        self.s_month_lineEdit.editingFinished.connect(
            self.s_month_editingFinished)
        self.e_year_lineEdit.editingFinished.connect(
            self.e_year_editingFinished)
        self.e_month_lineEdit.editingFinished.connect(
            self.e_month_editingFinished)
        self.subject_lineEdit.editingFinished.connect(
            self.subject_editingFinished)

        self.save_path_pushButton.clicked.connect(self.OpenFileDialog)

        self.login_payables_pushButton.clicked.connect(self.login_payables)
        self.filter_payables_pushButton.clicked.connect(self.filter_payables)
        self.export_payables_pushButton.clicked.connect(self.export_payables)
        self.merge_payables_pushButton.clicked.connect(self.merge_payables)
        self.login_payables_pushButton.setEnabled(False)
        self.merge_payables_pushButton.setEnabled(False)

        # internal_orders
        # self.adjust_pushButton.clicked.connect(self.inter_order_adjust)

        # other_merge
        self.merge_pushButton.clicked.connect(self.other_merge)
        self.merge_path_pushButton.clicked.connect(self.other_merge_path_dialog)

        # database_match
        self.database_fetch_pushButton.clicked.connect(self.database_match_fetch)
        # self.database_fetch_path_pushButton.clicked.connect(self.other_merge_path_dialog)

        # other_fetch
        self.fetch_pushButton.clicked.connect(self.other_fetch)
        self.fetch_file_pushButton.clicked.connect(self.other_fetch_file_dialog)
        self.blance_subject_lineEdit.editingFinished.connect(self.fetch_subject_editingFinished)
        self.blance_month_lineEdit.editingFinished.connect(self.fetch_month_editingFinished)

        # test
        # self.pushButton.clicked.connect(self.test)

    def configure_init(self):
        self.conf = configparser.ConfigParser()
        self.conf_path = os.path.join(os.getcwd(), 'configure.ini')
        self.conf.read(self.conf_path, encoding="utf-8-sig")
        # self.conf.readfp(codecs.open(self.conf_path, 'r', 'utf-8-sig'))

        if self.conf.has_option('payables', 'start_year'):
            s_year = self.conf.get('payables', 'start_year')
            self.s_year_lineEdit.setText(s_year)

        if self.conf.has_option('payables', 'start_month'):
            s_month = self.conf.get('payables', 'start_month')
            self.s_month_lineEdit.setText(s_month)

        if self.conf.has_option('payables', 'end_year'):
            e_year = self.conf.get('payables', 'end_year')
            self.e_year_lineEdit.setText(e_year)

        if self.conf.has_option('payables', 'end_month'):
            e_month = self.conf.get('payables', 'end_month')
            self.e_month_lineEdit.setText(e_month)

        if self.conf.has_option('payables', 'job'):
            job = self.conf.get('payables', 'job')
            self.job_lineEdit.setText(job)

        if self.conf.has_option('payables', 'subject'):
            subject = self.conf.get('payables', 'subject')
            self.subject_lineEdit.setText(subject)

        if self.conf.has_option('payables', 'save_path'):
            save_path = self.conf.get('payables', 'save_path')
            self.save_path_pushButton.setText(save_path)
        else:
            self.save_path_pushButton.setText(os.getcwd())

        center = self.conf.items("center")
        self.centers = {position[0]: position[1].split(',') for position in center}
        print(self.centers)

        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        # for row in range(0, 6):
        #     item = QTreeWidgetItem(self.treeWidget)
        #     for col in range(0, 4):
        #         item.setCheckState(col, Qt.Checked);
        #         item.setText(col, QCoreApplication.translate("MainWindow", u'啊', None))
        for (cnt, center) in enumerate(self.centers.items()):
            #print(cnt, center)
            if cnt % 4 == 0:
                item = QTreeWidgetItem(self.treeWidget)
            item.setCheckState(cnt % 4, Qt.Checked)
            item.setText(cnt % 4, QCoreApplication.translate("MainWindow", center[0], None))
        self.treeWidget.itemChanged.connect(self.center_select)
        self.treeWidget.setSortingEnabled(__sortingEnabled)

        # other merge
        if self.conf.has_option('other', 'other_merge_path'):
            merge_path = self.conf.get('other', 'other_merge_path')
            self.merge_path_pushButton.setText(merge_path)
        else:
            self.merge_path_pushButton.setText(os.getcwd())

        # other fetch
        if self.conf.has_option('other', 'other_fetch_file'):
            fetch_path = self.conf.get('other', 'other_fetch_file')
            self.fetch_file_pushButton.setText(fetch_path)

        if self.conf.has_option('other', 'other_fetch_subject'):
            subject = self.conf.get('other', 'other_fetch_subject')
            self.blance_subject_lineEdit.setText(subject)

        if self.conf.has_option('other', 'other_fetch_month'):
            month = self.conf.get('other', 'other_fetch_month')
            self.blance_month_lineEdit.setText(month)

    def payables_init(self):
        self.thread_other_payables = QThread()
        self.worker_other_payables = WorkerOtherPayables()
        # self.worker_other_payables.message_singel.connect(self.message_singel)
        self.worker_other_payables.finish_singel.connect(self.finish_singel)
        self.worker_other_payables.statusBar_singel.connect(self.statusBar_singel)
        self.worker_other_payables.moveToThread(self.thread_other_payables)
        self.thread_other_payables.started.connect(self.worker_other_payables.download)
        # self.thread_other_payables.finished.connect(self.finish_singel)

    def inner_order_init(self):
        self.thread_inter_orders = QThread()
        self.worker_inter_orders = WorkerInterOrders()
        # self.worker_inter_orders.message_singel.connect(self.message_singel)
        self.worker_inter_orders.statusBar_singel.connect(self.statusBar_singel)
        self.worker_inter_orders.finish_singel.connect(self.inter_order_finish_singel)
        self.worker_inter_orders.moveToThread(self.thread_inter_orders)
        self.thread_inter_orders.started.connect(self.worker_inter_orders.filter)

    def database_match_init(self):
        self.thread_database_match = QThread()
        self.worker_database_match = DatabaseMatch()
        # self.worker_inter_orders.message_singel.connect(self.message_singel)
        self.worker_database_match.statusBar_singel.connect(self.statusBar_singel)
        self.worker_database_match.finish_singel.connect(self.database_match_finish_singel)
        self.worker_database_match.moveToThread(self.thread_database_match)
        self.thread_database_match.started.connect(self.worker_database_match.run)

    def other_merge(self):
        # self.thread_other_merge = QThread()
        self.worker_other_merge = WorkerMerge()
        self.worker_other_merge.statusBar_singel.connect(self.statusBar_singel)
        # self.worker_other_merge.finish_singel.connect(self.other_merge_finish_singel)
        # self.worker_other_merge.moveToThread(self.thread_other_merge)
        # self.thread_other_merge.started.connect(self.worker_other_merge.)
        path = self.merge_path_pushButton.text().strip()
        self.worker_other_merge.merge(path, 'merge.xlsx')

    def other_fetch_init(self):
        self.thread_other_fetch = QThread()
        self.worker_other_fetch = WorkerFetch()
        self.worker_other_fetch.statusBar_singel.connect(self.statusBar_singel)
        self.worker_other_fetch.finish_singel.connect(self.other_fetch_finish_singel)
        self.worker_other_fetch.moveToThread(self.thread_other_fetch)
        self.thread_other_fetch.started.connect(self.worker_other_fetch.balance_sheet_fetch)

    def other_fetch(self):
        self.fetch_pushButton.setEnabled(False)
        subject = self.blance_subject_lineEdit.text().strip()
        month = self.blance_month_lineEdit.text().strip()
        src_file = self.fetch_file_pushButton.text()
        print(subject)
        print(month)
        print(src_file)

        self.worker_other_fetch.balance_sheet_set_parameter(\
                        src_file=src_file,\
                        subject=subject,\
                        month=month)
        self.thread_other_fetch.start()

    def database_match_fetch(self):
        self.database_fetch_pushButton.setEnabled(False)
        src_path = self.database_fetch_pushButton.text()

        self.worker_database_match.set_parameter(src_path=src_path)
        self.thread_database_match.start()

    def cust_ctrl_init(self):
        self.thread_cust_ctrl = QThread()
        self.worker_cust_ctrl = WorkerCustCtrl()
        self.worker_cust_ctrl.moveToThread(self.thread_cust_ctrl)
        self.worker_cust_ctrl.mouse_singel.connect(self.mouse_singel)
        # self.worker_cust_ctrl.message_singel.connect(self.message_singel)
        self.thread_cust_ctrl.started.connect(self.worker_cust_ctrl.run)
        self.thread_cust_ctrl.start()

        x, y = self.worker_cust_ctrl.get_size()
        self.size_label.setText("{}*{}".format(x, y))

    def set_parameter_payables(self):
        # print(centers)
        logger.debug(self.centers)

        duration = [self.s_year_lineEdit.text(), self.s_month_lineEdit.text(),
                    self.e_year_lineEdit.text(), self.e_month_lineEdit.text()]
        # print(duration)
        logger.debug(duration)

        job = self.job_lineEdit.text().strip()

        subjects = self.subject_lineEdit.text().strip().split(',')

        save_path = self.save_path_pushButton.text()
        # print(save_path)
        logger.debug(save_path)

        # self.worker_other_payables.set_parameter(centers, duration, job, subject, save_path)
        self.worker_other_payables.set_parameter(centers=self.centers,
                                                 duration=duration,
                                                 job=job,
                                                 subjects=subjects,
                                                 save_path=save_path)

    def download_payables(self):
        self.download_payables_pushButton.setEnabled(False)
        self.statusBar_singel('开始下载...')
        self.set_parameter_payables()
        self.thread_other_payables.start()

    def s_year_editingFinished(self):
        # print(self.s_year_lineEdit.text())
        self.conf.set('payables', 'start_year', self.s_year_lineEdit.text())
        self.conf.write(codecs.open(self.conf_path, 'w', 'utf-8-sig'))

    def s_month_editingFinished(self):
        # print(self.s_month_lineEdit.text())
        self.conf.set('payables', 'start_month', self.s_month_lineEdit.text())
        self.conf.write(codecs.open(self.conf_path, 'w', 'utf-8-sig'))

    def e_year_editingFinished(self):
        # print(self.e_year_lineEdit.text())
        self.conf.set('payables', 'end_year', self.e_year_lineEdit.text())
        self.conf.write(codecs.open(self.conf_path, 'w', 'utf-8-sig'))

    def e_month_editingFinished(self):
        # print(self.e_month_lineEdit.text())
        self.conf.set('payables', 'end_month', self.e_month_lineEdit.text())
        self.conf.write(codecs.open(self.conf_path, 'w', 'utf-8-sig'))

    def job_editingFinished(self):
        # print(self.job_lineEdit.text())
        self.conf.set('payables', 'job', self.job_lineEdit.text().strip())
        self.conf.write(codecs.open(self.conf_path, 'w', 'utf-8-sig'))

    def subject_editingFinished(self):
        # print(self.subject_lineEdit.text())
        self.conf.set(
            'payables',
            'subject',
            self.subject_lineEdit.text().strip())
        self.conf.write(codecs.open(self.conf_path, 'w', 'utf-8-sig'))

    def OpenFileDialog(self):
        path = QFileDialog.getExistingDirectory(
            self, '选择文件夹', self.save_path_pushButton.text())
        # print(path)
        if os.path.isdir(path):
            self.save_path_pushButton.setText(path)
            self.statusBar_singel(path)
            self.conf.set('payables', 'save_path', path)
            self.conf.write(codecs.open(self.conf_path, 'w', 'utf-8-sig'))

    def other_merge_path_dialog(self):
        path = QFileDialog.getExistingDirectory(
            self, '选择文件夹', self.merge_path_pushButton.text())
        # print(path)
        if os.path.isdir(path):
            self.merge_path_pushButton.setText(path)
            self.statusBar_singel(path)
            self.conf.set('other', 'other_merge_path', path)
            self.conf.write(codecs.open(self.conf_path, 'w', 'utf-8-sig'))

    def other_fetch_file_dialog(self):
        fname, ftype = QFileDialog.getOpenFileName(
            self, '选择文件', self.fetch_file_pushButton.text(), 'All Files (*)')
        print(fname)
        if os.path.isfile(fname):
            self.fetch_file_pushButton.setText(fname)
            self.statusBar_singel(fname)
            self.conf.set('other', 'other_fetch_file', fname)
            self.conf.write(codecs.open(self.conf_path, 'w', 'utf-8-sig'))

    def fetch_subject_editingFinished(self):
        # print(self.subject_lineEdit.text())
        self.conf.set(
            'other',
            'other_fetch_subject',
            self.blance_subject_lineEdit.text().strip())
        self.conf.write(codecs.open(self.conf_path, 'w', 'utf-8-sig'))

    def fetch_month_editingFinished(self):
        # print(self.subject_lineEdit.text())
        self.conf.set(
            'other',
            'other_fetch_month',
            self.blance_month_lineEdit.text().strip())
        self.conf.write(codecs.open(self.conf_path, 'w', 'utf-8-sig'))

    def login_payables(self):
        self.set_parameter_payables()
        self.worker_other_payables.login()

    def filter_payables(self):
        pass

    def export_payables(self):
        pass

    def merge_payables(self):
        self.set_parameter_payables()
        self.worker_other_payables.merge()
        self.message_singel('合并完成。')
        self.statusBar_singel('合并完成。')

    def center_select(self, item, column):
        source = self.sender()
        if item.checkState(column) == Qt.Checked:
            print("checked", item.text(column))
            if self.conf.has_option('center', str(item.text(column))):
                center_code = self.conf.get('center', item.text(column))
                self.centers[item.text(column)] = center_code
                print(self.centers)

        if item.checkState(column) == Qt.Unchecked:
            print("unchecked", item.text(column))
            if self.conf.has_option('center', str(item.text(column))):
                center_code = self.conf.get('center', item.text(column))
                self.centers.pop(str(item.text(column)))
                print(self.centers)

    # def inter_order_adjust(self):
    #     self.adjust_pushButton.setEnabled(False)
    #     self.statusBar_singel('开始调整...')
    #     path = os.path.join(os.getcwd(), r'datas\original_data')
    #     self.worker_inter_orders.set_parameter(path)
    #     self.thread_inter_orders.start()

    def message_singel(self, str):
        # 移动光标到最后的文字
        #text_cursor = self.textBrowser.textCursor()
        # text_cursor.movePosition(text_cursor.End)
        # self.textBrowser.setTextCursor(text_cursor)
        # self.textBrowser.insertPlainText(str)
        pass

    def statusBar_singel(self, msg):
        self.statusBar().showMessage(msg)

    def finish_singel(self):
        self.thread_other_payables.quit()
        self.download_payables_pushButton.setEnabled(True)
        self.statusBar_singel('下载完成。')
        QMessageBox.about(self, "提示", "下载完成")
        # print('finished')

    def other_fetch_finish_singel(self):
        self.thread_other_fetch.quit()
        self.fetch_pushButton.setEnabled(True)

    def inter_order_finish_singel(self):
        self.thread_inter_orders.quit()
        self.adjust_pushButton.setEnabled(True)
        self.statusBar_singel('调整完成。')

    def database_match_finish_singel(self):
        self.thread_database_match.quit()
        self.database_fetch_pushButton.setEnabled(True)
        self.statusBar_singel('提取完成。')
        QMessageBox.about(self, "提示", "提取完成")

    def mouse_singel(self, x, y):
        # self.x_label.setText('X: ' + str(x).rjust(4))
        # self.y_label.setText('Y: ' + str(y).rjust(4))
        self.mouse_label.setText('X: ' + str(x).rjust(4) + '  Y: ' + str(y).rjust(4))

    def test(self):
        pass


if __name__ == '__main__':
    try:
        # 每一pyqt5应用程序必须创建一个应用程序对象。sys.argv参数是一个列表，从命令行输入参数
        app = QApplication(sys.argv)
        ui = UIMainWindow()
        ui.show()

        # 系统exit()方法确保应用程序干净的退出
        # 的exec_()方法有下划线。因为执行是一个Python关键词。因此，exec_()代替
        app.exec_()
    except Exception as err:
        print('ui catch error!!!')
        print(err)
    finally:
        # 系统exit()方法确保应用程序干净的退出
        sys.exit()
