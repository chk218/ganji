# -*- coding:utf-8 -*-
import requests
from pyquery import PyQuery as pq
import xlwt

u1 = "https://3g.ganji.com/sz_zpjiudiancanyin/o_%d/?ifid=gj3g_list_previous__list"
m = "sz_zpjiudiancanyin"
un = "https://3g.ganji.com"
hea = {
    'User-Agent': "Mozilla/5.0 (Linux; Android 5.1; HW-KIW-CL00 Build/KIW-CL00) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36"
}

stus = [['公司', '职位', '要求', '地点', '福利', '电话', '联系人'], ]


def pa():
    # 循环1页
    for ss in range(3):
        ss += 1
        u2 = u1 % ss

        h1 = requests.get(url=u2, headers=hea)
        h2 = pq(h1.text)(".deliver-area")

        for i in h2.items():
            if m in str(i):
                h3 = un + i("a").attr("href")  # 单个信息的url
                h4 = requests.get(h3, headers=hea)

                h5 = pq(h4.text)(".comm-area-b")("table")("td")

                h6 = pq(h4.text)(".com-name").text()  # 获取公司名称

                li = [h6]

                for n in h5.items():
                    nn = n.text()

                    if nn != ">":
                        li.append(nn)
                if len(li) == 6:  # 是否存在‘福利’
                    li.insert(4, "无")
                    stus.append(li)
                else:
                    stus.append(li)
    return stus


print("正在爬取中，请稍等......")
stuss = pa()
book = xlwt.Workbook()  # 新建一个excel
sheet = book.add_sheet('case1_sheet')  # 添加一个sheet页
row = 0  # 控制行
for stu in stuss:
    col = 0  # 控制列
    for s in stu:  # 再循环里面list的值，每一列
        sheet.write(row, col, s)
        col += 1
    row += 1
book.save('职位信息.xls')  # 保存到当前目录下
print("爬取完成！")
