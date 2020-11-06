import pymysql
import configparser
import matplotlib.pyplot as plot
from matplotlib.font_manager import FontProperties
from pylab import *
import jieba
#E:\pythonanaconda\Lib\site-packages\jieba 结巴库下载包的位置
#连接数据库
def linkMysql():
    cf = configparser.ConfigParser()
    cf.read('config/mysql.ini', encoding='UTF-8')
    conn = pymysql.connect(
        host = cf.get('mysql','host'),
        port = int(cf.get('mysql','port')),
        user = cf.get('mysql','user'),
        passwd = cf.get('mysql','passwd'),
        charset = cf.get('mysql','charset'),
        db = cf.get('mysql', 'db')
    )
    return conn

#查询数据库message这个字段的全部数据 包左也包右
def getMessage(begin,count,message):
    connection = linkMysql()
    end = begin + count
    newresults = []
    allMessage = ""
    #对需要查询的字段进行拼接
    for i in range(0, len(message) - 1, 1):
        allMessage = allMessage + " " + message[i] + ", "
    allMessage = allMessage + message[len(message) - 1]

    #查询数据库
    with connection.cursor() as cursor:
        sql = "select " + allMessage + " from jobhunter"
        cursor.execute(sql)
        results = cursor.fetchall()
        connection.commit()
        if end > len(results):
            end = len(results)
        count = 0
        for result in results:
            if count > end:
                break
            one = []
            for i in range(len(result)):
                one.append(result[i])
            newresults.append(one)
            count += 1
    return newresults

#工资数据清洗
def washAveMoney(message,index): #信息列表 工资信息所在的下标
    for i in range(len(message)):
        unit = 0 #单位
        time = 1 #/年 /月
        s = str(message[i][index])
        if s.find('万') != -1:
            unit = 10000
        else:
            unit = 1000
        if s.find('年') != -1:
            time = 12
        else:
            time = 1
        s = s[0:-3]
        if s.find('-') != -1:
            two = s.split('-')
            min = float(two[0])
            max = float(two[1])
            avg = (max + min) / 2
            s = avg
        else:
            s = 0
        s = int (s * unit / time)
        message[i][index] = s

#工资数据处理
def dealMoney(message,index,index2):
    words = []
    for i in range(0, len(message)):
        words.append(message[i][index])
    results = {}
    i = 0
    for word in words:
        if len(words) == 1:
            continue
        else:
            try:
                number = int(message[i][index2])
            except(Exception):
                pass
            if results.get(word) != None:
                results[word] = (results.get(word, 0) + number) / 2
            else:
                results[word] = results.get(word, 0) + number
        i += 1
    items = []
    for i, j in results.items():
        item = []
        item.append(i)
        item.append(int(j))
        items.append(item)
    items.sort(key=lambda x: x[1], reverse=False)
    print("工资分析")
    for i in range(len(items)):
        word, count = items[i]
        print("{0:<10}{1:>5}".format(word, count))
    return items

#柱状图表示工资平均水平
def showMoney(message):
    #记得这里需要使用plt 不能是plot
    name_list = []
    num_list = []
    for i in range(0, len(message), 1):
        name_list.append(message[i][0])
        num_list.append(message[i][1])
    plt.rcParams['font.sans-serif'] = 'SimHei'
    plt.figure(figsize=(10,10))
    plt.barh(name_list, num_list, alpha=0.6, facecolor = 'deeppink', edgecolor = 'deeppink', label='Jay income')
    plt.title('各职业的平均工资水平',fontsize=20)#标题，并设定字号大小
    plt.savefig('./各职业的平均工资水平')
    plt.show()

def washText(message,index):
    jieba.load_userdict("E:\pythonanaconda\Lib\site-packages\jieba\dict2.txt")
    for i in range(len(message)):
        print(jieba.lcut(message[i][index]))

