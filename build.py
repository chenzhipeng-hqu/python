#
# -*- coding: utf-8 -*-

from PyInstaller.__main__ import run

'''
__bref__    : In this example, we create a simple window in PyQt5.
__author__  : chenzhipeng3472
__data__    : 04-July-2018

# -F, --onefile: 打包成一个EXE文件
# -D, --onedir: 创建一个目录，包含exe文件，但会依赖很多文件（默认选项）
# -w, –windowed, –noconsole: 不带console输出控制台，window窗体格式
# -c, –console, –nowindowed 使用控制台，无界面(默认) 
# -p, --paths：依赖包路径
# -i, --icon：图标
# --noupx：不用upx压缩
# --clean：清理掉临时文件
# –-distpath: 在哪里放置捆绑的应用程序（默认：./dist）
# –-workpath: 在哪里放置所有的临时工作文件，.log，.pyz等（默认：./build）
# -–specpath: 存储生成的spec文件的文件夹（默认：当前目录）

'''

if __name__ == '__main__':
    opts = ['ProgramUpdate.py',
            '-F',
            '--clean',
            '-p C:\\Users\\chenzhipeng3472\\AppData\Local\\Programs\\Python\Python36\\Lib\\site-packages\\PyQt5\\Qt\\bin',
            '-p C:\\Users\\chenzhipeng3472\\AppData\Local\\Programs\\Python\Python36\\Lib\\site-packages\\PyQt5\\Qt\\plugins',
            ]
    run(opts)
    input()
