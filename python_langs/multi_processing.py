#!/usr/bin/python3
# -*- encoding: utf-8 -*-

# Python 多线程/进程
# 进程池 Process Pool
# Python的多线程，经常我们会听到老手说：“Python下多线程是鸡肋，推荐使用多进程！”

from multiprocessing import Process, Pool
import time


def download_git(p_name, t, git_url, branch):
    print("sub-process " + p_name + " start ...")
    print("Download " + git_url + "(" + branch + ")")
    time.sleep(t)
    print("sub-process " + p_name + " over...")


if __name__ == "__main__":
    print("Main Process start")
    lst = ["abc1.git,DB", "abc2.git,DM", "abc3.git,DB", "abc4.git,DM", "abc5.git,DB", "abc6.git,DB", "abc7.git,master"]
    # lst += ["abc8.git,DB", "abc9.git,DM", "abc10.git,DB"]

    # # STYLE-1. 手动创建多个进程
    # p1 = Process(target=download_git, args=("p1", 3, "https://l2.git", "DM"))
    # p2 = Process(target=download_git, args=("p2", 5, "https://l3.git", "DB"))
    # p1.start()
    # p2.start()
    #
    # # 主进程等待 2个子进程全部执行完毕后 才结束
    # p1.join()
    # p2.join()

    # ------------------

    # STYLE-2. 使用进程池创建多个进程 (非阻塞式 apply_async)
    # pool = Pool(processes=3)
    # 默认进程池大小为系统自带核数 (本MAC机就是二核四线程-等同于模拟四核)
    start_time = time.time()
    pool = Pool()
    for i, git in enumerate(lst):
        git_name, branch = tuple(git.split(','))
        # 非阻塞式创建多个进程并启动
        pool.apply_async(func=download_git, args=("任务"+str(i+1), 3, "https://"+git_name, branch))

    # 当不再接收新请求时 关闭进程池
    pool.close()
    # 主进程等待所有子进程执行完毕
    pool.join()
    end_time = time.time()
    # ------------------

    # 进程间通信 (队列) from multiprocessing import Queue
    # 进程池间的 队列通信 from multiprocessing import Manager, Manager.Queue
    # https://www.bilibili.com/video/BV1EE411F7vV?p=9

    print("Main Process ... over ... (%.2f secs.)" % (end_time-start_time))
