# File类
class  File:
    # 读文件
    def readFile(self,file_name):
        print('正在读文件')
        # 读文件,编码格式utf-8
        f = open(file_name,encoding='utf-8')
        # 创建一个集合
        employees =[]
        # 按行读
        lines = f.readlines()
        # 遍历每一行
        for line in lines:
            # 按照逗号分割
            elements = line.split(',')
            # 创建一个实体
            employee = {}
            # 给属性赋值
            employee['name']=elements[0]
            employee['age']=int(elements[1])
            employee['salary']=float(elements[2])
            # 加入集合
            employees.append(employee)
        # 关闭文件
        f.close()
        print('读完了')
        # 返回集合
        return employees
    
    # 写文件
    def writeFile(self,file_name,message):
        print('正在写文件')
        # mode="w"，写模式，会重写文件；mode="a"，追加模式，会在文件末尾添加数据。
        with open(file_name, encoding="utf-8",mode="a") as data:  
            data.write(message)  
        print('写完了')

# 实例化对象
file = File()
# \n是换行
# message = '\n小刚,12,212121'
# 写文件    
# file.writeFile('1.txt',message)
# 读文件
employees = file.readFile('1.txt')
# 输出集合
print(employees)



