# -*- coding:UTF-8 -*-

"""
    @ 功能：根据难度分为以下四个层次的功能
        1. 实现检查 C语言 代码中关键词数量
        2. 检查 switch-case 有几组，每组中有几个 case
        3. 检查 有几组 if-else 结构
        4. 检查 有几组 if-elif-else 结构
    @ author：邱泽源
    @ create：2021-9-14

"""

# 引入 re、sys 等包
import re
import sys

# 版本、作者声明
__version__ = '0.1'
__author__ = 'Zeyuan Qiu'

# 初始化 输出格式数量
key_count = 0
switch_count = 0
case_count = []
if_else_count = 0
if_elif_else_count = 0
if_stack=[]

# 设定关键词字
KEYWORDS = [
    'auto', 'break', 'case', 'char', 'const', 'continue','default',
    'do', 'double', 'else', 'enum', 'extern','float', 'for', 'goto',
    'if', 'int', 'long', 'register', 'return', 'short', 'signed',
    'sizeof', 'static','struct', 'switch', 'typedef', 'union', 
    'unsigned', 'void', 'volatile', 'while'
]

# 文件预处理函数
def data_pretreatment(data_path):
    data = open(data_path, mode='r').read()
    # 将所有空白字符及长串空格都改为一个空格
    # 防止有人打一堆无用空格
    data = re.sub(r"\s +", " ", data)
    # 通过正则表达式并将提取单词
    # 正则表达式"\W"可提取出单词数字及下划线
    data = re.split(r"\W", data)
    return data

# 关键字处理函数
def keyword_process(data):

    #使用全局变量声明
    global key_count
    global switch_count
    global case_count
    global if_else_count
    global if_elif_else_count
    global if_stack

    # 逐个单词排查是否出现于关键词字典中
    data_iter = iter(range(len(data)))
    for i in data_iter:
        # 判断是否为关键词
        word = data[i]
        if word != '' and word in KEYWORDS:

            # 是关键词则 key_count++
            key_count = key_count + 1

            # 若为 switch 则 switch_count++ 
            # 且 case_count 增加一个元素
            if word == 'switch':
                switch_count = switch_count + 1
                case_count.append(0)

            # 若是 case 则 case_count 对应元素自增
            elif word == 'case':
                case_count[switch_count-1] = case_count[switch_count-1] + 1
        
            # 若是 if 则压入堆栈
            elif word == 'if':
                if_stack.append('if')

            # 若出现 else
            elif word == 'else' :

                # 判断是不是 else if
                if data[i+1] == 'if':

                    # 若是则将 elif 压栈删除下一个 if
                    if_stack.append('elif')
                    key_count += 1
                    data_iter.__next__()
                
                # 若只是 else
                else :

                    # 初始化 elifFlag 标志
                    elifFlag=0

                    # elif 出栈
                    while if_stack[-1] == "elif":
                        elifFlag=1
                        if_stack.pop()
                    
                    # 该 else 对应 if 出栈
                    if_stack.pop()

                    # 根据 elifFlag 判断为 if_else 或 if_elif_else
                    if elifFlag :
                        if_elif_else_count = if_elif_else_count + 1
                    else :
                        if_else_count = if_else_count + 1

# 输出函数
def final_print(mode):
    if(mode>=1):
        print("total num:",key_count)
    if mode >= 2:
        print("switch num:",switch_count)
        print("case num:",end=' ')
        if switch_count > 0:
                for i in range(switch_count):
                    print(case_count[i],end=' ')
        else:
            print(0)
    if mode >= 3:
        print('\nif-else num:',if_else_count)
    if mode >= 4:
        print('if-elif-else num:',if_elif_else_count)

if __name__ == "__main__":
    # 读入目标地址信息 dataPath 和检索模式 mode
    # 读入参数 文件名 dataPath 和 难度 mode
    path, mode = sys.argv[1:3]
    mode = int(mode)
    PARAGRAPH = data_pretreatment(path) #调用文件预处理函数
    keyword_process(PARAGRAPH)
    final_print(mode)