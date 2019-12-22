import matplotlib.pyplot as plt
import matplotlib
import re
class Paint:
    def paint(self,sal):
        language=[]
        avg_sal=[]
        color=['r:','b-','g-.']
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']
        plt.xlabel('编程语言')
        plt.ylabel('平均薪资 (k)')
        plt.title('平均工资')
        for i in sal.keys():
            language.append(i)
            avg_sal.append(sal[i])
        for i in range(len(language)):
            p=plt.bar(language[i],avg_sal[i],label=language[i],width=0.45)
        plt.ylim(0,35)
        plt.legend()
        plt.show()
        plt.savefig('')  #存放路径信息

    def index_paint(self,min_sal,max_sal,language):
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']
        area = []
        max_price=[]
        min_price=[]
        for i in min_sal.keys():
            area.append(i)
        for i in area:
            max_price.append(max_sal[i])
            min_price.append(min_sal[i])
        plt.xlabel('地区')
        plt.ylabel('薪资 (K)')
        plt.title(language+'地区性薪资数据图')
        p1=plt.plot(area,max_price,'r',label='最高工资')
        p2=plt.plot(area,min_price,'b',label='最低工资')
        plt.legend()
        plt.show()
        plt.savefig('')  #路径存放信息