# coding=UTF-8
import json
import requests
import time
import bs4
import random
import sys
import process
import pdb
reload(sys)
sys.setdefaultencoding('UTF-8')

'''
初始化函数
'''


def init():
    # 请求头
    userAgent = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
                 'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10'
                 ]

    # 经测试可用ip
    usefulIp = []

    # 获取代理ip地址
    uriGetIp = 'http://www.xicidaili.com/wt/'

    # 检测ip是否可用地址
    testGetIp = 'http://icanhazip.com/'

    usefulIp = getUsefulIPList(uriGetIp, testGetIp, userAgent)

    while(True):
        computedData(usefulIp, userAgent)
        time.sleep(60)


'''
获取可用的ip列表
'''


def getUsefulIPList(uriGetIp, testGetIp, userAgent):
    # 全部代理ip
    allProxys = []

    # 经测试可用ip
    usefulIp = []
    ipList = requests.get(
        uriGetIp, headers={'User-Agent': random.choice(userAgent)})

    ipData = bs4.BeautifulSoup(ipList.text, "html.parser")

    ip = ipData.select("#ip_list > tr > td:nth-of-type(2)")

    port = ipData.select("#ip_list > tr > td:nth-of-type(3)")

    protocol = ipData.select("#ip_list > tr > td:nth-of-type(6)")

    for ip, port, protocol in zip(ip, port, protocol):
        proxy = ip.get_text().strip()+':'+port.get_text().strip()
        allProxys.append(proxy)

    print('正在初始化ip数据池，请耐心等待...')

    process.max_steps = len(allProxys)

    process.process_bar = process.ShowProcess(process.max_steps)

    # 筛选可用ip
    for proxy in allProxys:
        process.process_bar.show_process()
        # time.sleep(0.05)
        try:
            theIp = requests.get(testGetIp,  headers={'User-Agent': random.choice(userAgent)}, proxies={
                'http': proxy}, timeout=1, allow_redirects=False)
        except requests.exceptions.Timeout:
            # print('超过1s')
            continue
        except requests.exceptions.ConnectionError:
            # print('连接异常')
            continue
        except requests.exceptions.HTTPError:
            # print('http异常')
            continue
        except:
            # print("其他错误")
            continue
        else:
            if (theIp.status_code == 200 and len(theIp.text) < 20):
                usefulIp.append(proxy)
            #    print(theIp.text)

    print('可用ip池为下：'+','.join(usefulIp))
    return usefulIp


'''
根据ip池爬取数据
'''


def computedData(usefulIp, userAgent, ipIndex=0):
    # debugger
    # pdb.set_trace()
    fhandle = open('../output/output.txt', 'a')  # 追加写入文件

    # Get请求-并传递headers
    try:
        data = requests.get("http://www.ziroom.com/z/nl/z3-r3-o2-s5%E5%8F%B7%E7%BA%BF-t%E5%8C%97%E8%8B%91%E8%B7%AF%E5%8C%97.html",
                            headers={'User-Agent': random.choice(userAgent)}, proxies={'http': random.choice(usefulIp)}, timeout=(3, 7))
        #
        pass
    except:
        print "Error: 请求失败"
        computedData(usefulIp, userAgent)
        return
        pass
    else:
        roomDate = bs4.BeautifulSoup(data.text, "html.parser")
        # 标题
        title = roomDate.select("#houseList > li > div.txt > h3 > a")
        # 地点 改版没了////
        # place = roomDate.select("#houseList > li > div.txt > h4 > a")
        # 距离
        distance = roomDate.select(
            "#houseList > li > div.txt > div > p:nth-of-type(2) > span")
        # 价格
        price = roomDate.select("#houseList > li > div.priceDetail > p.price")
        # 面积
        area = roomDate.select(
            "#houseList > li > div.txt > div > p:nth-of-type(1) > span:nth-of-type(1)")
        # 楼层
        floor = roomDate.select(
            "#houseList > li > div.txt > div > p:nth-of-type(1) > span:nth-of-type(2)")
        # 房间配置
        room = roomDate.select(
            "#houseList > li > div.txt > div > p:nth-of-type(1) > span:nth-of-type(3)")
        #
        print('北京市自如数据如下')
        fhandle.write('北京市'+time.strftime("%Y-%m-%d %H:%M:%S",
                                          time.localtime()) + '自如数据如下'+'\n')

        for title, price, area, floor, room, distance in zip(title, price, area, floor, room, distance):
            last_data = {
                "名称": title.get_text().strip(),
                # "地段": place.get_text().strip(),
                "距离": distance.get_text().strip(),
                "价格": price.get_text().replace(' ', '').replace('\n', ''),
                "面积": area.get_text().strip(),
                "楼层": floor.get_text().strip(),
                "房间大小": room.get_text().strip()
            }

            fhandle.write("名称："+title.get_text().strip())
            # fhandle.write("地段："+place.get_text().strip())
            fhandle.write("距离："+distance.get_text().strip())
            fhandle.write(
                "价格："+price.get_text().replace(' ', '').replace('\n', ''))
            fhandle.write("面积："+area.get_text().strip())
            fhandle.write("楼层："+floor.get_text().strip())
            fhandle.write("房间大小："+room.get_text().strip() + '\n')

            # print  json.dumps(last_data).decode('unicode-escape')
            # print  json.dumps(last_data,ensure_ascii=False)
            print json.dumps(last_data, encoding='UTF-8', ensure_ascii=False)

        fhandle.write("************************************************"+'\n')
        fhandle.close()
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        pass


'''
入口函数
'''
if __name__ == "__main__":
    init()
    pass