#岗位要求分析
def dealText(message,index):
    cf = configparser.ConfigParser()
    cf.read('config/workmessage.ini', encoding='UTF-8')
    allType = []
    allCount = {}
    for i in range(0, 263, 1):
        allType.append(cf.get('workmessage', str(i)))
    for i in allType:
        if i.find('/') != -1:
            i = i.split('/')
            allCount[i[0].lower()] = 0
        else:
            allCount[i.lower()] = 0
    for i in range(len(message)):
        for j in allType:
            if j.find('/') != -1:
                j2 = j.split('/')
                for k in j2:
                    message[i][index] = str(message[i][index]).lower()
                    if str(message[i][index]).find(k.lower()) != -1:
                        allCount[j2[0].lower()] += 1
                        break
            else:
                # if str(message[i][index]).lower().find(allType[220].lower()) != -1:
                #     print(message[i][index])
                #     allCount[allType[220].lower()] += 1
                #     break
                if str(message[i][index]).lower().find(j.lower()) != -1:
                    allCount[j.lower()] += 1
    items = []
    for i, j in allCount.items():
        item = []
        item.append(i)
        item.append(int(j))
        items.append(item)
    items.sort(key=lambda x: x[1], reverse=True)
    for i,j in items:
        print(str(i) + "=" + str(j))
    return items

#职位分析(未优化) message为列表。index表示workname下标，index2表示number下标
def dealWorkName(message, index, index2):
    words = []
    for i in range(0,len(message)):
        words.append(message[i][index])
    results = {}
    i = 0
    for word in words:
        if len(words) == 1:
            continue
        else:
            if message[i][index2] == '若干':
                number = 2
            else:
                try:
                    number = int(message[i][index2])
                except(Exception):
                    number = 1
            results[word] = results.get(word, 0) + number
        i += 1
    items = []
    for i,j in results.items():
        item = []
        item.append(i)
        item.append(int(j))
        items.append(item)
    items.sort(key=lambda x:x[1], reverse=True)
    for i in range(len(items)):
        word,count = items[i]
        print("{0:<10}{1:>5}".format(word, count))
    return items

#职位信息清洗
def washWorkName(message,index):
    cf = configparser.ConfigParser()
    cf.read('config/workname.ini',encoding='UTF-8')
    allType = []
    for i in range(0,33,1):
        allType.append(cf.get('workname',str(i)))

    for j in range(0,len(message)):
        flag = False
        for i in allType:
            i = str(i)
            if i.find('/') != -1:
                i = i.split('/')
                for k in i:
                    if str(message[j][index]).find(k) != -1:
                        message[j][index] = i[0]
                        flag = True
                        break
            else:
                if str(message[j][index]).find(i) != -1:
                    message[j][index] = i
                    flag = True
                    break
        if flag == False:
            message[j][index] = "其他"

#职位信息饼状图与工资
def showWorkName(workname):
    sum = 0
    label = []
    values = []
    explode = []
    for i in range(0,len(workname)):
        sum = sum + workname[i][1]
        label.append(workname[i][0])
        values.append(workname[i][1])
        explode.append(0.01)
    print(sum)
    plt.rcParams['font.sans-serif'] = 'SimHei' #设置中文显示
    plt.figure(figsize=(20,20))
    plt.pie(values,explode=explode,labels=label,autopct="%1.1f%%")
    plt.title("职位饼图")
    plt.savefig('./职位饼图')
    plt.show()

if __name__ == '__main__':
    #message = ['company','money','message','workname']
    message = ['workname','number','money','message']
    list = getMessage(0, 500, message)
    # washAveMoney(list,2)
    # # # dealText(list,2)
    # # # print(list)
    # washWorkName(list, 0)
    # workname = dealWorkName(list, 0, 1)
    # money = dealMoney(list, 0, 2)
    # # showMoney(money)
    # showWorkName(workname)
    # washText(list,3)
    dealText(list,3)
    #print(jieba.lcut('岗位职责：参与“互联网＋可信身份认证服务平台”的开发和建设。任职要求：1.2年以上java开发经验（不含实习期），熟悉软件开发流程，有良好的代码习惯；2．掌握主流web服务框架，熟悉客户端和服务端的数据交互开发，有RestfulAPI开发经验者优先；3.熟悉常用数据库，如SQLServer、MySql、Oracle等，有一定的数据库设计和优化能力；4．有实际的高并发或者大数据量开发项目工作经验者优先；5．能较好地与团队合作，思路清晰，有责任心；6.计算机相关专业，本科及以上学历职能类别：Java开发工程师微信分享'))
    # print(jieba.lcut("软件工程中级证书，软考中级通过，计算机专业，有RestfulAPI开发经验者优先,1.2年以上java开发经验（不含实习期）"))
    # jieba.load_userdict("E:\pythonanaconda\Lib\site-packages\jieba\dict2.txt")
    # print(jieba.lcut("软件工程中级证书，软考中级通过，计算机专业，有RestfulAPI开发经验者优先,1.2年以上java开发经验（不含实习期）"))