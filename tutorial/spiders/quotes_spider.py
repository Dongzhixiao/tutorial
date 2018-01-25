import scrapy
import tutorial.items
import re

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    # headers = {
        # "Accept":"*/*",
        # "Accept-Encoding":"gzip, deflate, sdch",
        # "Accept-Language":"zh-CN,zh;q=0.8",
        # "Cache-Control":"max-age=0",
        # "Connection":"keep-alive",
        # "Host": "www.xxxxxx.com",
        # "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
    # }
    raw_url = 'http://www.csdata.org/p/issue/'
    base_url = 'http://www.csdata.org'

    def start_requests(self):
        yield scrapy.Request(url=self.raw_url, callback=self.parse,dont_filter = True)

    def parse(self, response):
        
        netware = response.selector.xpath('//div[contains(@class,"journal_div")]//a/@href').extract()
        #self.log('文章网址：%s' % netware)
        #self.log('搜索到了: %s' % len(netware))
        
        #netware = ['http://www.csdata.org/p/issue/47/','http://www.csdata.org/p/issue/63/','/p/issue/71/']
        
        for i in range(2,len(netware)):
            #self.log(self.base_url + netware[i])
            s = self.base_url + netware[i]
            yield scrapy.Request(url=s, callback=self.parseChild,dont_filter = True,meta={'url':s})
        
    def parseChild(self,response):
        netware = response.selector.xpath('//div[contains(@class,"all_papers_div2")]//a/@href').extract()
        #self.log('文章网址：%s' % netware)
        #self.log('搜索到了: %s' % len(netware))

        #netware = ['/p/78/']

        for i in range(len(netware)):
            #self.log(self.base_url + netware[i])
            s = self.base_url + netware[i]
            yield scrapy.Request(url=s, callback=self.parseSibling,dont_filter = True,meta={'url':s})

    def dealTime(self,str):
        str = re.sub(r"\n", r"", str)
        str = re.sub(r"\s+", r"", str)
        return str.strip('：')

    def dealAffiliation(self,str):
        str = re.sub(r"\n", r"", str)
        str = re.sub(r"\s+", r"", str)
        return str.split('，')[0]

    def dealCountry(self,str):
        str = re.sub(r"\n", r"", str)
        str = re.sub(r"\s+", r"", str)
        return str.split('，')[-1]

    def parseSibling(self, response):
        #self.log("***********************")
        articleTitle = response.selector.xpath('//div[contains(@class,"title_ch")]/text()').extract()
        #articleTitle = articleTitle.xpath('string(.)').extract()[0]
        #self.log('文章标题：%s' % articleTitle)
        articleTag = 'empty'
        #self.log('文章类别：%s' % articleTag)
        ReceivedTime = response.selector.xpath('//*[@class="received"]/../text()').extract()
        #self.log('文章接收时间：%s' % ReceivedTime)
        AcceptTime = 'emtpy'
        #self.log('文章接受录用时间：%s' % AcceptTime)
        PublishedTime = response.selector.xpath('//*[@class="pub_date"]/../text()').extract()
        #self.log('文章发表时间：%s' % PublishedTime)
        ReferencesNumber = 'empty'
        #self.log('文章引用数目：%s' % ReferencesNumber)
        articleURL = response.meta['url']
        #self.log('文章地址：%s' % articleURL)
        Affiliations = response.selector.xpath('//*[contains(@id,"affChaff1")]/@value').extract()
        #self.log("文章机构：%s"% self.dealAffiliation(Affiliations[0]))
        Authors = response.selector.xpath('//span[@class="info_author_name_article_zh"]/text()').extract()
        #self.log("文章作者：%s" % Authors)
        #Country = Affiliations[0].split(',')[-1]
        fileName = "test.md"
        with open(fileName, 'a',encoding='utf-8') as f:
            # f.write('文章标题：%s' % articleTitle)
            # f.write('\n')
            # f.write('文章类别：%s' % articleTag)
            # f.write('\n')
            #写文章标题
            if len(articleTitle) > 0:
                f.write(articleTitle[0])
            else:
                f.write('empty')
            f.write(' ; ')
            #写文章类别
            f.write(articleTag)
            f.write(' ; ')
            #写文章接收时间
            if len(ReceivedTime) > 0 :
                f.write(self.dealTime(ReceivedTime[0]))
            else:
                f.write('empty')
            f.write(' ; ')
            #写文章接受录用时间
            f.write(AcceptTime)
            f.write(' ; ')
            #文章在线发表时间
            if len(PublishedTime) > 0:
                f.write(self.dealTime(PublishedTime[0]))
            else:
                f.write('empty')
            f.write(' ; ')
            #写文章引用文章数目
            f.write(str(ReferencesNumber))
            f.write(' ; ')
            #文章作者
            if len(Authors) > 0 :
                f.write('/')
                for content in Authors:
                    f.write(content)
                    f.write('/')
            else:
                f.write("empty")
            f.write(' ; ')
            #文章机构信息
            if len(Affiliations) > 0:
                f.write(self.dealAffiliation(Affiliations[0]))
            else:
                f.write("empty")
            f.write(" ; ")
            #文章作者国家
            if len(Affiliations) > 0:
                f.write(self.dealCountry(Affiliations[0]))
            else:
                f.write("empty")
            f.write(' ; ')
            # 文章所在网址
            f.write(articleURL)
            #输出一个空行
            f.write('\n')
        self.log('Saved file %s' % fileName)
        