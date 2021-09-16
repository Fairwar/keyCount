# keyCount 编程作业
软件工程第一次编程作业 keyCount

| 个作业属于哪个课程 | https://bbs.csdn.net/forums/fzuSoftwareEngineering2021 |
| ----------------- |--------------- | 
| 这个作业要求在哪里| https://bbs.csdn.net/topics/600574694 |
| 这个作业的目标 | 制定个人编程规范、C 或 C++文件关键字提取 |
| 学号 | 081900223 |
___________________
## 目录索引
* [keyCount 作业过程](#keyCount作业过程)
	* [PSP表格](#PSP表格)
	* [需求分析](#需求分析)
	* [代码迭代](#代码迭代)
		* [参数输入](#参数输入)
		* [文本预处理](#文本预处理)
		* [关键词处理](#关键词处理)
		* [输出](输出)
	* [性能分析](#性能分析)
		* [单元测试](#单元测试)
		* [运行时间](#运行时间)
	* [困难及新获知识](#困难及新获知识)
		* [正则表达式](#正则表达式)
___________________

## **keyCount作业过程**
+ ###  **PSP表格** 
| Personal Software Process Stages | 预估耗时(分钟) | 实际耗时(分钟) |
| -------------------------------- | ------------- | ------------- |
| Planning（计划）|  |  |
| Estimate（估计时间） |  |  |
| Development（开发） |  |  |
| Analysis（需求分析（包括学习新技术）） |  |  |
| Design Spec（生成设计文档） |  |  |
| Design Review（设计复审） |  |  |
| Coding Standard（代码规范 ） |  |  |
| Design（具体设计） |  |  |
| Coding（具体编码） |  |  |
| Code Review（代码复审） |  |  |
| Test（测试（自我测试，修改代码，提交修改）） |  |  |
| Test Report（测试报告） |  |  |
| Size Measurement（计算工作量） |  |  |
| Postmortem & Process Improvement Plan（事后总结, 并提出过程改进计划） |  |  |
| Total（合计） |  |  |
+ ###  **需求分析**  
	1. **输入格式**：python keyCount.py key.c mode  
		> + 需进行 ***提取输入信息、进行文件获取、文本化、文本预处理***    
		> + 将文本内容预处理为列表
		> + 使用 用到 ***sys*** 和 ***re*** 包

	2. **基础要求**：输出关键字统计信息  
		> + 需要初始化 ***关键词字典信息*** ，应设置为元组常数

	3. **进阶要求**：输出有几组 switch case 结构，同时输出每组对应的case个数  
	4. **拔高要求**：输出有几组 if else 结构  
	5. **终极要求**：输出有几组 if，else if，else 结构  
		> + 需要一个 ***关键词理函数*** ，对列表元素进行进行分类处理
		> + 应该根据 ***难度要求 mode*** 选择不同 ***输出模式***

+ ### **代码迭代**
	>&#160; &#160; &#160; &#160;刚开始的时候未考虑到被编程规范等要求，虽能实现其功能，但较为杂乱无章，第二天紧急补课了编程规范后对程序进行了一轮大改，将其从一段一团乱麻拯救成井然有序的面向函数，限于 markdown 能力有待提高，部分格式还未能完全在下方展示出
	1. #### **初始化参数**
		```python
		# 初始化计数变量 count
		key_count = 0
		witch_count = 0
		case_count = []	# 以列表储存 case 数量
		if_else_count = 0
		if_elif_else_count = 0

		# 初始化 堆栈 if_stack
		if_stack=[]

		# 初始化关键字元组 KEYWORDS
		KEYWORDS = (
		'auto', 'break', 'case', 'char'，'const', 'continue','default','do', 'double', 'else', 'enum', 'extern','float', 'for', 'goto','if', 'int', 'long', 'register', 'return', 'short', 'signed','sizeof', 'static','struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while'
		)
		```
	2. #### **文本预处理**
		>&#160; &#160; &#160; &#160;考虑到可能存在有 ***冗余空格*** 对 elseif 判断逻辑的干扰，在第 0.1.2 版本中增加了缩减冗余不可见字符
		```python
		def data_pretreatment(data_path):
			"""
				传入 文件路径参数 data_path
				返回 经预处理列表 data_listed
			"""
    		data = open(data_path, mode='r').read()	# 读取 data_path 指向文件
    		data_shorted = re.sub(r"\s +", " ", data)	# 缩减冗余不可见字符
    		data_listed = re.split(r"\W", data_shorted)	# 获取单词列表
    		return data	# 返回经过预处理的 data_listed
		```
	3. #### **关键词处理**
		>&#160; &#160; &#160; &#160;这个函数写得比较一气呵成，逻辑上没有出现问题，由于该函数较长，进行程序规范化修改过程程中花费时间较长，给我敲响了警钟。  
		&#160; &#160; &#160; &#160;实现方法上而言并无困难，过程中也是重温了一下 Python 的一些基础语法，同时也解决了一些之前学习 Python 时遇到的小困惑：  
		>
		><font color='OrangeRed'>**问：**</font>只有一个元素的列表可以索引<font color='OrangeRed'>**[-1]**</font>吗？  
		<font color='CornflowerBlue'>**答：**</font>可以，同样索引倒数第一个元素，在只有一个元素的列表中索引的就是唯一那个元素。 

		```python
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

    		data_iter = iter(range(len(data_listed)))  # 生成数据列表迭代器
    		for i in data_iter:
        
       			word = data_listed[i]

        		if word != '' and word in KEYWORDS:  # 判断是否为关键词

        		    key_count = key_count + 1  	# 是关键词则 key_count++

		            if word == 'switch':  		# 若为 switch 则 switch_count++ 
        		        switch_count = switch_count + 1 
                		case_count.append(0)  	# 且 case_count 增加一个元素
            
		            elif word == 'case':		# 若是 case
        		        case_count[-1] += 1		# case_count 对应元素加1

        		    elif word == 'if':   		# 若是 if 则压入堆栈
	                if_stack.append('if')
			
			        elif word == 'else' :   			# 出现 else
					    if data_listed[i+1] == 'if':   	# 出现 elseif
		                    if_stack.append('elif')  	# 压栈 elif
        		            key_count = key_count + 1  	# 计数下一个 if 
                		    data_iter.__next__()  		# 跳过下一个 if
                
                		else :  # 若只是 else

                    		elifFlag = False  	# 初始化 elifFlag 标志

		                    while if_stack[-1] == "elif":
        		                elifFlag =True
                		        if_stack.pop()  # elif 出栈
		                    if_stack.pop()  	# if 出栈

        		            if elifFlag :   	# 根据 elifFlag 增加计数
                		        if_elif_else_count += 1
		                    else :
        		                if_else_count +=  1
		```
	4. #### **输出模式**
		><font color='OrangeRed'>**问：**</font>如何不适用循环打印出列表且不带方括号?
		<font color='CornflowerBlue'>**答：**</font>print(*ListName, seq=' ')
		```python
		def final_print(mode):
    	if mode >= 1:
        	print("total num:",key_count)
    	if mode >= 2:
    	    print("switch num:",switch_count)
    	    print("case num:",end=' ')
    	    if switch_count > 0:
               print(*case_count, sep=' ') 
        	else:
            	print(0)
	    if mode >= 3:
        	print('if-else num:',if_else_count)
	    if mode >= 4:
    	    print('if-elseif-else num:',if_elif_else_count)
		```

+ ### **性能分析**
	1. #### 单元测试
	2. #### 运行时间

### **困难及新获知识**
#### 正则表达式
