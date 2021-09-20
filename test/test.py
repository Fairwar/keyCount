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
__version__ = '0.1.1'
__author__ = 'Zeyuan Qiu'

# 初始化 输出格式数量
key_count = 0
switch_count = 0
case_count = []
if_else_count = 0
if_elif_else_count = 0
if_stack=[]

# 设定关键词字
KEYWORDS = (
    'auto', 'break', 'case', 'char', 'const', 'continue','default',
    'do', 'double', 'else', 'enum', 'extern','float', 'for', 'goto',
    'if', 'int', 'long', 'register', 'return', 'short', 'signed',
    'sizeof', 'static','struct', 'switch', 'typedef', 'union', 
    'unsigned', 'void', 'volatile', 'while'
)

# 文件预处理函数
def data_pretreat(data_path):
    """
    	传入 文件路径参数 data_path
	    返回 经预处理列表 data_listed
	"""
    data = open(data_path, mode='r').read() # 读取 data_path 指向文件

    data_shorted = re.sub(r"\/\*([^\*^\/]*|[\*^\/*]*|[^\**\/]*)*\*\/",
                          "", data)    # 删除注释块
    data_shorted = re.sub(r"\/\/[^\n]*", "", data_shorted)      # 删除注释行
    data_shorted = re.sub(r"\'\"\'","",data_shorted)            # 删除 '"'(即 「"」的单字符)
    data_shorted = re.sub(r"\"(.*)\"", "", data_shorted)        # 删除字符串
    data_shorted = re.sub(r"[ \f\r\t\v]+"," ",data_shorted)     # 缩减多余不可见字符
    data_shorted = re.sub(r"[\n]+","  ",data_shorted)           # 改回车为双空格
    data_listed = re.split(r"\W", data_shorted)   # 转化为列表
    print(data_listed)
    return data_listed  # 返回经过预处理的 data_listed

# 关键字处理函数
def keyword_process(data_listed):
    """
        输入 待处理列表 data_listed
        返回 无
    """

    #使用全局变量声明
    global key_count
    global switch_count
    global case_count
    global if_else_count
    global if_elif_else_count
    global if_stack

    data_iter = iter(range(len(data_listed)))   # 生成数据列表迭代器
    for i in data_iter:
        
        word = data_listed[i]

        if word != '' and word in KEYWORDS:  # 判断是否为关键词

            key_count +=  1   # 是关键词则 key_count++

            if word == 'switch':        # 若为 switch 则 switch_count++ 
                switch_count += 1 
                case_count.append(0)    # 且 case_count 增加一个元素

            
            elif word == 'case':        # 若是 case
                case_count[-1] += 1     # case_count 对应元素加1
        
           
            elif word == 'if':          # 若是 if 则压入堆栈
                if_stack.append('if')

            elif word == 'else' :       # 若出现 else

                if data_listed[i+1] == 'if':    # 当为 elseif
                    if_stack.append('elif')     # 压栈 elif
                    key_count = key_count + 1   # 计数下一个 if 
                    data_iter.__next__()        # 跳过下一个 if
                
                else :                  # 若只是 else

                    elifFlag = False    # 初始化 elifFlag 标志

                    while if_stack[-1] == "elif":
                        elifFlag =True
                        if_stack.pop()  # elif 出栈
                    if_stack.pop()      # 当前 else 对应 if 出栈

                    if elifFlag :   # 判断为 if_else 或 if_elif_else
                        if_elif_else_count += 1
                    else :
                        if_else_count += 1

# 输出函数
def final_print(mode):
    if mode >= 1:
        print("total num:", key_count)
    if mode >= 2:
        print("switch num:", switch_count)
        print("case num:", end=' ')
        if switch_count > 0:
                print(*case_count, sep=' ') 
        else:
            print(0)
    if mode >= 3:
        print('if-else num:', if_else_count)
    if mode >= 4:
        print('if-elseif-else num:', if_elif_else_count)

if __name__ == "__main__":
    # 读入目标地址信息 dataPath 和检索模式 mode
    # 读入参数 文件名 dataPath 和 难度 mode
    path, print_mode = sys.argv[1:3]
    print_mode = int(print_mode)
    PARAGRAPH = data_pretreat(path) # 调用文件预处理函数
    keyword_process(PARAGRAPH)  # 调用关键字处理函数
    final_print(print_mode)   # 调用结果输出函数