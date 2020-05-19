# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/03/26
# @Author  : 陈志鹏
# @File    : financial_tools.py

import unittest
import project.log as log
from project.merge_expense import *

logger = log.Log(__name__).getlog()


class TestMergeExpense(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.merge_expense = MergeExpense()
        cls.merge_expense.set_parameter(month='4月', file_path=r'../datas/费用合并底稿/202004',
                            dst_file=r'../datas/费用合并底稿/202004费用合并（公式）底稿 - 副本.xlsm')
        cls.merge_expense.open_dst_file()

    @classmethod
    def tearDownClass(cls):
        # print('tearDownClass %s' % cls.__class__.__name__)
        cls.merge_expense.save_dst_file()

    def test_serach_files(self):
        file_list = self.merge_expense.search_files(self.merge_expense.file_path)
        self.assertEqual(len(file_list), 15)

    def test_find_company_in_filename(self):
        company = self.merge_expense.find_company_in_filename(r'./202004江西创新-费用.xlsx')
        self.assertEqual(company[1], '创新中心')

        company = self.merge_expense.find_company_in_filename(r'./202004九江天赐报表-费用.xlsx')
        self.assertEqual(company[1], '九江')

    def test_find_src_sheet(self):
        excel_file = pd.ExcelFile(r'../datas/费用合并底稿/202004/202004江西创新-费用.xlsx')
        src_sheet_match = '2020实际' + '管理费用'
        src_sheet = self.merge_expense.find_src_sheet(src_sheet_match, excel_file.sheet_names)
        self.assertEqual(src_sheet, '2020实际管理费用')

        excel_file = pd.ExcelFile(r'../datas/费用合并底稿/202004/202004安徽天孚报表-费用.xlsx')
        src_sheet_match = '2020实际' + '制造费用'
        src_sheet = self.merge_expense.find_src_sheet(src_sheet_match, excel_file.sheet_names)
        self.assertEqual(src_sheet, '2020实际制造费用安徽天孚')

    def test_find_dst_sheet(self):
        dst_sheet_match = 'G' + '-' + '安徽天孚'
        dst_sheet = self.merge_expense.find_dst_sheet(dst_sheet_match, self.merge_expense.writer.sheets)
        self.assertEqual(dst_sheet, dst_sheet_match)

    def test_find_dst_col(self):
        dst_sheet = 'G-安徽天孚'
        wsheet = self.merge_expense.writer.book[dst_sheet]
        month = '2020年' + '4月'
        dst_month_col = self.merge_expense.find_dst_col(month, wsheet)

        self.assertEqual(dst_month_col, 6)

    def test_handle_general(self):
        src_file = r'../datas/费用合并底稿/202004/202004江西创新-费用.xlsx'
        src_sheet = r'2020实际管理费用'
        expense = self.merge_expense.expense_table[0]
        dst_sheet = r'G-创新中心'
        dst_month_col = 6
        src_df = pd.read_excel(src_file, sheet_name=src_sheet, header=expense[3])
        self.merge_expense.handle_general(src_df, expense, dst_sheet, dst_month_col)

        wsheet = self.merge_expense.writer.book[dst_sheet]
        self.assertEqual(src_df.at[expense[2]-1, self.merge_expense.month],
                         wsheet.cell(row=expense[2]+5, column=dst_month_col+1).value)
        print(src_df.at[expense[2]-1, self.merge_expense.month])
        print(wsheet.cell(row=expense[2]+5, column=dst_month_col+1).value)

if __name__ == '__main__':
    # setLogName('out.log')
    # test.info()
    # test.warning()
    # test.debug()
    # print(__name__)
    unittest.main(verbosity=2)
