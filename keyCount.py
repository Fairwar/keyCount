# -*- coding:UTF-8 -*-
#引入正则表达式\sys等包
import re,sys

#设定关键词字
keyWords = ['auto','break','case','char','const','continue','default','do',
            'double','else','enum','extern','float','for','goto','if','int',
            'long','register','return','short','signed','sizeof','static',
            'struct','switch','typedef','union','unsigned','void','volatile',
            'while']

#初始化 输出格式数量
index = 0
Count = 0
switch_Count = 0
case_Count = []
if_else_Count = 0
if_elif_else_Count = 0
ifstack=[]

#读入目标地址信息 dataPath 和检索模式 mode
if __name__ == "__main__":
    dataPath, mode = sys.argv[1:3]
    mode = int(mode)


#读入文件并将提取单词(正则表达式"\W"可提取出单词数字及下划线)
paraGraph = open(dataPath,mode='r').read()
#将所有空白字符及长串空格都改为一个空格(防止有人打一堆无用空格)
paraGraph = re.sub(r"\s +"," ",paraGraph)
paraGraph=re.split(r"\W",paraGraph)

#逐个单词排查是否出现于关键词字典中
Iter = iter(range(len(paraGraph)))
for index in Iter:
    #判断是否为关键词
    word = paraGraph[index]
    if word != '' and word in keyWords:

        #是关键词则 Count++
        Count += 1

        #若为 switch 则 switch_Count++ 
        #且 case_Count 增加一个元素
        # (即增加一组 "switch case" 组合)
        if word == 'switch':
            switch_Count += 1
            case_Count.append(0)

        #若是 case 则 对应case_Count对应元素自增
        elif word == 'case':
            case_Count[switch_Count-1] += 1
        
        #若是 if 则压入堆栈
        elif word == 'if':
            ifstack.append('if')

        #若出现 else
        elif word == 'else' :

                #判断是不是 else if
                if paraGraph[index+1] == 'if':

                    #若是则将 elif 压栈删除下一个 if
                    ifstack.append('elif')
                    Count += 1
                    Iter.__next__()
                
                #若只是 else
                else :

                    # 初始化 elifFlag 标志
                    elifFlag=0

                    # elif 出栈
                    while ifstack[-1] == "elif":
                        elifFlag=1
                        ifstack.pop()
                    
                    #该 else 对应 if 出栈
                    ifstack.pop()

                    #根据 elifFlag 判断
                    if elifFlag :
                        if_elif_else_Count += 1
                    else :
                        if_else_Count += 1
        
#输出模块

print("total num:",Count)

if mode >= 2:
    print("switch num:",switch_Count)
    print("case num:",end=' ')
    for i in range(switch_Count):
        print(case_Count[i],end=' ')

if mode >= 3:
    print('\nif-else num:',if_else_Count)

if mode >= 4:
    print('if-elif-else num:',if_elif_else_Count)
