# -*- coding: utf-8 -*-
'''
    文件名：        hnu_grade_spider.py
    功能：          爬取湖南大学教务系统，获取成绩，并计算出学分绩点
    版本：          0.1
    知识点：         网络爬虫、登录
    语言:           python 2.7.9
    完成情况：       爬取了成绩，为完成学分绩的计算（不知道具体算法）
    改进点：
    
'''

import urllib
import urllib2
import cookielib

import re

class HNU_Grade_Spider(object):
    '''
        HNU_Grade_Spider
        用于爬取本人湖南大学教务系统成绩页面，并计算学分绩点

        属性：
            loginUrl：    登录成功后的界面url（不是登录界面）
            gradeUrl：    成绩查询页面url
    
            username：    登录名
            passwd：      登录密码
            postdata：    登录时提交的数据

            headers：     请求头

            cookies:      用于保存登录信息
            opener:

            gradeInfo:    成绩信息
    '''
    
    def __init__(self):
        self.loginUrl = 'http://yjs.hnu.cn/pyxx/login.aspx'
        self.gradeUrl = 'http://yjs.hnu.cn/pyxx/grgl/xskccjcx.aspx'

        print u'请输入学号和密码'
        self.username = raw_input()
        self.passwd = raw_input()
        self.postdata = urllib.urlencode({
            '__VIEWSTATE':'dDw1MzgxOztsPF9jdGwwOkltYWdlQnV0dG9uMTtfY3RsMDpJbWFnZUJ1dHRvbjI7Pj6hWty8bfyqvFNNQ4MeMOas3459GA==',
            '__VIEWSTATEGENERATOR':'F6318A86',
            '_ctl0:txtusername':self.username,
            '_ctl0:ImageButton1.x':'10',
            '_ctl0:ImageButton1.y':'23',
            '_ctl0:txtpassword':self.passwd
        })
        
        self.headers = {
##            'Connection': 'keep-alive',
##            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
##            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
##            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0',
##            'Referer':'http://yjs.hnu.cn/pyxx/login.aspx'
        }

        self.cookies = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))

        self.gradeInfo = []

    def login(self):
        '''
            login
            模拟登入教务系统

            参数：
                无
            返回值：
                无
        '''
        try:
            request = urllib2.Request(self.loginUrl, self.postdata, self.headers)
            loginPage = self.opener.open(request)
         #  print loginPage.read().decode('utf-8')
            return True 
            
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print u'连接失败，错误原因', e.reason
                return False

    def getGrade(self):
        '''
            getGrade
            获取成绩

            参数：无
            返回值：无
        '''
        if self.login():    # 登录，为了保存cookie
            gradePage = self.opener.open(self.gradeUrl)
          # print gradePage.read()

            regex_item = '</tr><tr nowrap="nowrap">.*?'     # 每一门成绩的起始标志
            regex_course = '<td><font size="2">(.*?)</font></td>'
            regex_credit = regex_course
            regex_term = regex_course
            regex_grade = regex_course

            regex = regex_item + regex_course + regex_credit + regex_term + regex_grade

            pattern = re.compile(regex, re.S)
            self.gradeInfo = re.findall(pattern, gradePage.read())

            for item in self.gradeInfo:
                print item[0], item[1], item[2], item[3]
        else:
            print u'登录失败'

    def calcGPA(self):
        '''
            calcGPA
            根据成绩计算平均学分绩

            参数：无
            返回值：无
            
        '''
        self.getGrade() # 获取成绩信息

        '''
            开始计算，计算公式??
        '''
        pass

    def start(self):
        '''
            启动函数
        '''
        print u'爬虫开始'
        self.calcGPA()
        print u'爬虫结束'
  


def main():
    '''
        '主函数'
    '''
    spider = HNU_Grade_Spider()
    spider.start()

main()
