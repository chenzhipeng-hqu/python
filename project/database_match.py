# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/03/26
# @Author  : 陈志鹏
# @File    : financial_tools.py

import os
import sys

work_path = os.path.join(os.path.dirname(sys.argv[0]), "../")
sys.path.append(os.path.abspath(work_path))
os.chdir(work_path)

import time
from project.fetch import *

# if hasattr(sys, 'frozen'):
#     os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

nowTime = lambda:int(round(time.time()*1000))

class DatabaseMatch(QObject):
    finish_singel = Signal()
    statusBar_singel = Signal(str)

    def __init__(self):
        super(DatabaseMatch, self).__init__()

    def __del__(self):
        print('delete %s' % self.__class__.__name__)

    def subject_num_ops(self, data):
        # print(type(data))
        # print(data['功能范围'])
        if data['总账科目'] >= 66030000:
            ret = self.src_index_df[self.src_index_df['总账科目'] == data['总账科目']]['长文本'].values[0]
        elif pd.isnull(data['功能范围']):
            ret = '#N/A'
        else:
            ret = self.src_index_df[self.src_index_df['功能范围'] == data['功能范围']]['功能范围描述'].values[0] + \
                  self.src_index_df[self.src_index_df['总账科目'] == data['总账科目']]['长文本'].values[0]

        return ret

    def abstract_ops(self, data):
        if str(data['分配']).find('FI') == -1:
            ret = data['文本']
        else:
            ret = data['分配'] + ',' +  data['文本']

        return ret

    def department_name_ops(self, data):
        temp = self.src_index_df[self.src_index_df['成本中心编码'] == data['成本中心']]
        if temp.empty:
            ret = '#N/A'
        else:
            ret = temp['成本中心'].values[0]
        return ret

    def project_num_ops(self, data):
        if pd.isnull(data['订单']):
            ret = ''
        elif 200000 <= data['订单'] < 999999:
            temp = self.src_index_df[self.src_index_df['SAP订单号'] == data['订单']]
            if temp.empty:
                ret = '#N/A'
            else:
                ret = temp['SAP项目名称'].values[0]
        else:
            ret = ''
        return ret

    def company_ops(self, data):
        temp = self.src_index_df[self.src_index_df['编码'] == data['公司代码']]
        if temp.empty:
            ret = '#N/A'
        else:
            ret = temp['简称'].values[0]
        return ret

    def apply_id_ops(self, data):
        temp = self.src_FB03_df[self.src_FB03_df['apply_id'] == data['apply_id']]

        self.data_cnt = self.data_cnt + 1
        self.statusBar_singel.emit('正在提取 申请人 %d...\r\n' % (self.data_cnt))
        if temp.empty:
            ret = '#N/A'
        else:
            ret = temp['用户名'].values[0]
        return ret

    def staff_ops(self, data):
        temp = self.src_index_df[self.src_index_df['号码'] == data['申请人']]
        if temp.empty:
            ret = '#N/A'
        else:
            ret = temp['姓名'].values[0]
        return ret

    def src_data_ops(self, data):
        # return self.project_num_ops(data), self.company_ops(data)
        return self.subject_num_ops(data), self.abstract_ops(data), self.department_name_ops(data), self.project_num_ops(data), self.company_ops(data)

    def set_parameter(self, *args, ** kwargs):
        self.src_path = kwargs.get('src_path')
        print(self.src_path)

    def run(self):
        self.statusBar_singel.emit('正在提取...\r\n')
        self.data_cnt = 0
        starttime = nowTime()
        src_file = r'./datas/数据库底稿-SAP/FAGLL03.xlsx'
        # src_file = r'./datas/original_data/调整内部订单号.xls'
        src_index_file = r'./datas/数据库底稿-SAP/索引.xlsx'
        src_FB03_file = r'./datas/数据库底稿-SAP/FB03.xlsx'
        dst_file = r'./datas/数据库底稿-SAP/数据库底稿-SAP类.xlsx'

        self.src_index_df = pd.read_excel(src_index_file, sheet_name='索引')
        self.src_FB03_df = pd.read_excel(src_FB03_file, sheet_name='Sheet1')
        src_data_df = pd.read_excel(src_file, sheet_name='Sheet1')
        # src_data_df = pd.read_excel(src_file, sheet_name='FAGLL03')
        # print(src_index_df.head())
        # print(src_data_df.head())

        # self.src_FB03_df['apply_id'] = self.src_FB03_df['公司代码'] + self.src_FB03_df['凭证编号']
        self.src_FB03_df['apply_id'] = (self.src_FB03_df['公司代码'].map(str) + self.src_FB03_df['凭证编号'].map(str)).map(int)
        # print('self.src_FB03_df:')
        # print(self.src_FB03_df['公司代码'].head())
        # print(self.src_FB03_df['凭证编号'].head())
        # print(self.src_FB03_df['apply_id'].head())
        dst_df = pd.DataFrame(columns=['会计年度', '期间', '凭证日期', '凭证编号', '科目编号', '科目名称', '借方本币', '摘要', '部门', '部门名称', '申请人',
                                       '员工姓名', '项目编号', '项目名称', '账套'])
        # dst_df = pd.read_excel(dst_file)
        dst_df['会计年度'] = src_data_df['会计年度']
        dst_df['期间'] = src_data_df['记帐期间']
        dst_df['凭证日期'] = src_data_df['过账日期'].dt.strftime('%Y-%m-%d')
        dst_df['凭证编号'] = src_data_df['凭证编号']
        dst_df['科目编号'] = src_data_df['总账科目']
        dst_df['借方本币'] = src_data_df['本币金额']
        dst_df['部门'] = src_data_df['成本中心']
        dst_df['项目编号'] = src_data_df['订单']

        self.statusBar_singel.emit('正在提取 科目名称 ...\r\n')
        dst_df['科目名称'] = src_data_df.apply(self.subject_num_ops, axis=1)
        self.statusBar_singel.emit('正在提取 摘要 ...\r\n')
        dst_df['摘要'] = src_data_df.apply(self.abstract_ops, axis=1)
        self.statusBar_singel.emit('正在提取 部门名称 ...\r\n')
        dst_df['部门名称'] = src_data_df.apply(self.department_name_ops, axis=1)
        self.statusBar_singel.emit('正在提取 项目名称 ...\r\n')
        dst_df['项目名称'] = src_data_df.apply(self.project_num_ops, axis=1)
        self.statusBar_singel.emit('正在提取 账套 ...\r\n')
        dst_df['账套'] = src_data_df.apply(self.company_ops, axis=1)

        self.statusBar_singel.emit('正在提取 公司代码+凭证编号 ...\r\n')
        # src_data_df['apply_id'] = src_data_df['公司代码'] + src_data_df['凭证编号']
        src_data_df['apply_id'] = (src_data_df['公司代码'].map(str) + src_data_df['凭证编号'].map(str)).map(int)
        # print('src_data_df:')
        # print(src_data_df['公司代码'].head())
        # print(src_data_df['凭证编号'].head())
        # print(src_data_df['apply_id'].head())
        dst_df['申请人'] = src_data_df.apply(self.apply_id_ops, axis=1)
        # src_data_df['申请人'] = dst_df['申请人']
        self.statusBar_singel.emit('正在提取 员工姓名...\r\n')
        dst_df['员工姓名'] = dst_df.apply(self.staff_ops, axis=1)

        # dst_df[['科目名称', '摘要', '部门名称', '项目名称', '账套']] = src_data_df.apply(self.src_data_ops, axis=1, result_type='expand')

        self.statusBar_singel.emit('正在合成文件...\r\n')
        dst_df.to_excel(dst_file, index=False, engine='openpyxl')
        self.statusBar_singel.emit('完成, %dms\r\n' % (nowTime()-starttime))
        print('finish', nowTime()-starttime, 'ms')
        self.finish_singel.emit()

if __name__ == '__main__':
    database_match = DatabaseMatch()
    database_match.run()