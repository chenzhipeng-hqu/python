# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/05/30
# @Author  : 陈志鹏
# @File    : xx.py
"""

"""

__author__ = '陈志鹏'

import os
import sys
work_path = os.path.join(os.path.dirname(sys.argv[0]), "../")
sys.path.append(os.path.abspath(work_path))
os.chdir(work_path)

import tensorflow as tf
import numpy as np

from project import log

logger = log.Log(__name__, log_path=os.getcwd()).getlog()

def test1():
    # 使用 NumPy 生成假数据(phony data), 总共 100 个点.
    x_data = np.float32(np.random.rand(2, 100))  # 随机输入
    y_data = np.dot([0.100, 0.200], x_data) + 0.300

    # 构造一个线性模型
    #
    b = tf.Variable(tf.zeros([1]))
    W = tf.Variable(tf.random.uniform([1, 2], -1.0, 1.0))
    y = tf.matmul(W, x_data) + b

    # 最小化方差
    loss = tf.reduce_mean(tf.square(y - y_data))
    # optimizer = tf.train.GradientDescentOptimizer(0.5)
    optimizer = tf.compat.v1.train.GradientDescentOptimizer(0.5)
    train = optimizer.minimize(loss)

    # 初始化变量
    init = tf.initialize_all_variables()

    # 启动图 (graph)
    sess = tf.Session()
    sess.run(init)

    # 拟合平面
    for step in xrange(0, 201):
        sess.run(train)
        if step % 20 == 0:
            print
            step, sess.run(W), sess.run(b)

    # 得到最佳拟合结果 W: [[0.100  0.200]], b: [0.300]


def test2():
    # 进入一个交互式 TensorFlow 会话.
    import tensorflow as tf
    sess = tf.InteractiveSession()

    x = tf.Variable([1.0, 2.0])
    a = tf.constant([3.0, 3.0])

    # 使用初始化器 initializer op 的 run() 方法初始化 'x'
    x.initializer.run()

    # 增加一个减法 sub op, 从 'x' 减去 'a'. 运行减法 op, 输出结果
    sub = tf.sub(x, a)
    print
    sub.eval()
    # ==> [-2. -1.]

if __name__ == '__main__':
    logger.info('\r\n ---------------- welcom to use -----------------')
    test2()
